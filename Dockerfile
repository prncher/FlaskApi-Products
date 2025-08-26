FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
# indicates the port from the host. If the host is using 4000 from env file, change the expose.
EXPOSE 4000
CMD ["python", "./services/products.py"]
# RUN apk add bash curl --no-cache
