FROM ghcr.io/iximiuz/labs/rootfs:ubuntu-docker

LABEL org.opencontainers.image.source=https://github.com/unlabs-dev/uncloud-labs

# Update Docker to latest stable
RUN --mount=type=bind,source=scripts,target=/tmp/scripts sudo /tmp/scripts/install-docker.sh

ENV UNCLOUD_VERSION=v0.17.1
RUN curl -fsS https://get.uncloud.run/install.sh | sudo env VERSION=${UNCLOUD_VERSION} sh

COPY ./rootfs-images/uncloud-django-app/app /home/laborant/app
RUN sudo chown -R laborant:laborant /home/laborant/app
