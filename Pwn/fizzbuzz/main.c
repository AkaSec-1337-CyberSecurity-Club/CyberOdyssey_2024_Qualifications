#include <stdio.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

const char *ok = "";

/*
 * Description:
 * this is a challenge to bypass a certain filter that doesnt allow you to get a 
 * shell on the system while executing your code, the solution at the end is 
 * use the registers from read to reread from the input and bypass the filter 
 * and execute the code
 */

#define SC_SIZE (1024 * 4)

void slow_print(char *msg){
	int i = -1;
	while (msg[++i] != '\0'){
		write(1, &msg[i], 1);
		usleep(50000);
	}
	write(1, "\n", 1);
}

void  __attribute__((constructor)) ignore_me(){
	setvbuf(stdin, 0, _IONBF, 0);
	setvbuf(stdout, 0, _IONBF, 0);
	setvbuf(stderr, 0, _IONBF, 0);
	alarm(128);
}

void fabort(){
	puts("Not happening");
	exit(EXIT_FAILURE);
}

int main(){
	unsigned char	*buffer;
	int	i = -1;

	buffer = mmap((void *)0x0, SC_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC,
			MAP_PRIVATE|MAP_ANONYMOUS, -1 , 0);

	bzero(buffer, SC_SIZE);
	printf("shellcode >> ");
	buffer[read(0, buffer, SC_SIZE) - 1] = '\0';
	mprotect(buffer, SC_SIZE, PROT_READ | PROT_EXEC);
	bool x = false;
	while (++i != SC_SIZE){
		if (buffer[i] == 0)
			continue;
		if (x == false){
			x = true;
			if (buffer[i] % 3 != 0){
				fabort();
			}
		} else {
			x = false;
			if (buffer[i] % 5 != 0){
				fabort();
			}
		}
	}
	slow_print("executing...");
	register long long r8 __asm__ ("r8") = 0;
	((void (*) (void)) buffer) ();
	slow_print("/bin/sh");

}
