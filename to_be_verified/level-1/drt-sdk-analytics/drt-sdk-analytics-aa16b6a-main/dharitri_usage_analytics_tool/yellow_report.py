from typing import Any, Dict, cast

import dash
import plotly.graph_objs as go
from dash import Input, Output, dcc, html

from dharitri_usage_analytics_tool.ecosystem_configuration import \
    EcosystemConfiguration
from dharitri_usage_analytics_tool.elastic_fetcher import (
    ElasticSearchFetcher, ElasticSearchPackage)
from dharitri_usage_analytics_tool.fetcher import Package
from dharitri_usage_analytics_tool.utils import (FormattedDate, Reports,
                                                   get_environment_var)

report_type = Reports.YELLOW.value


app = dash.Dash(__name__)


def get_layout():
    directory = get_environment_var('JSON_FOLDER')
    dropdown_options = report_type.get_report_dropdown_options(directory)
    selected_option = dropdown_options[0]['value'] if dropdown_options else None  # Set default value as the newest file generated

    # Layout of the Dash app
    return html.Div(style={'backgroundColor': report_type.repo_color}, children=[
        html.Div(
            style={
                'display': 'flex',
                'alignItems': 'center'
            },
            children=[
                html.H1(
                    report_type.repo_title,
                    style={'marginRight': '20px', 'width': '30%'}
                ),
                dcc.Dropdown(
                    id='file-selector', maxHeight=1000,
                    options=dropdown_options,
                    value=selected_option,
                    clearable=False,
                    style={'width': '35%'}
                ),
            ]
        ),

        # Container for dynamic content
        html.Div(id='report-content')
    ])


app.layout = get_layout


def create_table(fetcher: ElasticSearchFetcher, section: str):
    header_row = html.Thead([
        html.Th('User', style={'width': '70%', 'textAlign': 'left'}),
        html.Th('Count Total', style={'width': '10%', 'textAlign': 'right'}),
        html.Th('Count last week', style={'width': '10%', 'textAlign': 'right'}),
        html.Th('Avg count per day', style={'width': '10%', 'textAlign': 'right'}),
    ])
    table_header = [header_row]
    table_rows = []
    packages: list[ElasticSearchPackage] = [cast(ElasticSearchPackage, item) for item in fetcher.packages]
    packages.sort(key=lambda pkg: pkg.no_of_downloads, reverse=True)
    total: Dict[str, int] = {'total_usage': 0, 'last_week_usage': 0}
    for package in packages:
        package_statistics = package.create_summary_statistics_from_daily_downloads(fetcher.end_date, report_type.repo_length)
        total['total_usage'] += package_statistics['downloads_total']
        total['last_week_usage'] += package_statistics['downloads_last_week']

        row = [
            html.Td(package.package_name),
            html.Td(f'{package_statistics["downloads_total"]:,}', style={'textAlign': 'right', 'maxWidth': '10ch'}),
            html.Td(f'{package_statistics["downloads_last_week"]:,}', style={'textAlign': 'right'}),
            html.Td(f'{int(package_statistics["avg_daily_downloads"]):,}', style={'textAlign': 'right'}),
        ]
        table_rows.append(html.Tr(row))

    row = html.Tr([
        html.Td('Total', style={'fontWeight': 'bold'}),
        html.Td(f'{total["total_usage"]:,}', style={'textAlign': 'right', 'maxWidth': '10ch', 'fontWeight': 'bold'}),
        html.Td(f'{total["last_week_usage"]:,}', style={'textAlign': 'right', 'fontWeight': 'bold'}),
        html.Td(f'{total["total_usage"] / report_type.repo_length:,.0f}', style={'textAlign': 'right', 'fontWeight': 'bold'}),
    ])
    table_rows.append(row)

    return html.Table(table_header + table_rows, id='downloads_table', style={
        'width': '98%',
        'borderCollapse': 'collapse',
    })


def create_graph(fetcher: ElasticSearchFetcher, section: str) -> Dict[str, Any]:
    packages: list[Package] = [item for item in fetcher.packages]
    packages.sort(key=lambda pkg: pkg.no_of_downloads, reverse=True)
    downloads_dict = {p.package_name: {d.date: d.downloads for d in p.downloads} for p in packages}
    start_date = FormattedDate.from_string(fetcher.start_date)
    end_date = FormattedDate.from_string(fetcher.end_date)
    date_range = [str(start_date + x) for x in range(end_date.days_from(start_date) + 1)]

    traces = [
        go.Scatter(
            x=date_range,
            y=[int(downloads_dict[package.package_name].get(d, 0)) for d in date_range],
            mode='lines+markers',
            name=package.package_name
        )
        for package in [p for p in packages if p.no_of_downloads > 1000]
    ]

    return {
        'data': traces,
        'layout': go.Layout(
            title='Daily Usage Evolution',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Usage'},
            hovermode='closest'
        )
    }


@app.callback(
    Output('report-content', 'children'),
    Input('file-selector', 'value')
)
def update_yellow_report(selected_file: str):
    selected_organization = 'DHARITRI'
    organization = EcosystemConfiguration[selected_organization.upper()].value
    fetcher = ElasticSearchFetcher.from_generated_file(selected_file, organization)
    return html.Div([
        dcc.Tabs([
            dcc.Tab(label=section.replace('_', ' '), id=section, style={'font-weight': 'normal'},
                    selected_style={'font-weight': 'bold'}, children=[
                html.H1(f"{organization.name} - {section.replace('_', ' ')} - API User Agent Access Details"),
                html.H2('Access Data Table'),
                create_table(fetcher, section),

                html.H2('Access Trends'),
                html.Div([
                    dcc.Graph(
                        id='downloads-graph',
                        figure=create_graph(fetcher, section)
                    ),
                ], style={'display': 'inline-block', 'width': '100%'}),
            ])
            for section in ['Grouped_data']
        ],
            colors={
            "border": "white",  # Border color
            "primary": "blue",  # Color of the selected tab
            "background": "lightgray"  # Color of the unselected tabs
        }),
    ])


if __name__ == '__main__':
    app.run_server(debug=False, port=report_type.repo_port, host='0.0.0.0')
