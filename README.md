# Database Schema

![database_schema](docs/database_schema.png)

For more details on the schema [see here](docs/schema.md). 

# Development Environment Setup
### 1. Clone the Repository

```Bash
$ git clone https://github.com/s-bose7/csv-uploader.git
```
### 2. Project Setup

Navigate to the project directory:
```bash
$ cd csv-uploader
```

Create and activate a virtual environment using your preferred tool (e.g., venv).
```bash
$ python3 -m venv gp-db-uploader
$ source gp-db-uploader/bin/activate # unix
```  
Install dependencies listed in requirements.txt:
```bash
$ pip install -r requirements.txt
```
Create a data directory to store your CSV files for upload.
```bash
$ mkdir data
```
Create the migration environment:
```bash
$ alembic init migrations # This will create a dir migrations in project root with an alembic.ini file
```
### 3. Environment Variables (.env)
Create a .env file in the project root for environment variables:
```bash
$ touch .env
```
Populate the .env file with the following variables, replacing the placeholders with your actual credentials:
```bash
DEV_DB_USER=postgres
DEV_DB_PASSWORD=your_development_password
DEV_DB_HOST=localhost
DEV_DB_PORT=5432
DEV_DB_NAME=your_development_database_name

PROD_DB_USER=your_production_username
PROD_DB_PASSWORD=your_production_password
PROD_DB_HOST=your_production_database_host
PROD_DB_PORT=5432
PROD_DB_NAME=your_production_database_name
```
### Important:

Obtain production credentials from your `heroku-postgres` settings. Never store production credentials in version control (e.g., Git).

### 4. Starting the Database container (Development Only)

Refer to this separate [guide](docs/guide.md) for instructions on starting the database container in a development environment.

# Using the Tool

### 1. Running Migrations:

`run_migrations.py` handles database schema changes through Alembic migrations. Execute this first:

```bash
python3 run_migrations.py -production -new  # Use '-development' for development
```
`-new` flag is to indicate that there's been some changes in the original database schema, so alembic needs to create new migrations accordingly. So only pass this flag if you changed the original schema otherwise leave blank. 

### 2. Uploading Data:

`main.py` uploads data from your CSV files. Run it only after migrations:

```bash
python3 main.py -production  # Use '-development' for development
```

# Additional Notes:

The -production flag is used for production environment. Use -development for local development.  
The project uses Alembic for migrations. Refer to the official [documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html) for advanced usage.

# Development checklist

- [x] Create database schema
- [x] Add configurations  
- [x] Create the migrations 
- [x] Read and validate data 
- [x] Make insertions  
- [ ] Add indexes to tables 
- [ ] Add logging 
- [x] Deploy to heroku 
- [ ] Batch insertions for better performance.
