SRC = main.c
NAME = run
CFLAGS = -fno-stack-protector -no-pie

$(NAME): $(SRC)
	gcc $(CFLAGS) $(SRC) -o $(NAME)

clean :
	rm -rf $(NAME)
