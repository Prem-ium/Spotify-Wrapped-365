FROM python:3
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD main.py /
ADD covers /
ADD .cache* /
ADD .cache /

CMD [ "python", "./main.py" ]