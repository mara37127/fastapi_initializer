# Fastapi intializer
This is a fastapi project initializer that includes some basic needs.
You have here some boilerplate codes so you can jump directly to the main purpose of your application.

## Modules
In this project you have these ready to use modules:
   - ### logging
    The logging is configured and a new logfile is used every 24 hours
   - ### authentication handling
    A jwt pair token (access_token & refesh_token) is generated once the user is correctly connected.
   - ### database connexion
    A connexion to a mySQL database is already set up .
    You just have to specify the informations of your database
   - ### docker container
    You can easily deploy your application using containers with the configuration already done.


## Usage
Clone this project and do these steps to get started:
 - #### activate the environment
    ```bash
    source bin/activate
    ```
 - #### Specify database informations in the src/config/database.py file.
 - #### Go to src/ folder and Run the application with this command :
    ```bash
    uvicorn main:app --reload --port=8080
    ```
 - #### Using containers
 In your src/config/database.py file you must choose the database connexion for containers
 Then create an image of your application with this command in the application root folder:
 ```bash
    docker build -t your_image_name:version .
 ```
 You must specify an image name and a version and don't forget the "." that indicate the location of the Dockerfile.
 Then go to the docker-compose.yml file and modify the line #19 with your image name and version.
 If these steps are done correctly, launch your application with this command:
 ```bash
    docker-compose up -d
 ```

 # Enjoy !!!


