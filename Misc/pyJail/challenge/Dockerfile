FROM python:3.11-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y socat \
    && groupadd ctf \
    && useradd -r -g ctf ctf

WORKDIR /usr/src/app

RUN echo -n "ODYSSEY{pyJ41l5_4r3_5t1ll_4_Tr3nD}" > flag.txt

COPY chall.py .

RUN chmod 500 chall.py \
    && chown ctf:root chall.py \
    && chmod 444 flag.txt

USER ctf

EXPOSE 4042

CMD socat -T120 TCP-L:4042,fork,reuseaddr EXEC:"python3 chall.py",pty,stderr,setsid,sane,raw,echo=0