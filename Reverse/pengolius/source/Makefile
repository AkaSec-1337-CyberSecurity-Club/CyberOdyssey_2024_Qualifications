NAME = pengolius

ASM = nasm
LD = ld

ASMFLAGS = -f elf64
LDFLAGS = -pie -dynamic-linker /lib64/ld-linux-x86-64.so.2

SRC = pengolius.asm

OBJ = $(SRC:.asm=.o)

RM	=	rm -f

all: $(NAME)

$(OBJ): $(SRC)
	$(ASM) $(ASMFLAGS) $< -o $@

$(NAME): $(OBJ)
	$(LD) $(LDFLAGS) $< -o $@

clean:
	$(RM) $(OBJ)

fclean: clean
	$(RM) $(NAME)

re: fclean all

.PHONY: all clean fclean re