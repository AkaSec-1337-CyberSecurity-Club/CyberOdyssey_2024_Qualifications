FROM archlinux@sha256:ddf93aeb00bb0be8dd2aadbd643df87c377e2f8726740303e6c44c7090e10958

RUN pacman -Sy
RUN pacman -S --noconfirm socat qemu

RUN useradd ctf

WORKDIR /chal
COPY burg.bin /chal
COPY run.sh /chal
RUN chmod 755 run.sh 


CMD ["socat", "tcp-l:8181,reuseaddr,fork", "EXEC:./run.sh"]
