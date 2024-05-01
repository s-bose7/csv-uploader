## Set up a PostgreSQL Docker container

```bash
$ docker run --name my-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

database is:  my-postgres (container name)  
password is:  mysecretpassword (you can set anything, just make sure to change the password in the postgresql.py file)

if you see in the command line this message after doing docker run, that means a container name "my-postgres" is alreday running.

```bash
docker: Error response from daemon: Conflict. The container name "/my-postgres" is already in use by container "4394f94b3bf9885bf25959c385c54cb762f63e571be843bea6f1857b03d2044c". You have to remove (or rename) that container to be able to reuse that name.
See 'docker run --help'.
```

In that case you can start the container by doing ```$ docker start my-postgres```. Alternatively you can remove the container by doing ```$ docker rm -f my-postgres```. 

## Verify whether the container is up and running

```bash
$ docker ps
3d8454300c26   postgres   "docker-entrypoint.s…"   5 hours ago   Up 5 hours   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   my-postgres
$
```

If you see the output something like above then congrats!

## Creating the database

NOTE: We can create a database from a python script as well, but for the context of this project I created the databse manually from `psql` shell. If you need to create the databse programmitically you can fill up the `create_database()` in postgresql.py file.

#### STEP 1: Connect to psql shell in the container
```bash
$ docker exec -it my-postgres bash
root@3d8454300c26:/# 
```
Remember this name should match to whatever name you gave to the container

#### STEP 2: Switch to the postgres user by running the following command:
```bash
root@3d8454300c26:/# su postgres
postgres@3d8454300c26:/$ 
```

#### STEP 3: Once you're logged in as the postgres user, you can start the psql client tool by running:
```bash
postgres@3d8454300c26:/$ psql
postgres=# 
```
This will connect you to the default PostgreSQL database.


#### STEP 4: Listing the default databases 
```bash
postgres=# \l
```

#### STEP 5: Creating a DB
```bash
postgres=# CREATE DATABASE group_contacts;
CREATE DATABASE
```
At this point you can head over to the main.py to start the csv to database migration process. 