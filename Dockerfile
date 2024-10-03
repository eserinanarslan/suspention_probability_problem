# Use a newer Python version (e.g., Python 3.12)
FROM python:3.12-slim

# Add the requirements.txt to the container
ADD requirements.txt /.

# Install the required Python packages
RUN pip install --upgrade pip && pip install -r /requirements.txt

# Add the code to the container
ADD . /code/
#ADD . /data/

# Set the working directory to /code/src if main.py is inside /src
WORKDIR /code

# Define the default command to run when the container starts
CMD ["python", "src/main.py"]
