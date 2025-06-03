# Simple personal passwords manager on the blockchain

## Prerequisites

For clipboard interaction:

```
sudo apt install xclip
```

## How to run

Initialize password manager:

```
python3 ./passwords_manager/main.py init
```

Insert or update entries:

```
python3 ./passwords_manager/main.py upsert --secret=./passwords_manager/testdata/secret.hex --wallet=./passwords_manager/testdata/wallet.pem --url=https://devnet-gateway.dharitri.com
```

Reveal entries:

```
python3 ./passwords_manager/main.py get --secret=./passwords_manager/testdata/secret.hex --address=drt1kvudr40e0mp46cv59mj5dawezwce6pffg25xtkflm6xgagpax43swhrfqa --url=https://devnet-gateway.dharitri.com
```

## Development setup

Create a virtual environment and install the dependencies:

```
python3 -m venv ./.venv
source ./.venv/bin/activate
pip install -r ./requirements.txt --upgrade
pip install autopep8
```

If using VSCode, restart it or follow these steps:
 - `Ctrl + Shift + P`
 - _Select Interpreter_
 - Choose `./.venv/bin/python`.
