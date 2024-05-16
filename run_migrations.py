import sys

import configparser
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory

from config import db_config

# Check command-line arguments
if len(sys.argv) < 2:
    print("Usage: python run_migrations.py [-env] [-new]")
    sys.exit(1)

ENV = sys.argv[1] if len(sys.argv) > 1 else "-development"
DB_URL = db_config.get_database_url(environment=ENV)

# Check if the '-new' flag is provided
new_migrations = False
if len(sys.argv) > 2 and sys.argv[2] == "-new":
    new_migrations = True

# Update the alembic.ini file with the new connection string
config = configparser.ConfigParser()
config.read("alembic.ini")
config.set("alembic", "sqlalchemy.url", DB_URL)
with open("alembic.ini", "w") as config_file:
    config.write(config_file)

# Initialize the Alembic configuration
alembic_cfg = Config("alembic.ini")

# Check if there are new migrations
script = ScriptDirectory.from_config(alembic_cfg)
heads = script.get_heads()

if new_migrations:
    revision_message = input("Enter a message for the new revision: ")
    # Run the Alembic revision command with --autogenerate
    print(f"ENVIRONMENT: {ENV}, Running Alembic revisions...")
    command.revision(alembic_cfg, autogenerate=True, message=revision_message)
    command.upgrade(alembic_cfg, "head")
    print("Migrations completed successfully.")

elif heads:
    # There are pending migrations, run the upgrade command
    print(f"ENVIRONMENT: {ENV}, Upgrading database schema...")
    command.upgrade(alembic_cfg, "head")
    print("Database schema upgraded successfully.")

else:
    print(f"ENVIRONMENT: {ENV}, No new migrations found.")


# Remove the database connection string from alembic.ini
config.set("alembic", "sqlalchemy.url", "DB_URL")
with open("alembic.ini", "w") as config_file:
    config.write(config_file)
