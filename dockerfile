# Use an official lightweight Python image
FROM python:3.10-slim-bullseye

# Set the working directory inside the container
WORKDIR /code

# Copy your local files to the container
COPY ./requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit needs this for containerized apps
#ENV PYTHONUNBUFFERED=1
#ENV STREAMLIT_PORT=8501
COPY ./src ./src
#EXPOSE 8501

# Set Streamlit to allow access from outside the container
CMD ["streamlit", "run", "src/app.py","--server.runOnSave=true", "--server.headless=true", "--server.fileWatcherType=poll"]
