# Backend-users-proyecto

## Creating a virtual environment in Windows
1. Open a command prompt and navigate to the directory where you want to create the virtual environment.
2. Type `python -m venv .venv` and press Enter.
3. To activate the virtual environment, type `.venv\Scripts\activate` and press Enter.
4. You can now install packages and run your Python code within the virtual environment.
5. To install requirements, type `python -m pip install -r requirements.txt`
6. To deactivate the virtual enviroment, type `deactivate`
## Create image users
1. Create image users: `docker build -t users_app .`
2. Create and run container: `docker run -d -p 3001:3001 -e DATABASE_URL=postgresql://postgres:admin@host.docker.internal:5432/postgres users_app`