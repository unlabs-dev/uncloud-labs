FROM ghcr.io/iximiuz/labs/rootfs:ubuntu-docker

LABEL org.opencontainers.image.source=https://github.com/unlabs-dev/uncloud-labs

# Update Docker to latest stable
RUN --mount=type=bind,source=scripts,target=/tmp/scripts sudo /tmp/scripts/install-docker.sh

# Install Uncloud components
ENV UNCLOUD_VERSION=v0.17.1
RUN curl -fsS https://raw.githubusercontent.com/psviderski/uncloud/tags/${UNCLOUD_VERSION}/scripts/install.sh \
    | sudo INSTALL_ONLY=true UNCLOUD_VERSION=${UNCLOUD_VERSION} bash
