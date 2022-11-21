FROM python:slim-buster

COPY challenge-files /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 5555
CMD ["server.py"]
