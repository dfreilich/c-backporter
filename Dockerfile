# Use an appropriate base image (e.g., Python)
FROM python:3.12

# Install diff and patch utilities (assuming they are available via apt-get)
RUN apt-get update && apt-get install -y \
    diffutils \
    patch

# Set working directory
WORKDIR /app

# Install Python dependencies, if any (update with your requirements.txt)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script into the container
COPY backporter/app.py /app/

# Command to run your Python script with placeholder arguments
CMD ["python", "app.py", "/data/before.c", "/data/after.c", "/data/target.c", "-o", "/data"]
