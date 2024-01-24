FROM python:3.12-slim
RUN pip install django psycopg2-binary requests Pillow

COPY ./project/ /project
WORKDIR /project
# ARG PASS = 12345
# ENV pass = $PASS
CMD python3 manage.py migrate && \
    python3 manage.py runserver 0.0.0.0:8000


    