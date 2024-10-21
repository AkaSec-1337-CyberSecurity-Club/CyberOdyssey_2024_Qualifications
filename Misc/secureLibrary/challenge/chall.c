#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
#include <sys/stat.h>

void create_file(const char *file_name, const char *content) {
    struct stat buffer;
    if (stat(file_name, &buffer) == 0) {
        printf("File already exists\n");
        return;
    }

    FILE *f = fopen(file_name, "w");
    if (!f) {
        perror("Error opening file");
        return;
    }

    fprintf(f, "%s", content);
    fflush(f);
    printf("File created successfully\n");
}

void read_file(const char *file_name) {
    FILE *file = fopen(file_name, "r");
    if (!file) {
        perror("File not found");
        return;
    }

    printf("File content: ");

    int ch;
    while ((ch = fgetc(file)) != EOF) {
        if (strstr(file_name, "flag")) {
            putchar('h');
        } else {
            putchar(ch);
        }
    }
    putchar('\n');
}

int main() {
    char choice;
    char file_name[256];
    char content[1024];

    while (1) {
        printf("\n*******************************\n");
        printf("*     Library Application     *\n");
        printf("*******************************\n");
        printf("*    1. Create file           *\n");
        printf("*    2. Read file             *\n");
        printf("*    3. Exit                  *\n");
        printf("*******************************\n");
        printf("Enter choice: ");

        choice = getchar();
        while (getchar() != '\n');

        switch (choice) {
            case '1':
                printf("Enter file name: ");
                fgets(file_name, sizeof(file_name), stdin);
                file_name[strcspn(file_name, "\n")] = '\0';

                printf("Enter content: ");
                fgets(content, sizeof(content), stdin);
                content[strcspn(content, "\n")] = '\0';

                create_file(file_name, content);
                break;
            case '2':
                printf("Enter file name: ");
                fgets(file_name, sizeof(file_name), stdin);
                file_name[strcspn(file_name, "\n")] = '\0';

                read_file(file_name);
                break;
            case '3':
                return 0;
            default:
                printf("Invalid choice\n");
                break;
        }
    }

    return 0;
}