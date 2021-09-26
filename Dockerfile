FROM debian:stable-slim
RUN apt update && apt install python3 python3-pip -y
RUN pip3 install uvicorn fastapi psycopg2-binary
COPY ./ ./
EXPOSE 8000
ENTRYPOINT ["python3", "main.py"]
