from enum import Enum

from dharitri_usage_analytics_tool.ecosystem import Organization
from dharitri_usage_analytics_tool.utils import PackagesRegistries


class EcosystemConfiguration(Enum):
    DHARITRI = Organization(
        name='Dharitri',
        search_includes={
            PackagesRegistries.NPM.value.repo_name: '@terradharitri/sdk',
            PackagesRegistries.CARGO.value.repo_name: 'dharitri',
            PackagesRegistries.PYPI.value.repo_name: 'dharitri-sdk',
            PackagesRegistries.GITHUB.value.repo_name: 'sdk',
        },
        search_excludes={
            PackagesRegistries.GITHUB.value.repo_name: 'deprecated'
        },
        github_organization='dharitri',
        gather_data=True,
        report_warnings=True,
    )
    SOLANA = Organization(
        name='Solana',
        search_includes={
            PackagesRegistries.NPM.value.repo_name: '@solana',
            PackagesRegistries.CARGO.value.repo_name: 'solana',
            PackagesRegistries.PYPI.value.repo_name: 'solana',
            PackagesRegistries.GITHUB.value.repo_name: '',
        },
        search_excludes={
            PackagesRegistries.GITHUB.value.repo_name: 'deprecated'
        },
        github_organization='solana-labs',
        affiliated_orgs=['anza-xyz', 'michaelhly'],
        gather_data=True,
        report_warnings=False,
    )
    NEAR = Organization(
        name='Near',
        search_includes={
            PackagesRegistries.NPM.value.repo_name: 'near-',
            PackagesRegistries.CARGO.value.repo_name: 'near-',
            PackagesRegistries.PYPI.value.repo_name: 'near',
            PackagesRegistries.GITHUB.value.repo_name: 'near',
        },
        search_excludes={
            PackagesRegistries.GITHUB.value.repo_name: 'deprecated'
        },
        github_organization='near',
        gather_data=True,
        report_warnings=False,
    )
    AVALANCHE = Organization(
        name='Avalanche',
        search_includes={
            PackagesRegistries.NPM.value.repo_name: '@avalabs/',
            PackagesRegistries.CARGO.value.repo_name: 'avalanche',
            PackagesRegistries.PYPI.value.repo_name: 'avalanche',
            PackagesRegistries.GITHUB.value.repo_name: '',
        },
        search_excludes={
            PackagesRegistries.GITHUB.value.repo_name: 'deprecated'
        },
        github_organization='ava-labs',
        gather_data=True,
        report_warnings=False,
    )
