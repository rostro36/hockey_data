FROM python:3.9

COPY dash_app.py team_dict.py plotting.py requirements.txt ./
COPY data/ data/
COPY logos/ logos/

RUN pip install -r requirements.txt

CMD python3.9 dash_app.py