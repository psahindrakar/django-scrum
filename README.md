# django-scrum
A sample project to start learning RESTful server development with python-django. The project is configured using docker for 
ease for development and deployment.

# Setting up django with docker

Steps followed to setup a project
1. Created a folder structure. Structure is as follows - 
    - documents: To keep any project related document, e.g. database design diagram, restapi design, project SRS etc.
    - nginx: nginx docker configuration files are stored in this folder. The configuration files are very standard. So just copy them as is
    if needs to be reused.  
    - source: It has source code of the project and docker config file. The container created from this docker runs python-django code. 
2. In source folder, the docker file should have following content -
    ```
    FROM python:3.5-onbuild
    ```
3. In source folder, there should be `requiremets.txt` file. The file is used by `pip` tool which is used for dependency managmenet of a project.
In `requiremets.txt` the required frameworks and libraries should be referred along with the required version. The tool fetches and installs them 
on the docker. To start with django project, following are the requirements - 
```
# Framework
Django==1.10

# Libs 
djangorestframework==3.5.3
django-filter==1.0.1
Markdown==2.6.7

# Server
gunicorn==19.6.0
```
We will be using django as a web framework. Django rest framework is a python library which helps building REST apis. By default django provides a server
for running web applications. However, it is not supposed to be used for production environment. It is for development purpose only. For production, we 
use Gunicorn, which is a production ready, battle tested python WSGI HTTP Server for UNIX.
4. Nginx is used for load balancing and as a front web server. Gunicorn is hosts the django server. There are two separate dockers. These dockers are
bound together by docker compose tool. The docker compose requires `docker-compose.yml` file which has contents as follows -
```
version: '2'

services:

    scrum_web:
        build: ./source
        container_name: scrum_web 
        # restart: always
        expose:
            - "8000"
        volumes:
            - ./source:/usr/src/app
        env_file: .env
        environment:
            DEBUG: 'true'
        command: /usr/local/bin/gunicorn scrum.wsgi -w 2 -b :8000   # Gunicorn command should be run from where manage.py of django is located.
                                                                    # Creates 2 worker processes and listens at 8000 port

    scrum_nginx:
        build: ./nginx/
        container_name: scrum_nginx
        # restart: always
        ports:
            - "9000:80"                                             # Host port 9000 is mapped on to container's port 80
        volumes:
            - /www/static
        links:
        - scrum_web:web
```
With this the source directory is mounted at /usr/src/app path in the container.
5. The `.env` file used to pass environment variables to scrum_web container. The `.env` needs to be created next to `docker-compose.yml` file. Initially 
it will be empty. 
6. Now that the ground work is setup, run `docker-compose build` to build the docker mentioned in `docker-compose.yml`.
7. Initally when dockers are built, there is no project structure inside it. To create the same, we need to take control of scrum_web docker. Using 
following command scrum_web containers shell can be accessed. 
`docker-compose run scrum_web /bin/sh`. The shell of the container opens. 
8. Using `requirement.txt` file we had mentioned which django version was required inside the docker. It can be tested using following command - 
`django-admin.py --version`. It should print 1.10 as version of django. 
9. Create a project with following command `django-admin.py startproject scrum .`. Make sure to add `.` at the end to instruct that the project should
be created in the current folder and not create a new folder for it. 
10. The source folder has `manage.py`. Run following command to create a app in the project `python manage.py startapp board`
11. Exit from shell connected to scrum_web container with `exit` on terminal
12. To test if everything is configured correctly, build docker composer by `docker-composer build` and execute with `docker-composer up`
13. In browser check `localhost:9000` for running django server. A web page with success message should be displayed.




