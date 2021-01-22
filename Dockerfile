FROM alpine:latest
RUN apk update
RUN apk add --no-cache python3 py3-pip
RUN pip3 install pytest
RUN pip3 install Flask
WORKDIR /app
COPY . .
EXPOSE 5000
CMD flask run --host 172.17.0.2