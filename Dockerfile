# Use a specific version of Alpine Linux as the base image
FROM alpine:3.15.3

# Use Python 3.10.12
ENV PYTHON_VERSION=3.10.12

# Install necessary system dependencies
RUN apk add --no-cache python${PYTHON_VERSION} py3-pip

# Install a specific version of pip (example: 21.3.1)
RUN pip3 install --no-cache-dir 'pip==21.3.1'

# Set the working directory in the container
WORKDIR /app

# Copy the FastAPI app code into the container
COPY . .

# Install necessary Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port that the FastAPI app will run on
EXPOSE 5000

# Command to run the FastAPI app using uvicorn
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
