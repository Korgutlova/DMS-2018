FROM python:3.6
RUN mkdir -p /app
ADD ./requirements.txt /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app