# **STUDENT ACCOMODATION PIPELINE**
## **About This Repository**
- This is a pipeline which extracts data from files loads to database, queries database and unloads resuslts as json format.
## **PROJECT STRUCTURE**
![Folder Structure](images/folder_structure.png)
## **INSTALLATION**
- Install a code editor/IDE (VS code **RECOMMENDED❗**)
- Install python to your local machine, if it does not have python by defualt(**PYTHON 3.10.0 GOING UP**).
- After cloning the repository to your local machine, create a virtual enviroment.
- Install all dependencies listed in the requirements.txt file.
- Install Docker desktop to your local machine.
- Install chocolately, if it not supported by defualt in your machine.
- install make(to run commands in the make file, so your systems understand them).
- (Optional) Install PgAdmin to interacte with your databse visually.
## **DEVELOPMENT**
- **Download or Copy docker-compose.yml file**:
   - **.env file with credentials will be sent to user/developer privately .**
   - **Open docker-compose.yml with VS code, and make sure they are in the same directory with the .env file .**
   - **In the terminal of the same directory run the following commands:**
   - **docker compose up -d**(To start the containers/ create them if not exist)
   - **docker logs (container_name)**(This attaches the logs of the containers on the terminal to see the output)
   - **docker compose run --rm (service_name) bash**(This lets you get inside a conatiner and interact with it, run commands, check filesystem)
   - **docker compose run --rm etl bash**(This will be the exact command you will run to interact specifically with the etl container)
   - AFTER THE COMMAND ABOVE **cd into src folder and run (python main.py)**, this will start the console app
   - **etl- container or any temp containers created using the image under etl service have the same filesystem as the Project Structure**(app is the root folder instead of STUDENT_ACCOMODATION_PIPELINE)
   - **MAKE SURE DOCKER DESKTOP IS RUNNING BEFORE ANY STEP ABOVE!**
## **USAGE**
![Console App](images/pipeline_app.png)
## **ARCHITECTURE**
![Architecture](images/architecture.png)

