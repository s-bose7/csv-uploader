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

