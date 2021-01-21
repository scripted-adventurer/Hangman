FROM alpine:latest
RUN apk update
RUN apk add --no-cache python3 py3-pip
RUN pip3 install pytest
RUN pip3 install Flask
WORKDIR /app
COPY . .