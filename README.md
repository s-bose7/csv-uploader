# Database Schema

For more details on the schema [see here.](docs/schema.md) 

![database_schema](docs/database_schema.png)


# Creating and upgrading a new migration

### Create a new migration file for a new database schema:

```bash
$ alembic revision --autogenerate -m "schema updated"
```

### To apply the schema migration and create the database tables:

```bash
$ alembic upgrade head
```

### Alembic keeps track of the current database version, and you can check the current version with:

```bash
$ alembic current
```

### If you need to revert the database to a previous version, you can use:
```bash
$ alembic downgrade -1  # Downgrade one revision
```

# Development checklist

- [x] Create database schema 
- [x] Create the migrations 
- [x] Read and validate data 
- [x] Make insertions
- [ ] Add indexes to tables 
- [ ] Add logging 
- [ ] Add configurations 
- [ ] Dockerize application 
- [ ] Batch insertions for better performance when dealing with large datasets (bulk insert methods or wrap the entire process in a transaction)


# Using this tool progessively in the workflow

-  To get a  guide on how to start the database container [see here.](docs/guide.md)

# Development evnviroment setup

- 