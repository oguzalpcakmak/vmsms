FROM python:3.10-alpine
#RUN apt-get update && apt-get install -y libpq-dev gcc
#RUN apt-get install libsasl2-dev

RUN ls *

WORKDIR /base_project_py

COPY base_project_py/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY base_project_py/. .

RUN ls *

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
