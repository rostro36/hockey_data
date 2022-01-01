FROM python:3.8

COPY application.py data_reader.py plotting.py team_dict.py requirements.txt ./
COPY data/ data/
COPY logos/ logos/

RUN pip install -r requirements.txt

CMD python3.8 application.py
