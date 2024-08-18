FROM alpine:latest

RUN apk add --update --no-cache python3 && apk add py3-pip
RUN apk add firefox
RUN rm /usr/lib/python*/EXTERNALLY-MANAGED
RUN pip install flask && pip install selenium

WORKDIR /app

COPY main.py ./
COPY templates/index.html ./templates/

EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["main.py"]