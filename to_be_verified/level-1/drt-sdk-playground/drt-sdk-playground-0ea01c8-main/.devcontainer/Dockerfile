FROM ubuntu:22.04

ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install some dependencies as root
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    python3.10 python3-pip python3.10-venv \
    git \
    pkg-config \
    libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Switch to regular user
USER $USERNAME
WORKDIR /home/${USERNAME}

ENV DHARITRI="/home/${USERNAME}/dharitri-sdk"
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
ENV PATH="/home/${USERNAME}/.cargo/bin:${PATH}"

# Install pipx
RUN python3 -m pip install --no-cache-dir --user pipx

# Install drtpy
ARG VERSION_DRTPY="v9.10.2"
RUN pipx install dharitri-sdk-cli==${VERSION_DRTPY}

# Install rust and other tools
ARG VERSION_RUST="1.82.0"
RUN wget -O rustup.sh https://sh.rustup.rs && \
    chmod +x rustup.sh && \
    ./rustup.sh --verbose --default-toolchain ${VERSION_RUST} --target wasm32-unknown-unknown -y && \
    rm -rf /home/${USERNAME}/.cargo/registry/* && rm -rf /home/${USERNAME}/.cargo/git/*

ARG VERSION_SC_META="0.54.0"
RUN cargo install dharitri-sc-meta --locked --version ${VERSION_SC_META} && \
    rustup component add rustfmt && \
    rm -rf /home/${USERNAME}/.cargo/registry/* && rm -rf /home/${USERNAME}/.cargo/git/*

RUN sc-meta install all

# Temporary workaround (until fixes in drt-rs-sdk are released):
# https://github.com/TerraDharitri/drt-rs-sdk/pull/1424
COPY "./run-scenarios" /home/${USERNAME}/.cargo/bin/run-scenarios

# Install test wallets
RUN drtpy deps install testwallets && rm ${DHARITRI}/*.tar.gz

# Install Node JS
ARG VERSION_NODE=22
RUN wget -O install.sh https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh && \
    chmod +x install.sh && \
    ./install.sh
ENV NVM_DIR=/home/${USERNAME}/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${VERSION_NODE}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${VERSION_NODE}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${VERSION_NODE}
ENV PATH="/home/${USERNAME}/.nvm/versions/node/v${VERSION_NODE}/bin:${PATH}"

# Install DharitrI libraries (Python)
ARG SDK_PY_VERSION="1.0.0"

RUN pip3 install dharitri-sdk==${SDK_PY_VERSION}

# Note: DharitrI libraries for JavaScript / TypeScript aren't installed globally.
