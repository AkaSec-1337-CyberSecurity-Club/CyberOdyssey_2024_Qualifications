#ifndef BURG_H
#define BURG_H

#define PASS "thankyougrubfornevercomplaining"

#define SERIAL_PORT 0x3F8

#define BACKSPACE 127
#define NL 13

#include <stdint.h>


#define bool uint8_t
#define true 1
#define false 0

typedef struct creds {
	char username[31];
	char password[31];
}creds;

void sinit();			// serial int
void swrite(char a);		// serial write
void sprint(const char* str);	// serial print
uint8_t sread();		// serial read
uint32_t sgets(char *buffer, int mlen);		// serial fgets
void spnbr(int n);

int read_floppy_sector(char *buffer, uint8_t head, uint8_t track, uint8_t sector);

extern creds user_creds;

#endif
