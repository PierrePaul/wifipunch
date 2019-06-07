FROM node:alpine as uibuild
ENV uipath="wifipunchui"
COPY ${uipath}/package.json /${uipath}/package.json
COPY ${uipath}/package-lock.json /${uipath}/package-lock.json
WORKDIR /${uipath}
RUN npm install
COPY ${uipath} /${uipath}
RUN sed -i '/baseURL/d' services/UserServices.js
RUN npm run build --verbose

FROM python:3.6-alpine
ENV path="/wifipunch"
RUN apk add --no-cache --update postgresql-dev python3-dev build-base
ADD wifipunch/requirements.txt ${path}/requirements.txt
RUN pip install -r ${path}/requirements.txt
# ADD wifipunch $path
COPY wifipunch $path
VOLUME $path
COPY --from=uibuild /wifipunchui/dist /frontend
WORKDIR $path
CMD flask db init || flask db upgrade && flask run --host=0.0.0.0
