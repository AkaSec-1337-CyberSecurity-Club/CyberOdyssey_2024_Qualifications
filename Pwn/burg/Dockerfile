FROM ubuntu:24.10 as ubu

RUN apt-get update && apt-get -y install \
    qemu-system-x86 \
    && rm -rf /var/lib/apt/lists/*

FROM pwn.red/jail

COPY --from=ubu / /srv
COPY run.sh /srv/app/run
COPY burg.bin /srv/app/burg.bin

RUN chmod 755 /srv/app/run

ENV JAIL_MEM=64M JAIL_TMP_SIZE=269M JAIL_CPU=1000 JAIL_PORT=8181 JAIL_POW=0 JAIL_TIME=696969

