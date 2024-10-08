# Use an official TensorFlow runtime as a parent image
FROM tensorflow/tensorflow:latest-py3

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 7860 available to the world outside this container
EXPOSE 7860

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "src/main.py"]
