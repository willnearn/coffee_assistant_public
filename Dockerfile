#Docker work flow:
# docker build -t willnearn/umiapp:latest .    #I think this automatically tags it as latest?
# docker run -p 80:80 willnearn/umiapp:latest
# docker login
# docker push willnearn/umiapp:latest


# Use an official Python runtime as a parent image. May need to come back and delete -slim later if the run fails, but I think that I should be fine here since I `pip install` both packages that I import in my code
FROM python:3.9-slim

# Set the working directory in the container. REVIEW
WORKDIR /usr/src/umiapp 

# Copy the current directory contents into the container at /usr/src/app
COPY requirements.txt ./
# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Set environment variable for access to OpenAI
ENV NOT_OPENAI_API_KEY=<ImNotGivingOutMyApiKey>
ENV NOT_GOOGLE_API_KEY=<ImNotGivingOutMyApiKey>

# Make port 80 available to the world outside this container
EXPOSE 80

#Setup Flask
ENV FLASK_APP=run_gemini.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["python", "./run_gemini.py"]
