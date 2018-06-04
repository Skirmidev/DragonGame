FROM python:3.4-alpine
COPY . /web
WORKDIR /web/app
RUN pip install -r ./requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]