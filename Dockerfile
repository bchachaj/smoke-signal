# For more information, please refer to https://aka.ms/vscode-docker-python
FROM public.ecr.aws/lambda/python:3.7

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app.py scry.py .env ./


# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
USER 9000

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["app.handler"]
