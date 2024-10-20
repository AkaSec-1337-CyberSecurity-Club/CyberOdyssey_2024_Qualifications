#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <stdbool.h>

#define MENU "1. Pomodoro timer\n2. Create a TODO\n3. Delete a TODO\n4. Print TODOs\n5. Finish TODO\n6. edit TODO\n>> "

typedef struct tmp_buffer{
	uint64_t size;
	char buffer[16];
}tmp_buffer;

typedef struct todo {
	int	tmp;
	int	done;
	char	*todo;
	int	todo_size;
}todo;

todo *todos[100] = {0};
uint8_t todo_count = 0;


int readint(){
	char buffer[10];
	bzero(buffer, 10);
	if (read(0, buffer, 3) > 1){
		return (atoi(buffer));
	}
	return (0);
}

void pomo(){
	int i = 25;
	while (i > 0){
		printf("\e[1;1H\e[2J\t\t%d minutes left", i);
		sleep(60);
		i--;
	}
	puts("");
}
void ctodo(char *tmp){
	puts("Pick up your battles");
	if (todo_count >= 99){
		puts("Nope. That's too many battles.");
		puts("Put some battles back.");
		return;
	}
	todos[todo_count] = calloc(sizeof(todo), 1);
	todos[todo_count]->tmp = false;
	todos[todo_count]->done = false;
	printf("Battle size >> ");
	int bsize = readint();
	if (bsize > 999) {
		printf("Yeah no");

	}
	todos[todo_count]->todo = calloc(bsize, 1);
	if (todos[todo_count]->todo == NULL){
		todos[todo_count]->todo = tmp;
		todos[todo_count]->tmp = true;
	}
	printf("Battle name >> ");
	if ((size_t)(bsize + 2) > 1000){
		puts("integer overflow detected, exploit rejected");
		exit(EXIT_FAILURE);
	}
	read(0, todos[todo_count]->todo, bsize + 2);
	todos[todo_count]->todo_size = bsize;
	todo_count++;
	printf("Battle added, todo index is %d\n", todo_count - 1);
}

void etodo(){
	printf("todo index >> ");
	uint8_t todo_idx = readint();
	if (todo_idx > 100 || todos[todo_idx] == NULL){
		puts("NOP");
		return;
	}
	printf("todo title >> ");
	read(0, todos[todo_idx]->todo, todos[todo_idx]->todo_size + 2);
	puts("done");
	

}

void dtodo(){
	printf("todo index >> ");
	uint8_t todo_idx = readint();
	if (todo_idx > 100){
		puts("NOP");
		return;
	}
	if (todos[todo_idx]->tmp != true)
		free(todos[todo_idx]->todo);
	free(todos[todo_idx]);
	puts("todo deleted");
}

void ptodo(){
	printf("todo index >> ");
	uint8_t todo_idx = readint();
	if (todos[todo_idx] == NULL)
		return;
	if (todo_idx < 100)
		printf("[%c] - %s\n", todos[todo_idx]->done ? 'x' : ' ', todos[todo_idx]->todo);
}

void stodo(){
	printf("todo index >> ");
	uint8_t todo_idx = readint();
	if (todo_idx > 100){
		puts("Yeah, you still didn't reach that level.");
		return;
	}
	if (todos[todo_idx] != NULL)
		todos[todo_idx]->done = true;
	puts("Done");
}


void  __attribute__((constructor)) ignore_me(){
        setvbuf(stdin, 0, _IONBF, 0);
        setvbuf(stdout, 0, _IONBF, 0);
        setvbuf(stderr, 0, _IONBF, 0);
        alarm(128);
	asm volatile("nop;pop %rbp;ret;pop %rdi;ret;");
}

void menu(){
	uint32_t uchoise;
	tmp_buffer emerg_buffer;
	bzero(&emerg_buffer, sizeof(tmp_buffer));
	while (true){
		printf(MENU);
		uchoise = readint();
		if (uchoise == 1)
			pomo();
		else if (uchoise == 2)
			ctodo(emerg_buffer.buffer);
		else if (uchoise == 3)
			dtodo();
		else if (uchoise == 4)
			ptodo();
		else if (uchoise == 5)
			stodo();
		else if (uchoise == 6)
			etodo();
		else 
			return;
	}
}

int main(){
	bzero(todos, sizeof(todos));
	menu();
}
