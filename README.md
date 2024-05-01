# Database Schema

For detail schema [see here.](https://raw.githubusercontent.com/s-bose7/csv-uploader/master/docs/schema.md) To get a  guide on how to start the database container [see here.](https://raw.githubusercontent.com/s-bose7/csv-uploader/master/docs/guide.md)

![Alt Text](https://raw.githubusercontent.com/s-bose7/csv-uploader/master/docs/database_schema.png)



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

