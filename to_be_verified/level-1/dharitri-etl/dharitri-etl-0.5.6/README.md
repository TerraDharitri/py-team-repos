# DharitrI ETL

ETL (extract, transform and load) tools for publishing DharitrI blockchain data (extracted from a standard DharitrI Elasticsearch instance) on Google BigQuery.

## Published data

[Mainnet](https://console.cloud.google.com/marketplace/product/bigquery-public-data/blockchain-analytics-dharitri-mainnet-eu)

## Setup virtual environment

Create a virtual environment and install the dependencies:

```
python3 -m venv ./venv
source ./venv/bin/activate

pip install -r ./requirements.txt --upgrade
pip install -r ./requirements-dev.txt --upgrade
```

## Run the tests

```
export PYTHONPATH=.
pytest -m "not integration"
```

## Quickstart

This implementation copies the data from Elasticsearch in two parallel flows.

One flow copies the append-only indices (e.g. blocks, transactions, logs, receipts, etc.) into a staging BQ dataset. This process is incremental, i.e. it only copies the new data since the last run, and it's executed more often than the second flow (every 1 hour, by default). Once the staging database is loaded, the data is transferred to the main BQ dataset, using the _Big Query Data Transfers_ facility.

The second flow copies the mutable indices (e.g. tokens, accounts, etc.) into a staging BQ dataset. This process is not incremental. Tables are truncated and reloaded on each run. Once the staging database is loaded, the data is transferred to the main BQ dataset, using the _Big Query Data Transfers_ facility. This flow is executed less often than the first flow (every 4 hours, by default).

In order to invoke the two processes, you can either use the Docker setup (see next section) or explicitly invoke the following commands:

```
# First, set the following environment variables:
export GCP_PROJECT_ID=dharitri-blockchain-etl
export WORKSPACE=${HOME}/dharitri-etl/mainnet

# The first flow (for append-only indices):
python3 -m dharitrietl.app process-append-only-indices --workspace=${WORKSPACE} --sleep-between-iterations=3600

# The second flow (for mutable indices):
python3 -m dharitrietl.app process-mutable-indices --workspace=${WORKSPACE} --sleep-between-iterations=86400
```

### Rewinding

Sometimes, errors occur during the ETL process. For the append-only flow, it's recommended to rewind the BQ tables to the latest checkpoint (good state), and re-run the process only after that. This helps to de-duplicate the data beforehand, through a simple data removal. Otherwise, the full data de-duplication step would be employed (performed automatically, after each bulk of tasks, if the data counts from BQ and Elasticsearch do not match), which is more expensive.

To rewind the BQ tables corresponding to the append-only indices to the latest checkpoint, run the following command:

```
python3 -m dharitrietl.app rewind --workspace=${WORKSPACE}
```

If the checkpoint is not available or is assumed to be corrupted, one can find the latest good checkpoint by running the following command:

```
python3 -m dharitrietl.app find-latest-good-checkpoint --workspace=${WORKSPACE}
```

## Docker setup

Build the Docker image:

```
docker build --network host -f ./docker/Dockerfile -t dharitri-etl:latest .
```

Set up the containers:

```
# mainnet
docker compose --file ./docker/docker-compose.yml \
    --env-file ./docker/env/mainnet.env \
    --project-name dharitri-etl-mainnet up --detach

# devnet
docker compose --file ./docker/docker-compose.yml \
    --env-file ./docker/env/devnet.env \
    --project-name dharitri-etl-devnet up --detach

# testnet
docker compose --file ./docker/docker-compose.yml \
    --env-file ./docker/env/testnet.env \
    --project-name dharitri-etl-testnet up --detach
```

## Generate schema files

Maintainers of this repository should trigger a re-generation of the BigQuery schema files whenever the Elasticsearch schema is updated. This is done by running the following command (make sure to check out [drt-go-chain-tools](https://github.com/TerraDharitri/drt-go-chain-tools) in advance):

```
python3 -m dharitrietl.app regenerate-schema --input-folder=~/drt-go-chain-tools/elasticreindexer/cmd/indices-creator/config/noKibana/ --output-folder=./schema
```

The resulting files should be committed to this repository.

At times, the **load** step could fail for some tables due to, say, new fields added to Elasticsearch indices (of which the BigQuery schema was not aware). If so, then re-generate the schema files (see above), update the BigQuery with the `bq` command (example below is for the `tokens` table), and restart the ETL flow:

```
bq update ${GCP_PROJECT_ID}:${BQ_DATASET}.tokens schema/tokens.json
```

## Running integration tests

Generally speaking, the current integration tests should be ran locally (in the future, they might be added in the CI pipeline).

First, connect to the Google Cloud Platform as follows:

```
gcloud auth application-default login
gcloud config set project dharitri-blockchain-etl
gcloud auth application-default set-quota-project dharitri-blockchain-etl
```

Then, run the integration tests:

```
pytest -m "integration"
```

## Management (Google Cloud Console)

Below are a few links useful for managing the ETL process. They are only accessible to the DharitrI team.

- [BigQuery Workspace](https://console.cloud.google.com/bigquery?project=dharitri-blockchain-etl): inspect and manage the BigQuery datasets and tables.
- [Analytics Hub](https://console.cloud.google.com/bigquery/analytics-hub/exchanges?project=dharitri-blockchain-etl): create and publish data listings.
- [Logs Explorer](https://console.cloud.google.com/logs/query?project=dharitri-blockchain-etl): inspect logs.
- [Monitoring](https://console.cloud.google.com/bigquery/admin/monitoring?project=dharitri-blockchain-etl&region=eu): resource utilization and jobs explorer.
- [Data Transfers](https://console.cloud.google.com/bigquery/transfers?project=dharitri-blockchain-etl): inspect and manage the data transfers.
