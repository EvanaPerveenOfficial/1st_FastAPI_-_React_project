FROM python:latest


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /docker_app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir jose


COPY . /docker_app/


EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]