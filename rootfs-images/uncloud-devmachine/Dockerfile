FROM ghcr.io/iximiuz/labs/rootfs:ubuntu-docker

LABEL org.opencontainers.image.source=https://github.com/unlabs-dev/uncloud-labs

# Update Docker to latest stable
RUN --mount=type=bind,source=scripts,target=/tmp/scripts sudo /tmp/scripts/install-docker.sh

ARG UNCLOUD_VERSION
RUN curl -fsS https://get.uncloud.run/install.sh | sudo env VERSION=${UNCLOUD_VERSION} sh
