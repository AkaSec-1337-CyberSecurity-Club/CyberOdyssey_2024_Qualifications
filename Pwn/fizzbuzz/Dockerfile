FROM ubuntu@sha256:c62f1babc85f8756f395e6aabda682acd7c58a1b0c3bea250713cd0184a93efa as ubu

FROM pwn.red/jail

COPY --from=ubu / /srv
COPY fizzbuzz /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run

ENV JAIL_MEM=10M JAIL_TMP_SIZE=1 JAIL_CPU=1000 JAIL_PORT=9191 JAIL_POW=0
