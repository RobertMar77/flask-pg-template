# Postgres-backed Flask Server Template

This is a template repository for setting up a basic Flask app backed by a Postgres database.

## Developing in VS Code with the Remote Development Extension Pack

VS Code offers [a feature](https://code.visualstudio.com/docs/remote/containers) that lets you use a Docker container as your full-time development environment.

Install the [Remote Development Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack), and then when you open a project that has a `.devcontainer` folder/file, VS Code will prompt you to re-open the project inside a container. This can take several minutes to set up on the initial run, but should be quicker afterwards

This will make it so that all necessary system and project dependencies are installed all at once. Neat!

### Codebase Summary

This repo consists of a Postgres database, a pgAdmin web server, and a Python Flask web server application skeleton.

### Seeding the database

If you wish to initialize the database upon creation, you can add `.sql` files in a `/.devcontainer/pg_init` folder. See the [postgres docker readme](https://github.com/docker-library/docs/blob/master/postgres/README.md#initialization-scripts) for details.

### Running the Flask Application

Inside the integrated terminal in VS Code, type

```
flask --debug run
```

This will run the server bound to TCP port 5000. You can then make HTTP calls to `http://localhost:5000`

### Connecting to the pgAdmin DBMS instance

You can use the included dbms instance by opening `http://localhost:5050` in a browser window and entering the following credentials:

**username**: `admin@admin.com`

**password**: `root`

Database server credentials from the "Add New Server" dialog):

**Connection -> Host**: `db`
**Connection -> Username**: `postgres`
**Connection -> Password**: `postgres`
