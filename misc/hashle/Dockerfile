FROM python:slim-buster

# copy src to the image
COPY challenge-files /app

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# configure the container to run in an executed manner
ENTRYPOINT ["python"]

# expose the app port
EXPOSE 1337

CMD ["server.py"]
