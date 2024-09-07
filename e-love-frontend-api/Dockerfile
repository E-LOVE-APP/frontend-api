FROM python:3.10-slim

WORKDIR /app

# Copying the pyproject.toml and poetry.lock files to the working directory of the container
COPY pyproject.toml poetry.lock ./

#no-root is used for dependencies to be installed in the container without installing the project itself. 
#It can fasten the build process and reduce the size of the final image.
RUN pip install poetry && poetry install 

# Copying the rest of the files to the working directory of the container
COPY . /app

# Copying the .env file to the working directory of the container. (However we did it in the previous step, we do it again to make sure it is copied)
COPY .env .env

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

