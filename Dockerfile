FROM python:3.11-slim-buster

#ENV PYTHONDONTWRITEBYTECODE =1
#ENV PYTHONUNBUFFERED =1

WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt

# RUN pip install --upgrade pip
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY . .

EXPOSE 8000

RUN poetry config virtualenvs.create false --local

# Django serverni ishga tushirish
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]