FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

#no-root is used for dependencies to be installed in the container without installing the project itself. 
#It can fasten the build process and reduce the size of the final image.
RUN pip install poetry && poetry install --no-root 

COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

