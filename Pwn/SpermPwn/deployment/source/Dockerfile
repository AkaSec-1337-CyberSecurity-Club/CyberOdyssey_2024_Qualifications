FROM ubuntu:22.04
RUN apt-get update && apt-get install -y socat 

WORKDIR /app
COPY ./chall .
COPY ./flag.txt .
RUN useradd -m ctf
USER ctf
CMD ["socat", "TCP-LISTEN:2001,reuseaddr,fork", "EXEC:/app/chall"]