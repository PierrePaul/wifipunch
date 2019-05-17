FROM python:3.6-alpine
ENV path="/wifipunch"
RUN apk add --no-cache --update postgresql-dev python3-dev build-base
ADD wifipunch/requirements.txt ${path}/requirements.txt
RUN pip install -r ${path}/requirements.txt
# ADD wifipunch $path
# COPY wifipunch $path
CMD FLASK_APP=${path}/app.py flask run --host=0.0.0.0
