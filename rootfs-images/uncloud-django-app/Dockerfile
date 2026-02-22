FROM ghcr.io/iximiuz/labs/rootfs:ubuntu-docker

# Update Docker to latest stable
RUN --mount=type=bind,source=scripts,target=/tmp/scripts sudo /tmp/scripts/install-docker.sh

# Install latest Uncloud
RUN curl -fsS https://get.uncloud.run/install.sh | sudo sh

COPY ./rootfs-images/uncloud-django-app/app /home/laborant/app
RUN sudo chown -R laborant:laborant /home/laborant/app

RUN sudo mkdir -p /opt/tutorial-files \
    && cd /home/laborant/app \
    && sudo mv Dockerfile compose.yaml /opt/tutorial-files/
