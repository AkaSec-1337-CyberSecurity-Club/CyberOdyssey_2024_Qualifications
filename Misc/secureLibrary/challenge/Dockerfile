FROM gcc:13.3.0

RUN apt-get update \
    && apt-get install --no-install-recommends -y socat

WORKDIR /usr/src/myapp

RUN echo -n "ODYSSEY{hhhhhhh_7h15_15_7h3_fl4g_hh}" > flag.txt

COPY chall.c run_chall.sh ./

RUN chmod +x run_chall.sh

RUN gcc -o chall chall.c

EXPOSE 4041

CMD socat -T60 TCP-L:4041,fork,reuseaddr EXEC:"/usr/src/myapp/run_chall.sh",pty,stderr,setsid,sane,raw,echo=0
