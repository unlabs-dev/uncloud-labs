FROM ghcr.io/iximiuz/labs/rootfs:ubuntu-docker

LABEL org.opencontainers.image.source=https://github.com/tonyo/uncloud-labs

# Update Docker to latest stable
RUN --mount=type=bind,source=scripts,target=/tmp/scripts sudo /tmp/scripts/install-docker.sh

ENV UNCLOUD_VERSION=v0.17.1
RUN curl -fsS https://get.uncloud.run/install.sh | VERSION=${UNCLOUD_VERSION} sudo sh
