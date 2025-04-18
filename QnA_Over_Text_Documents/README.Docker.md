# Docker


References: 
- [Docker Website](https://docs.docker.com/get-started/)
- [Docker's Python guide](https://docs.docker.com/language/python/)

- Easy to transport: Package your application and its dependencies into a single unit called container. Saves you from the hassle of sharing your source-code and creating the same enviorment on testing/deployment machine.
- Portable: Docker containers can run on virtually any machine, regardless of the underlying OS or hardware.
- Scaling up and tearing down is easy: You can easily scale your application up or down by adding or removing containers. 
- Lightweight and fast: viable and cost effective alternative to hypervisor-based virtual machines. Uses less resources and starts up faster than traditional VMs.
- Isolation: Each container runs in its own isolated environment, which means that you can run multiple containers on the same machine without them interfering with each other.
- Security: Docker containers are more secure than traditional VMs because they run in their own isolated environment. This means that if one container is compromised, the others are not affected.
- Version control: Docker allows you to version control your containers, which means that you can easily roll back to a previous version if something goes wrong.
- Reproducibility: Docker containers are reproducible, which means that you can easily recreate the same environment on different machines. This is especially useful for testing and deployment.
- Collaboration: Docker makes it easy to share your application and its dependencies with other developers. This is especially useful for open source projects, where multiple developers need to work on the same codebase.
- CI/CD: Docker can be used in continuous integration and continuous deployment (CI/CD) pipelines, which means that you can automate the process of building, testing, and deploying your application. This is especially useful for large projects with multiple developers.

### Docker Architecture
 - Client - The Docker client is the primary way that users interact with Docker. It provides a command-line interface (CLI) for managing Docker containers, images, and networks.
 - Host - Builds, run and distributes the containers. 
 - Registry - A registry is a repository for storing Docker images. Docker Hub is the default public registry, but you can also set up your own private registry.
   - Docker Hub, ECR (Elastic Container Registry), ACR, GCR. 
   - Private registry - can run on your local system or even in a organization. 
   - Registry and Repository are different: i.e. Repository can be considerd as a folder in the registry, that should store the related images.
 - Docker Compose - Another client, lets you work with multiple containers at once. It is a tool for defining and running multi-container Docker applications. You define your application stack in a YAML file called docker-compose.yml, and then use the docker-compose command to manage the entire stack.
 - Docker Objects:
   - Image -  An image is a read-only template with instructions for creating a Docker container. Includes all files, binaries, libraries, and configurations to run a container.
     - Images are immutable, meaning that once they are created, they cannot be changed. If you need to make changes to an image, you must create a new image based on the original.
     - Container images are composed of layers. Each layer represents a set of file changes or instructions. When you create a new image, Docker creates a new layer on top of the existing layers. i.e. 
       - Base image - The base image is the starting point for your Docker image. It can be a minimal operating system, a programming language runtime, or any other software that you need to run your application.
       - Intermediate image - The intermediate image is created when you build your Docker image. It contains the changes that you made to the base image, such as installing software or copying files.
       - Final image - The final image is the result of the build process. It contains all of the layers that were created during the build process, including the base image and any intermediate images.
   - Container - A container is a runnable instance of an image. It is a lightweight, standalone, and executable package that includes everything needed to run a piece of software, including the code, runtime, libraries, and system tools.
     - Self-contained (has everything in it to run on its own), portable, isolated(minimal influence on host or on other containers), and independent(independently managed, deleting one doesnot affect other containsers).
   - Volume - 
   - Network
   - Dockerfile
   
You need to start *Docker Desktop* a host gui or *Docker Daemon* a command line interface for docker engine on linux. Then only you can run the docker commands.
To start docker engine on linux, use the command `sudo systemctl start docker` or `sudo service docker start`. 

### Important things to remember 
Following issues raised and resolved while using docker
* login before runing the docker-compose command. Use docker login -u vsscorvc 
* Never put comment in the same line that of code in the Dockerfile. It will cause the build to fail. Use separate line for comments and codes.
* For CMD, use the form ["executable", "param1", "param2"] and in double quotes.
* Not sure why, but streamlit app is only able to run on 8501 port. If you use other ports its not working. Use -p 8501:8501 to publish the port. And if the port is already in use, check the process by `lsof -i :8501` and kill the process using `kill -9 <PID>`.
* When running the app inside docker, use the `host.docker.internal:PORT_NUMBER` as the host name to connect to the localhost of the host machine. i.e. if you want to connect to ollama server running on the host machine, use host.docker.internal:11434 as the host name in the url.

### Docker CLI
 - `docker --help` to see the list of commands
 - `docker ps --help` to see the list of options for the ps command

### Docker Init
    - `docker init` to create a new Docker project. This will create a new directory with the necessary files and folders for your Docker project.
        - Creates a Dockerfile, .dockerignore, and a README file in the current directory.
    - `docker init --compose` to create a new Docker Compose project. This will create a new directory with the necessary files and folders for your Docker Compose project.

### (Write a Dockerfile)[https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/]
    - Dockerfile starts with a FROM instruction, which specifies the base image to use for your Docker image. The base image can be any valid Docker image, including an official image from Docker Hub or a custom image that you have created.
    - The FROM instruction is followed by a series of other instructions that define the steps to build your Docker image. These instructions can include RUN, COPY, ADD, ENV, EXPOSE, CMD, and ENTRYPOINT.
    - The WORKDIR instruction is used to set the working directory for the container. This can be used to specify the directory where the application code is located or where the application will run.
    - The RUN instruction is used to execute a command in the container during the build process. This can be used to install software, copy files, or perform any other necessary tasks.
    - The COPY instruction is used to copy files from the host machine to the container. This can be used to copy application code, configuration files, or any other necessary files.
    - The ADD instruction is similar to the COPY instruction, but it can also be used to extract files from a tar archive or download files from a URL.
    - The ENV instruction is used to set environment variables in the container. This can be used to configure the application or set default values for the container.
    - The EXPOSE instruction is used to specify the ports that the container will listen on. This can be used to expose the application to the outside world.
    - The CMD instruction is used to specify the command that will be run when the container is started. This can be used to start the application or run any other necessary tasks.
    - The ENTRYPOINT instruction is similar to the CMD instruction, but it is used to specify the command that will be run when the container is started. This can be used to start the application or run any other necessary tasks.
    - The VOLUME instruction is used to create a mount point for a volume in the container. This can be used to store data that needs to persist across container restarts or to share data between containers.
    - The ARG instruction is used to define a variable that can be passed to the Docker build process. This can be used to customize the build process or to pass in configuration values.

### Build Image using a Dockerfile
 - First, build your image, e.g.: `docker build -t image_name_in_lowercase .`. 
   - Here, -t is used to tag the image with a name, you can also usee --tag. '.' indicates the current directory as the build context, where the Dockerfile is located.
 - If development and tagert deployment machine has different OS and CPU architecture then use 
   - `docker build --platform=linux/amd64 -t image_name_in_lowercase .` 
   - or `docker buildx build --platform linux/x86_64 --tag image_name_in_lowercase .` Both commmands are same.
     - docker build seems a shorthand for docker buildx build.
 - To list all images in the repository: `docker images` or `docker image ls`
 - To remove an image: `docker rmi image_name`
 - To share the image with others in a file formate use, `docker save -o image_name.tar image_name`
   - To load the image from a file: `docker load -i image_name.tar`
   - To load the image from a file and tag it: `docker load -i image_name.tar`
   

When you run the docker build command to create a new image, Docker executes each instruction in your Dockerfile, creating a layer for each command and 
in the order specified. For each instruction, Docker checks whether it can reuse the instruction from a previous build. If it finds that you've already
executed a similar instruction before, Docker doesn't need to redo it. Instead, it’ll use the cached result. This way, your build process becomes faster
and more efficient, saving you valuable time and resources.    

### Run the image
#### Publishing ports
 - -p or --publish flag is used to indicate that requests on host's port shoud be forwarded to the container's port.
   - `docker run -d -p HOST_PORT:CONTAINER_PORT image_name`
 - or, Let docker pick the host port for the container.
 - `docker run -d -p CONTAINER_PORT image_name`
 - or, use -P or --publish-all flag to publish all exposed ports to random ports on the host.
   - `docker run -d -P image_name`ls
**-d flag for detach mode
   

#### Persistent Storage
All the changes made to the container's filesystem are lost when the container is stopped or removed. To store the data persistently, 
you need to use a volumne is mount on the containers path.

#### Sharing local files with containers.
If you want that container can read and write to the local filesystem, you need to mount a local directory to the container's path.
  - Use -v or --volume flag to mount a local directory to the container's path.
  - `docker run -d -v /path/on/host:/path/in/container image_name`
  - or, use --mount flag to mount a local directory to the container's path.
  - `docker run -d --mount type=bind,source=/path/on/host,target=/path/in/container image_name`

### Stop and delete the container
- To list all running containers: `docker ps`
- To stop a container: `docker stop container_name`
- To remove a container: `docker rm container_name`

### Connecting to localhost of host from docker.
Network stack of the host machine and docker is different due to being different entity.
To connect to the localhost of the host machine from the docker container, there are multiple ways.
one way is to use host.docker.internal as dns name instead of localhost in url.
https://www.youtube.com/watch?v=lJAhaiDuAYc


## Deploy the docker container on the remote machine
- Install docker engine on the remote machine. (https://docs.docker.com/engine/install/)
docker run -p 8083:8505 -v /mnt/sasdshare/vivek/LLM/llm_apps/QnA_Over_Text_Documents/uploaded_pdfs:/app/data streamlit_image

## Run ollama on docker
  - Pulls the image from docker registry and creates a container on the host system 
  - `docker run -d --name ollama -p 11434:11434 -v ollama_storage:/root/.ollama  ollama/ollama:latest` 
  - Adding OLLAMA_HOST env variable with 0.0.0.0 value, any IP address in home network can access it.
  - `OLLAMA_HOST=0.0.0.0 docker run -d --name ollama -p 11434:11434 -v ollama_storage:/root/.ollama  ollama/ollama:latest`
  - Runs the model in iteractive mode to chat with model and attaches the terminal to the container.
  - `docker exec -it containe_name ollama run deepseek-r1:1.5b`. here container_name='ollama'

## Docker Compose
Docker Compose is a tool for defining and running multi-container applications. It is the key to unlocking a streamlined and efficient development and deployment experience.

Compose simplifies the control of your entire application stack, making it easy to manage services, networks, and volumes in a single, comprehensible YAML configuration file. Then, with a single command, you create and start all the services from your configuration file.

Compose works in all environments; production, staging, development, testing, as well as CI workflows. It also has commands for managing the whole lifecycle of your application:

- write a compose.yaml as in this example mentioning ollama and streamlit web app details.
- `docker compose up -d` to start the application. (This will run the containers in detached mode)
- You might need to download the models for the ollama (docker image).
  - `docker exec -it container_name ollama pull deepseek-r1:1.5b`

** But it seems ollama is not able to get GPU spport inside the docker container..Either you run ollama on the host machine or run it along side docker desktop.
** Although we can get nvidia GPU support for ollama in docker container for linux operating system.
