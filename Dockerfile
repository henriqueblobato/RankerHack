FROM python:3.10

WORKDIR /app

RUN apt-get update
RUN apt-get install -y npm && \
	npm install -g yarn && \
	yarn global add playwright && \
	yarn global add playwright-chromium

RUN playwright install-deps

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8081

CMD ["python", "app.py"]
