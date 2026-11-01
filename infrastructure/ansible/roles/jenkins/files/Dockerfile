FROM jenkins/jenkins:lts-jdk21

USER root

# Docker CLI, Compose, Buildx и инструменты для pipeline.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        openssh-client \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg \
        -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && . /etc/os-release \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian ${VERSION_CODENAME} stable" \
        > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        docker-ce-cli \
        docker-buildx-plugin \
        docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

# Версия инструмента согласована с Kubernetes в K3s.
ARG KUBECTL_VERSION=v1.36.4

# Установка kubectl с проверкой контрольной суммы.
# Kustomize доступен через команду kubectl kustomize.
RUN set -eu; \
    arch="$(dpkg --print-architecture)"; \
    case "$arch" in \
        amd64|arm64) ;; \
        *) echo "Unsupported architecture: $arch"; exit 1 ;; \
    esac; \
    download_dir="$(mktemp -d)"; \
    cd "$download_dir"; \
    curl -fsSL --retry 3 \
        "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${arch}/kubectl" \
        -o kubectl; \
    curl -fsSL --retry 3 \
        "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${arch}/kubectl.sha256" \
        -o kubectl.sha256; \
    printf '%s  kubectl\n' "$(cat kubectl.sha256)" | sha256sum --check; \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl; \
    cd /; \
    rm -rf "$download_dir"; \
    kubectl version --client=true

USER jenkins

RUN jenkins-plugin-cli --plugins \
    workflow-aggregator \
    git \
    github \
    docker-workflow \
    ssh-agent \
    credentials-binding