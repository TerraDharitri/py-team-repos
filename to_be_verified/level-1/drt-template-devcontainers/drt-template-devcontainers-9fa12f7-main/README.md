# drt-template-devcontainers

DharitrI devcontainer templates to be used in **VSCode** or **GitHub Codespaces**, for Smart Contract development (others to come).

## For users of the templates

Before everything, please follow the Visual Studio Code series on dev containers:
 - [Beginner's Series to Dev Containers](https://youtube.com/playlist?list=PLj6YeMhvp2S5G_X6ZyMc8gfXPMFPg3O31)
 - [Dev Container How To](https://youtube.com/playlist?list=PLj6YeMhvp2S6GjVyDHTPp8tLOR0xLGLYb)
 - [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers)

In Visual Studio code, the following DharitrI dev containers are available:

 - [DharitrI: Smart Contracts Development (Rust)](src/smart-contracts-rust)
 - ...

## Using the Docker images without VSCode

If you'd like to use the Docker image(s) to invoke `drtpy` commands and build contracts directly from a terminal, without VSCode's devcontainers feature, below are a few examples.

First, let's export some environment variables:

```
export IMAGE=terradharitri/devcontainer-smart-contracts-rust:latest
export DOCKER_USER=$(id -u):$(id -g)

# Mandatory: run the container as the current user (should be 1000:1000), not as root.
# Suggestion: use a stateless container; remove it after use (--rm).
# Suggestion: map the current directory to "/data" in the container.
export RUN="docker run --network=host --user=${DOCKER_USER} --rm -it --volume $(pwd):/data"
```

Run the container and do a quick inspection:

```
${RUN} ${IMAGE} whoami
${RUN} ${IMAGE} drtpy --version
${RUN} ${IMAGE} cargo --version
${RUN} ${IMAGE} rustc --version
${RUN} ${IMAGE} sc-meta --version
${RUN} ${IMAGE} wasm-opt --version
```

Clone `drt-rs-contracts` locally, then build a few contracts within the container:

```
git clone https://github.com/TerraDharitri/drt-rs-contracts.git  --single-branch --depth=1

${RUN} ${IMAGE} sc-meta all build --path /data/drt-rs-contracts/contracts/adder
stat ./drt-rs-contracts/contracts/adder/output/adder.wasm

${RUN} ${IMAGE} sc-meta all build --path /data/drt-rs-contracts/contracts/ping-pong-rewa
stat ./drt-rs-contracts/contracts/ping-pong-rewa/output/ping-pong-rewa.wasm
```

Deploy a previously-built smart contract on Devnet:

```
${RUN} ${IMAGE} drtpy contract deploy \
    --bytecode /data/drt-rs-contracts/contracts/adder/output/adder.wasm \
    --arguments 0 \
    --pem /home/developer/dharitri-sdk/testwallets/latest/users/alice.pem \
    --recall-nonce \
    --gas-limit 5000000 \
    --chain D \
    --proxy https://devnet-gateway.dharitri.com \
    --send
```

Call a function of a previously-deployed smart contract:

```
${RUN} ${IMAGE} drtpy contract call \
    drt1qqqqqqqqqqqqqpgqr3clh6ghpww5fc4uhwh2amsseuvecswzd8ssmqdyn0 \
    --function "add" \
    --arguments 42 \
    --pem /home/developer/dharitri-sdk/testwallets/latest/users/alice.pem \
    --recall-nonce \
    --gas-limit 5000000 \
    --chain D \
    --proxy https://devnet-gateway.dharitri.com \
    --send
```

Query a smart contract:

```
${RUN} ${IMAGE} drtpy contract query \
    drt1qqqqqqqqqqqqqpgqr3clh6ghpww5fc4uhwh2amsseuvecswzd8ssmqdyn0 \
    --function "getSum" \
    --proxy https://devnet-gateway.dharitri.com
```

Setup a localnet (make sure to set the `--workdir`, as well), then inspect the generated files (on the mapped volume):

```
${RUN} --workdir /data ${IMAGE} drtpy localnet setup
cat ./localnet.toml
tree -L 1 ./localnet
```

Start the localnet (make sure to publish the necessary ports; see the generated `localnet.toml`):

```
${RUN} --workdir /data --publish 7950:7950 ${IMAGE} drtpy localnet start
```

You can pause the localnet by simply stopping the container, then restart it by invoking the `start` command again.

In a separate terminal, inspect an endpoint of the localnet's Proxy (as a smoke test):

```
curl http://127.0.0.1:7950/network/config | jq
```

## For maintainers of the templates

Skip this section if you are not a maintainer of this repository.

Resources:
 - [Create a Dev Container](https://code.visualstudio.com/docs/devcontainers/create-dev-container)
 - [devcontainers/templates](https://github.com/devcontainers/templates)
 - [devcontainers/template-starter](https://github.com/devcontainers/template-starter)
 - [Public index of templates](https://containers.dev/templates)


### Build images

Build the Docker images for local testing:

```
docker build --network=host ./resources/smart-contracts-rust -t terradharitri/devcontainer-smart-contracts-rust:latest -f ./resources/smart-contracts-rust/Dockerfile
```

### Test the templates

```
rm -rf "/tmp/test-workspace" && mkdir -p "/tmp/test-workspace" && \
cp -R "src/smart-contracts-rust/.devcontainer" "/tmp/test-workspace" && \
code "/tmp/test-workspace/"
```

Then, in VSCode, launch the command `Dev Containers: Rebuild and Reopen in Container`, wait, then inspect the environment. For example, check version of `drtpy`, `rust`, `sc-meta`, build the sample smart contracts, verify output of `rust-analyzer`.

### Publish images

Locally:

```
docker build --network=host ./resources/smart-contracts-rust -t terradharitri/devcontainer-smart-contracts-rust:latest -f ./resources/smart-contracts-rust/Dockerfile
docker push terradharitri/devcontainer-smart-contracts-rust:latest
```

On Github, trigger the GitHub workflow(s) `publish-image-*.yml` to publish the image(s). Ideally, do this on the `main` branch.

### Publish templates

Trigger the GitHub workflow `publish-templates.yml` to publish the templates. Ideally, do this on the `main` branch.
