FROM python:3.13

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e src

EXPOSE 5000

ENV QUART_APP=ssg:app

ENTRYPOINT ["quart", "run", "-h", "0.0.0.0", "-p", "5000"]
