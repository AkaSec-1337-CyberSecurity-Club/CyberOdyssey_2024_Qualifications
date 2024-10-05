FROM gcc:13.3.0

RUN apt-get update \
    && apt-get install --no-install-recommends -y socat

WORKDIR /usr/src/myapp

RUN echo -n "ODYSSEY{f4k3_fl4g}" > flag.txt

COPY chall.c ./

RUN gcc -o chall chall.c

EXPOSE 4746

CMD socat -T60 TCP-L:4746,fork,reuseaddr EXEC:"./chall",pty,stderr,setsid,sane,raw,echo=0