FROM python:3.8-slim-buster

# runs the gateway on localhost:8001

EXPOSE 8081

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

# Switching to a non-root user
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden.
CMD ["gunicorn", "--bind", "0.0.0.0:8081", "apigateway:api"]
