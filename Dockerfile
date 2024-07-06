FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip3 install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 8080
EXPOSE 8080

# Specify the command to run the application
CMD ["python3", "main.py"]