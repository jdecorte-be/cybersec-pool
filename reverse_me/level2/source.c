#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

int32_t ok()
{
    return puts("Good job.");
}

void no()
{
    puts("Nope.\n");
    exit(1);
}

int main()
{
    // MEMORY REPRESENTATION
    // buffer2 | ebp - 0x39 to 0x35 | len = 4
    // password | ebp - 0x35 to 0x1d | len = 24
    // buffer1 | ebp - 0x1d to 0x14  | len = 9

    char password[24]; // ebp - 0x35
    char buffer2[4];

    printf("Please enter key: ");
    if (scanf("%23s", &password) != 1)
        no();

    // password need to start with '00'
    if(password[1] != '0') // ebp - 0x34
        no();
    if(password[0] != '0') // ebp - 0x35
        no();
    fflush(0); // clear stdin

    char buffer1[9]; // ebp - 0x1d
    memset(&buffer1, 0, 9);
    buffer1[0] = 'd'; // byte [ebp-0x1d] = 0x64
    buffer2[3] = '\0'; // byte [ebp-0x36] = 0x0

    int32_t a = 2; // ebp - 0x14
    int32_t b = 1; // ebp - 0x10

    while(true)
    {
        bool cmp = false;

        if(strlen(&buffer1) < 8)
            cmp = a < strlen(&password);

        if (!cmp)
            break;

        // password is ascii of delabere by pack of 3
        // password = "00101108097098101114101"
        buffer2[0] = password[a];
        buffer2[1] = password[1 + a];
        buffer2[2] = password[2 + a];
        buffer1[b] = atoi(&buffer2);
        a += 3;
        b++;
    }
    buffer1[b] = 0;

    if (strcmp(&buffer1, "delabere") != 0)
        no();

    ok();
    return 0;
}