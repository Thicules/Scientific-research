FROM python:3.10.10

WORKDIR /app

COPY . .


RUN pip install -r requirements.txt

ENV FLASK_APP=Build_web.py

ENV FLASK_ENV=development

EXPOSE 8080

CMD ["python3", "Build_web.py"]