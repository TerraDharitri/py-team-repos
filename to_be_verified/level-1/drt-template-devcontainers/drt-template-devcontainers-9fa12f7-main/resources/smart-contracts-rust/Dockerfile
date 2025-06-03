FROM ubuntu:22.04

ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ARG VERSION_DRTPY="v9.8.1"
ARG VERSION_RUST="1.82.0"
ARG VERSION_SC_META="0.54.0"
ARG VERSION_WASM_OPT="0.116.1"

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
RUN pipx install dharitri-sdk-cli==${VERSION_DRTPY}

# Install rust and other tools
RUN drtpy config set "dependencies.rust.tag" ${VERSION_RUST} && \
    drtpy config set "dependencies.sc-meta.tag" ${VERSION_SC_META}
RUN drtpy deps install rust && rm -rf /home/${USERNAME}/.cargo/registry/* && rm -rf /home/${USERNAME}/.cargo/git/*
RUN cargo install wasm-opt --version ${VERSION_WASM_OPT}

# Install test wallets
RUN drtpy deps install testwallets && rm ${DHARITRI}/*.tar.gz

RUN rustup component add rustfmt && rm -rf /home/${USERNAME}/.cargo/registry/* && rm -rf /home/${USERNAME}/.cargo/git/*

# This command will be executed once the devcontainer is created
COPY "post_create_command.py" "${DHARITRI}/devcontainer-resources/"
