FROM python:3.9-slim-buster

RUN mkdir /charm_app
RUN mkdir -p /charm_app/input
RUN mkdir -p /charm_app/output

COPY *.py /charm_app/
COPY requirements.txt /charm_app/
COPY /input/*.csv /charm_app/input/

WORKDIR /charm_app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py", "-z", "ZONES.csv", "-p", "ICU_INPUT_PARAMS.csv", "-c", "DAILY_ARRIVALS.csv"]
