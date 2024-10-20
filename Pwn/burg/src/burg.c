#include "burg.h"

creds user_creds;

void memset(void *ptr, uint8_t byte, uint32_t len){
	uint32_t i = 0;
	while (i < len){
		((uint8_t *) ptr)[i] = byte;
		i++;
	}
}

uint8_t strncmp(char *a, char *b, uint32_t mlen){
	uint32_t i = 0;
	while (a[i] == b[i] && i < mlen){
		i++;
	}
	return (a[i] - b[i]);
}

int main() {
	// reading from floppy
	sinit();
	sprint("BURG loading.\n");
	sprint("Welcome to BURG!\n");
	memset(&user_creds, 0,  sizeof(creds));

	sprint("username >> ");
	sgets(user_creds.username, 32);
	sprint("password >> ");
	sgets(user_creds.password, 32);
	if (strncmp(user_creds.username, "burg_admin", sizeof("burg_admin")) != 0){
		sprint("Get off grub enjoyer\n");
		return (0);
	}
	if (strncmp(user_creds.password, PASS, sizeof(PASS)) != 0){
		sprint("Yeah you might wanna contact burg_admin\n");
		return (0);
	}
	sprint("error: no such partition.\n");
	sprint("Entering rescue mode...\n");
	sprint("burg rescue> ");

	return 0;
}
