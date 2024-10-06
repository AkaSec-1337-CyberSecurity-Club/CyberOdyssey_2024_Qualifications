#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void returnToMePlease()
{
    int a = 0;
    if (a == 0x1337)
    {
        printf("You are not allowed to call this function\n");
        return;
    }
    system("/bin/sh");
}
int main()
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    char name[0x10];
    printf("return to me please : %p\n", returnToMePlease);
    gets(name);
    return 0;
}