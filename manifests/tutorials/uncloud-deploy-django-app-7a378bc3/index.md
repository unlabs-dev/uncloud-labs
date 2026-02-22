---
kind: tutorial

title: "Uncloud: How to Deploy a Django Web Application"

description: |
  Learn how to quickly deploy your Python Django-based application to a remote Linux server under your control. This hands-on tutorial covers preparing and packaging a Django application from source code on your local machine and then deploying it to an Uncloud-managed machine, along with the networking ingress configuration and without using any external image registry.

categories:
  - linux
  - containers

tagz:
  - uncloud

createdAt: 2026-01-11
updatedAt: 2026-01-11

cover: __static__/cover.png

playground:
  name: uncloud-django-app-2b759193
  tabs:
    - machine: dev-machine
    - machine: server-1
    - machine: server-2
    - kind: http-port
      name: Application
      number: 80
      hostRewrite: issue-tracker.internal
      machine: server-1
---

## Introduction

In this hands-on tutorial, you'll learn how to deploy a Django web application from source code to a remote Linux server using Uncloud.

::remark-box
💡 **What is Uncloud?** [Uncloud](https://uncloud.run/docs/) is a lightweight clustering and container orchestration tool that lets you deploy and manage web applications across cloud VMs and bare metal servers. It creates a secure [WireGuard](https://www.wireguard.com/) mesh network between Docker hosts and provides automatic service discovery, load balancing, and HTTPS ingress — all without the complexity of Kubernetes.
::

**Prerequisites**

Before starting this tutorial, you should have:

- A basic understanding of [Docker](https://www.docker.com/) and containers. There are great tutorials and courses available on iximiuz Labs (the very same platform you're using now), for example check out the [Docker skill path](https://labs.iximiuz.com/skill-paths/docker-101-run-and-manage-containers) if you want to brush up on fundamentals.
- Familiarity with [Python](https://www.python.org/) and the [Django](https://www.djangoproject.com/) web framework.
- A basic understanding of Uncloud and how an Uncloud cluster functions. If you haven't completed the initial Uncloud tutorial ([How to Create an Uncloud Cluster](../uncloud-create-cluster-ebebf72b/)), we recommend you to start there.

**What You'll Learn**

By the end of this tutorial, you'll be able to:

1. Dockerize a Django application by creating a Dockerfile
2. Create a Compose file for deployment configuration
3. Build and deploy your application using Uncloud
4. Access your deployed application through the web browser
5. Check the application logs

Let's get started!

---

## Tutorial Environment

It is highly encouraged to take advantage of the interactive features of the [iximiuz Labs platform](https://labs.iximiuz.com/about) and follow the tutorial by executing the commands in the interactive environment.

To get started, click the "Start Tutorial" button located under the table of contents on the left side of the screen (like, do it right now!). After a few seconds, you'll see a terminal on the right side of your screen.

In this tutorial, you have access to the following machines:

- :tab{text='dev-machine' machine='dev-machine'} - the control-only environment where you'll prepare the application and run Uncloud CLI commands. Think of it as your developer machine that you'll use to control the cluster remotely.
- :tab{text='server-1' machine='server-1'}, :tab{text='server-2' machine='server-2'} - two Ubuntu machines that are already part of an initialized Uncloud cluster where your application will be deployed.

The Django application source code is already available on :tab{text='dev-machine' machine='dev-machine'} in the `~/app` directory. This is a sample issue tracking application built with Django that we'll be using as an example.

## Preparing Your Django Application

### Understanding the Application Structure

The Django application in this tutorial is a simple issue tracker. Let's take a look at its structure:

```sh
cd ~/app
tree -L 2
```

You should see a typical Django project structure:

```
.
├── README.md
├── issuetracker        # Main project directory with core settings and routing configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py           # Django management script
├── requirements.txt    # File listing Python dependencies
└── tracker             # Application directory with models, views, and templates
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── migrations
    ├── models.py
    ├── static
    ├── templates
    ├── tests.py
    ├── urls.py
    └── views.py
```

### Dockerizing the Application

To deploy this application with Uncloud, we need to containerize it first. This means creating a `Dockerfile` that defines how to build a container image for our application.

Create a `Dockerfile` at `~/app/Dockerfile` with the following content:

```dockerfile
### FIXME: copy from Dockerfile
```

This Dockerfile:

1. Uses Python 3.12 as the base image
2. Sets up the working directory
3. Installs Python dependencies from `requirements.txt`
4. Copies the application code into the container
5. Collects Django static files
6. Exposes port 8000
7. Runs the Django development server when the container starts

::remark-box
📝 **Production Note**: In a production environment, you would typically use a production-ready server like [Gunicorn](https://gunicorn.org/) (WSGI) or [Uvicorn](https://uvicorn.dev/) (ASGI) instead of Django's development server. For this tutorial, we'll keep it simple with the built-in Django's development server.
::

::remark-box
📝 **Dependency management**: We're using "plain" `pip` and `requirements.txt` file to manage Python dependencies in this tutorial, mostly to not shift away the focus from Uncloud-related concepts. For modern alternatives we recommended to look at [uv](https://docs.astral.sh/uv/) as a universal Python package and environment manager.
::

### Testing the Docker Build

Before deploying to Uncloud, let's verify that our Docker image builds successfully:

```sh
cd ~/app
docker build -t django-app:test .
```

You should see Docker building the image layer by layer. If the build completes successfully, you're ready to deploy!

You can verify the image was created:

```bash
docker images | grep django-app
```

<!-- prettier-ignore-start -->
::image-box
---
:src: __static__/docker-build-output.png
:alt: 'Docker Build Output'
:max-width: 700px
---

_Successful Docker build showing all layers._
::
<!-- prettier-ignore-end -->

---

## Deploying to Uncloud Cluster

Now that we have a Dockerized application, let's deploy it to your Uncloud cluster.

### Creating a Compose File

Uncloud uses the [Compose Specification](https://compose-spec.io/) to define deployment configurations. Create a `compose.yaml` file in your application directory:

```yaml
services:
  web:
    # Build the image from the current directory
    build: .

    # Expose the application on a public URL
    # Replace 'app.example.com' with your actual domain
    x-ports:
      - app.example.com:8000/https

    # Set environment variables
    environment:
      DJANGO_SETTINGS_MODULE: issuetracker.settings
      PYTHONUNBUFFERED: 1

    # Restart policy
    restart: unless-stopped
```

Let's break down what this configuration does:

- **`build: .`** - Tells Uncloud to build a container image from the Dockerfile in the current directory
- **`x-ports`** - Uncloud-specific extension that configures ingress routing. This publishes your application on the specified domain with HTTPS
- **`environment`** - Sets environment variables inside the container
- **`restart: unless-stopped`** - Ensures the container automatically restarts if it crashes

::remark-box
**About the domain configuration**: In a real-world scenario, you would replace `app.example.com` with your actual domain name. For this tutorial environment in iximiuz Labs, we'll use `issue-tracker.internal` as configured in the playground settings, which will be accessible via the :tab{text='Application' name='Application'} tab.
::

### Building and Deploying with `uc deploy`

Now for the exciting part - deploying your application! Navigate to your application directory and run:

```sh
cd ~/app
uc deploy
```

This single command will:

1. **Build the image** - Uses your local Docker to build the image from the Dockerfile
2. **Tag the image** - Automatically tags it with a Git-based version (or timestamp if not a Git repo)
3. **Push to cluster** - Transfers the image directly to your cluster machines using [unregistry](https://github.com/psviderski/unregistry), efficiently sending only the layers that don't already exist
4. **Plan deployment** - Shows you what will change and asks for confirmation
5. **Deploy containers** - Creates and starts containers using zero-downtime rolling updates

You'll see output similar to:

```
Building service 'web'...
[+] Building 45.2s (10/10) FINISHED
Pushing image to cluster machines...
Planning deployment...

Changes:
  + Create service 'web' with 1 replica

Proceed? [y/N]: y

Deploying services...
✓ Service 'web' deployed successfully
```

::remark-box
💡 [`uc deploy`](https://uncloud.run/docs/cli-reference/uc_deploy) is a powerful command that handles the entire deployment workflow. Check out the [CLI reference](https://uncloud.run/docs/cli-reference/uc_deploy) for all available options and flags.
::

### Understanding the Deployment Process

What just happened under the hood?

1. **Local Build**: Docker built your image using the Dockerfile, creating layers for each instruction
2. **Direct Push**: Instead of pushing to an external registry (like Docker Hub), Uncloud pushed the image directly to your cluster machines
3. **No Registry Required**: This is a key feature of Uncloud - you don't need to set up or pay for a container registry
4. **Layer Optimization**: Only the layers that don't exist on the target machines were transferred, making subsequent deployments much faster

<!-- prettier-ignore-start -->
::image-box
---
:src: __static__/deployment-flow.png
:alt: 'Uncloud Deployment Flow'
:max-width: 800px
---

_Visual representation of the `uc deploy` workflow._
::
<!-- prettier-ignore-end -->

### Verifying the Deployment

Check that your service is running:

```sh
uc ls
```

You should see output similar to:

```
NAME    MODE         REPLICAS   IMAGE                   ENDPOINTS
caddy   global       2          caddy:2.10.2
web     replicated   1          django-app:...          http://issue-tracker.internal → :8000
```

For more detailed information about the service:

```sh
uc inspect web
```

You should see output showing the container details:

```
Service ID: a1b2c3d4e5f6
Name:       web
Mode:       replicated
CONTAINER ID   IMAGE            CREATED          STATUS                   IP ADDRESS   MACHINE
abc123def456   django-app:...   30 seconds ago   Up 30 seconds (healthy)  10.210.0.3   server-1
```

To view the logs from your Django application:

```sh
uc logs web
```

::remark-box
💡 [`uc ls`](https://uncloud.run/docs/cli-reference/uc_ls) is a shortcut for the [`uc service ls`](https://uncloud.run/docs/cli-reference/uc_service_ls) command. Check all [`uc service`](https://uncloud.run/docs/cli-reference/uc_service) commands for available service operations.
::

---

## Accessing Your Application

### In the iximiuz Labs Environment

In this tutorial environment, you can access your deployed application using the built-in browser. Click on the :tab{text='Application' name='Application'} tab at the top of your screen.

You should see the Django issue tracker homepage! Try creating a new issue to verify everything is working correctly.

<!-- prettier-ignore-start -->
::image-box
---
:src: __static__/django-app-running.png
:alt: 'Running Django Application'
:max-width: 800px
---

_The deployed Django issue tracker application._
::
<!-- prettier-ignore-end -->

You can also reach the service from the :tab{text='dev-machine' machine='dev-machine'} terminal. In that case, make sure to specify the correct "Host" header:

```sh
# You can target ANY server of the cluster (server-1 or server-2)
curl --header 'Host: issue-tracker.internal' server-1
```

### In a Real-World Deployment

In a production environment with Uncloud:

1. **Domain Configuration**: You would configure your domain's DNS to point to your Uncloud cluster
2. **Automatic TLS**: Uncloud automatically provisions TLS certificates using Let's Encrypt for your configured domains
3. **HTTPS by Default**: Your application would be immediately accessible via HTTPS at the domain you specified in the `x-ports` configuration
4. **Ingress Management**: Uncloud handles all the ingress routing, SSL termination, and load balancing for you

No need to manually configure reverse proxies, SSL certificates, or load balancers!

::remark-box
📚 **Learn More**: For detailed information about publishing services to the internet with custom domains and automatic TLS, check out the [Publishing Services](https://uncloud.run/docs/concepts/ingress/publishing-services) documentation.
::

---

## Making Updates

One of the powerful features of Uncloud is how easy it is to deploy updates. Let's say you made changes to your application code. Simply run:

```sh
uc deploy
```

Uncloud will:

1. Detect the changes
2. Rebuild the image (with layer caching for speed)
3. Push only the changed layers
4. Perform a zero-downtime rolling update

Your new version will be deployed without any service interruption!

### Deploying Configuration Changes Only

If you only changed the `compose.yaml` file (for example, updated environment variables) without modifying the application code, you can deploy just the configuration:

```sh
uc deploy --no-build
```

This skips the build step and only updates the service configuration.

<!-- prettier-ignore-start -->
::remark-box
---
kind: warning
---

⚠️ **Image Tag Considerations**: When using dynamic image tags based on Git state (which is the default), deploying with `--no-build` may fail if the tag has changed. See [Deploy configuration changes only](https://uncloud.run/docs/guides/deployments/deploy-app/#deploy-configuration-changes-only) in the official docs for best practices.
::
<!-- prettier-ignore-end -->

---

## Next Steps

Congratulations! You've successfully deployed a Django application to Uncloud. Here are some things you can explore next:

1. **Add a Database Service**: Extend your `compose.yaml` to include a PostgreSQL database service instead of SQLite
2. **Environment Variables**: Use environment variables for sensitive configuration like database passwords
3. **Multiple Services**: Deploy additional services like Redis for caching or Celery for background tasks
4. **Production Configuration**: Replace the development server with Gunicorn and add Nginx for serving static files
5. **Scale Your Service**: Try scaling your web service to multiple replicas with [`uc scale`](https://uncloud.run/docs/cli-reference/uc_scale): `uc scale web 2`

### Additional Resources

- [Uncloud Documentation](https://uncloud.run/docs) - Complete guide to all Uncloud features
- [Compose Specification](https://compose-spec.io/) - Learn about all available Compose file options
- [Deploy to Specific Machines](https://uncloud.run/docs/guides/deployments/deploy-specific-machines) - Control where services are deployed
- [Compose Support Matrix](https://uncloud.run/docs/compose-file-reference/support-matrix) - Supported Compose features in Uncloud

Happy deploying! 🚀

## Questions or Feedback?

Run into any issues or have ideas to improve this tutorial? Open an issue or contribute a fix on GitHub: https://github.com/tonyo/uncloud-labs/
