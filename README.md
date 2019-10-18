# GraphQL + Flask

GrapQL API to get logs data.

Logs are in `resource` folder.

## Installation

Use `Python3.7` to install `pipenv` and all dependencies

```shell
python3.7 -m pip install pipenv
python3.7 -m pipenv install
```

Virtual environment should be created with all dependencies.

## Run

- Run postgres
```shell
docker-compose -f docker-compose up
```
- Run Flask app
```shell
python service/app.py
```

After Flask app is run, appropriate user is created (used for Basic Auth).

*Note:* the password is not hashed in DB intentionally.

- Go to `http://127.0.0.1:5000/` to access the API.
