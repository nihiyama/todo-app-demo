# backend

## setup

1. setup development with devcontainer. (see .devcontainer dir)
    - choose python container.
    - preinstall pipenv.

2. start virtualenv
    - `pipenv shell`

3. pipenv install (the following is included in the pipfile packages)
    - fastapi[all]
      - pydanitc
      - starlett
      - uvicorn
      - etc.
    - sqlalchemy
    - sqlalchemy-utils
    - gunicorn
    - fastapi-camelcase
    - python-jose[cryptography]
    - passlib[bcrypt]
    - fastapi-jwt-auth
4. pipenv install --dev (the following is included in the pipfile dev-packages)
      - pytest
      - pytest-cov
      - pytest-mock
      - pytest-asyncio