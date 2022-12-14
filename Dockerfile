# start by pulling the python image
FROM python:3.8

RUN apt-get update

RUN mkdir /app

# copy the requirements file into the image
COPY . /app

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

WORKDIR /app/src

#CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

ENTRYPOINT ["python"]

CMD ["app.py"]

