ASM = nasm
ASRC = src/boot.s
SSRC = src/burg.c src/io.c
NAME = burg.bin
RUN = qemu-system-x86_64
CFLAGS = -nostdlib -ffreestanding -mno-red-zone -fno-exceptions  -Wall -Wextra -Werror -T linker.ld

all : build boot burg add_offset add_flag

build:
	if [ ! -d "build/" ]; then \
		mkdir build; \
	fi

boot : 
	$(ASM) -f elf $(ASRC) -o build/boot.bin

burg:
	i386-elf-gcc -m32 -ggdb $(SSRC) build/boot.bin -o $(NAME) $(CFLAGS)

add_offset :
	dd if=/dev/zero of=burg.bin bs=$(shell expr 2048 - `stat -c %s burg.bin`) count=1 seek=$(shell stat -c %s burg.bin) oflag=seek_bytes

add_flag :
	dd if=flag.txt of=burg.bin bs=$(shell stat -c %s flag.txt) count=1 seek=$(shell stat -c %s burg.bin) oflag=seek_bytes

run : build boot
	$(RUN) -nographic -serial mon:stdio -fda $(NAME)

debug : 
	$(RUN) -nographic -serial mon:stdio -fda $(NAME) -s -S

clean : 
	rm -rf build

fclean : clean
	rm -rf $(NAME)
