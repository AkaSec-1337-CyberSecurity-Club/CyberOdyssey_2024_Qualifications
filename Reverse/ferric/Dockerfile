FROM debian

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    unzip \
    wget \
    binutils-mips64-linux-gnuabi64 \
    binutils-aarch64-linux-gnu

RUN mkdir /ctf
COPY ./src/main.py /ctf

RUN wget https://yx7.cc/code/ynetd/ynetd-2024.02.17.tar.xz
RUN tar -xvf ynetd-2024.02.17.tar.xz
RUN cd ynetd-2024.02.17 && make && chmod +x ynetd && cp ynetd /usr/bin/

WORKDIR /ctf
CMD chmod +x main.py && ynetd -p 7771 ./main.py