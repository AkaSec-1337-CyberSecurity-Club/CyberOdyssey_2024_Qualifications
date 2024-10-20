FROM ubuntu@sha256:c62f1babc85f8756f395e6aabda682acd7c58a1b0c3bea250713cd0184a93efa as ubu

RUN apt update
RUN apt install make gcc -y
RUN mkdir /app
COPY main.c /app
COPY Makefile /app

WORKDIR /app
RUN make

RUN rm main.c Makefile

FROM pwn.red/jail

COPY --from=ubu / /srv
COPY flag.txt /srv/app/flag.txt

RUN chmod 755 /srv/app/run

ENV JAIL_MEM=10M JAIL_TMP_SIZE=1 JAIL_CPU=1000 JAIL_PORT=7171 JAIL_POW=0
