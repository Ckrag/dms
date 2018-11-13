# Use an official Python runtime as an image
FROM python:3.6
#FROM phusion/baseimage:latest

# The EXPOSE instruction indicates the ports on which a container # # will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this
# instruction creates a directory with this name if it doesn’t exist
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run dms.py when the container launches
COPY app.py /app
COPY data /app/data
COPY model /app/model
COPY templates /app/templates
COPY static /app/static
#CMD python app.py

#ENTRYPOINT [ "python" ]
#CMD [ "dms.py" ]
