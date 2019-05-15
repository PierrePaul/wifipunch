FROM python:3.6-alpine
ENV path="/wifipunch"
ADD wifipunch $path
RUN pip install -r ${path}/requirements.txt
CMD python ${path}/run.py
