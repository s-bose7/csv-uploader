## Set up a PostgreSQL Docker container (With GIS support)

Image name: postgis/postgis
Container name:  postgis 
Password:  mysecretpassword 

```bash
$ docker pull postgis/postgis
$ docker run --name postgis -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgis
```

```bash
docker: Error response from daemon: Conflict. The container name "/postgis" is already in use by container "4394f94b3bf9885bf25959c385c54cb762f63e571be843bea6f1857b03d2044c". You have to remove (or rename) that container to be able to reuse that name.
See 'docker run --help'.
```
If you see in the command line this message after doing docker run, that means a container name "my-postgres" is alreday running.  
In that case you can start the container by doing ```$ docker start postgis```. Alternatively you can remove the container by doing ```$ docker rm -f postgis```. 

## Verify whether the container is up and running

```bash
$ docker ps
3d8454300c26   postgis   "docker-entrypoint.s…"   5 hours ago   Up 5 hours   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgis
```

If you see the output something like above then congrats!

## Creating the database

#### STEP 1: Connect to psql shell in the container
```bash
$ docker exec -it mpostgis bash
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