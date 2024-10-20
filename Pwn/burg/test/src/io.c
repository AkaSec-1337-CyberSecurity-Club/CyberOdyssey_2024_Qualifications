#include "burg.h"

static inline void outb(unsigned short port, unsigned char val) {
    __asm__ volatile ("outb %0, %1" : : "a"(val), "Nd"(port));
}

static inline unsigned char inb(unsigned short port) {
    unsigned char ret;
    __asm__ volatile ("inb %1, %0" : "=a"(ret) : "Nd"(port));
    return ret;
}

// serial init
void sinit() {
    outb(SERIAL_PORT + 1, 0x00);
    outb(SERIAL_PORT + 3, 0x80);
    outb(SERIAL_PORT + 0, 0x03);
    outb(SERIAL_PORT + 1, 0x00);
    outb(SERIAL_PORT + 3, 0x03);
    outb(SERIAL_PORT + 2, 0xC7);
    outb(SERIAL_PORT + 4, 0x0B);
}

// swrite
void swrite(char a) {
    while ((inb(SERIAL_PORT + 5) & 0x20) == 0);
    outb(SERIAL_PORT, a);
}

// serial print
void sprint(const char* str) {
    while (*str) {
        swrite(*str++);
    }
}

// serial read
uint8_t sread() {
    while ((inb(SERIAL_PORT + 5) & 0x01) == 0);
    return inb(SERIAL_PORT);
}

void spnbr(int n) {
    if (n < 0)  // Handle negative numbers
    {
        swrite('-');
        n = -n;
    }

    if (n >= 10)
        spnbr(n / 10);  // Recursively print the higher digits
    swrite((n % 10) + '0');  // Print the last digit
}

uint32_t sgets(char *buffer, int mlen){
	int i = 0;
	uint8_t keystroke = 0;
	bool nt = false;
	while (keystroke != NL && i < mlen){
		keystroke = sread();
		if (keystroke == BACKSPACE){
			nt = true;
			i--;
		} else {
			buffer[i] = keystroke;
			if (nt == true){
				buffer[i + 1] = '\0';
				nt = false;
			}
			i++;
		}
	}
	swrite('\n');
	buffer[i] = '\0';
	return (uint32_t) i;
}
