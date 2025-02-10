# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables for AWS credentials if not using IAM roles (or mount them as secrets)
# ENV AWS_ACCESS_KEY_ID=your_access_key_id
# ENV AWS_SECRET_ACCESS_KEY=your_secret_access_key

# Define the command to run the application
CMD ["python", "data_ingestion.py"]
