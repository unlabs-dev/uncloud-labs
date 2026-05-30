---
kind: page

# Issue: currently title should be more at least 10 characters long
title: Uncloud.run

description: |-
  Deploy and manage containerised apps across servers — without Kubernetes overhead.

categories:
  - linux
  - containers
  - networking

tagz:
  - uncloud
  - docker
  - self-hosting

createdAt: 2026-05-28
updatedAt: 2026-05-29

cover: __static__/logo-wide.png

tutorials:
  uncloud-create-cluster-ebebf72b: {}
  uncloud-deploy-django-app-7a378bc3: {}

playgrounds:
  uncloud-cluster-64523f7c: {}
---

<img src="__static__/logo-title.svg" width="40%" style="display: block; margin: 0 auto;" alt="Uncloud logo">

[Uncloud](https://uncloud.run) is a lightweight tool for deploying and managing containerised applications across a cluster of Linux machines. Connect any cloud VMs or bare-metal servers into a secure [WireGuard](https://www.wireguard.com/) mesh network, then deploy and scale services using familiar [Docker Compose](https://docs.docker.com/reference/compose-file/) files and Docker-like CLI commands.

It sits in the gap between Docker Compose (single-machine only) and Kubernetes (powerful but complex): you get zero-downtime rolling deployments, automatic HTTPS, cross-machine service discovery, and load balancing - with no central control plane to maintain and roughly 150 MB RAM overhead per node.

> **Links:** [GitHub](https://github.com/psviderski/uncloud) · [Documentation](https://uncloud.run/docs/) · [Discord](https://discord.gg/eR35KQJhPu) · [Community Recipes](https://github.com/psviderski/uncloud-recipes)

---

## Follow a Tutorial

Tutorials are guided paths with concrete tasks and step-by-step instructions.

<!-- prettier-ignore-start -->
::grid
---
items:
  - content: tutorials.uncloud-create-cluster-ebebf72b
  - content: tutorials.uncloud-deploy-django-app-7a378bc3
---
::
<!-- prettier-ignore-end -->

---

## Start in a Playground

Playgrounds are open-ended environments with a pre-configured Uncloud cluster. Use them to experiment freely without any local setup.

<!-- prettier-ignore-start -->
::grid
---
items:
  - playground: playgrounds.uncloud-cluster-64523f7c
---
::
<!-- prettier-ignore-end -->

The playground has two server nodes (`server-1`, `server-2`) and a `dev-machine` control node with the `uc` CLI ready to use:

```sh
# List all machines in the cluster
uc machine ls

# Run an Nginx container across the cluster
uc run nginx:latest --name web --publish app.example.com:80/http

# Scale the service to 2 replicas (one per server)
uc scale web 2
```

---

## Suggested Learning Path

1. Complete the **[Set Up a New Cluster](https://labs.iximiuz.com/tutorials/uncloud-create-cluster-ebebf72b)** tutorial to learn how to initialise a cluster from scratch, add machines, and deploy your first service.
2. Complete the **[Deploy a Django App](https://labs.iximiuz.com/tutorials/uncloud-deploy-django-app-7a378bc3)** tutorial to see how to ship a Python web application directly from source code — no external container registry required.
3. Open the **[Uncloud Cluster playground](https://labs.iximiuz.com/playgrounds/uncloud-cluster-64523f7c)** to experiment freely on a live two-node cluster with the `uc` CLI.
