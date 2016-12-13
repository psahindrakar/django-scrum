# django-scrum
A sample project to start learning RESTful server development with python-django. The project is configured using docker for 
ease for development and deployment.

In this document, tried to capture as much details as possible as to how the final result is achieved. A scrum board building example is considered here. 
The details about the example is in the document folder. It is example from a blog. Though the example is for django 2.x, in this repo it has been updated for 
django 3.x.

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

# Configuring Mysql
Django by default comes configured to work with sqlite database. For bigger project mysqlite is not an option. In this case, we want to use mysql with 
django. The `docker-compose.yml` is updated as follows to include mysql and mysql data container -
```
version: '2'

services:

    scrum_web:
        build: ./source
        container_name: scrum_web 
        expose:
            - "8000"
        depends_on:
            - scrum_mysql
            - scrum_mysql_data
        links:
            - scrum_mysql:mysql
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
        ports:
            - "9000:80"                                             # Host port 9000 is mapped on to container's port 80
        volumes:
            - /www/static
        links:
            - scrum_web:web

    scrum_mysql_data:
        image: mysql:5.7
        container_name: scrum_mysql_data
        entrypoint: /bin/bash


    scrum_mysql:
        image: mysql:5.7
        container_name: scrum_mysql
        depends_on:
            - scrum_mysql_data
        volumes_from:
            - scrum_mysql_data
        environment:
            MYSQL_DATABASE: scrum_app
            MYSQL_USER: scrum_master
            MYSQL_PASSWORD: scrum@2016!
            MYSQL_ROOT_PASSWORD: Selenite#1
```
and the `.env` file is updated with environment variables which are inturn passed to scrum_web container. 
```
# Add Environment Variables

SECRET_KEY=twydj8^_vdjw$ww7@^6e542v_rzab+qy*57qwjbf63khz2fc2)
DB_NAME=scrum_app
DB_USER=scrum_master
DB_PASS=scrum@2016!
DB_SERVICE=mysql
DB_PORT=3306
```
The `/source/scrum/settings.py` file is updated to use mysql and environment variable passed from `.env` file. Take a look in the file for more details.


# Migration and setting up superuser
After following the reference tutorial from documents folder, the scrum and task models are created in `/source/board/models.py`. As per the model the 
database needs to be udpated. To do so the migrations need to created and applied on the database. It can be done as follows - 
1. Connect to the scrum_web container using following command - 
```
docker exec -ti scrum_web /bin/bash
``` 
It start the container's bash terminal. 
2. Run following commands on the terminal to create and apply migrations -
```
python manage.py makemigrations board
python manage.py migrate
```
3. To create a superuser run following command and follow terminal instructions -
```
python manage.py createsuperuser
```

# Installing collectstatic
When trying out apis in browser in debug mode, django provides a facility for api testing. The views generated for these testing require various static
file to make the pages look good. Django provides a package called `collectstatic` which when installed in projects brings all the required static files
to make the test page look good. Add following to ;ine `settings.py`. It locates the static folder for the project. It is the location where all the
static files will be installed. 

```
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```
After that from base dir, execute following command to bring static resources.  
```
python manage.py collectstatic
```
As we are using nginx as a loadbalancer and static file distributor, it should be made sure that the nginx setting are configured correctly to register the 
static folder. In nginx server configuration, the static location should be configured as follows. 
```
location /static {
    alias /usr/src/app/static;
}
```

#Doing Something Periodic
In most of the projects, there are some periodic tasks e.g. sending email for pending payments, sending a remider sms of service expiry etc. Considering
one of the typical cases for this project. In the content of sprint project, we can decide to send an email reminder to assignee about the task which will
expire on the day. 

The idea will be send an email at 7am every morning with a list of tasks which are going to expire on that very day. With that email user will be aware that
those tasks needs to be completed on the same day. 

In order to do that, we are going to use celery. Following line will be added to `requirements.txt` file. 
```
celery==4.0.1                       # For task queue and cronjobs
```
As there are changes in `requirements.txt` file, the `scrum_web` container needs to be reinitialised to prepare as per new changes. Run
'docker-compose build' for the same. To maintain all the celery tasks a separate app is created called as `services` using following command 
```
docker-compose run scrum_web /bin/bash
python manage.py startapp services
exit
```
After that new folder are created in the project directoty. The folder access rights needs to be updated by `chmod +666 ./source/*`.
Celerry tasks is created following the instruction from [this link](https://realpython.com/blog/python/asynchronous-tasks-with-django-and-celery/)

Docker configuration for celery and django is introduced in [this post](https://www.syncano.io/blog/configuring-running-django-celery-docker-containers-pt-1/)










