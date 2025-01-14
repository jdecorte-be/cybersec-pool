#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

void ___syscall_malloc(void)
{
    puts("Nope.");
    exit(1);
}

void ____syscall_malloc(void)
{
    puts("Good job.");
    return;
}

int main()
{
    // MEMORY REPRESENTATION
    // buffer2 | ebp - 0x44 to 0x40 | len = 4
    // password | ebp - 0x40 to 0x1d | len = 31
    // buffer1 | ebp - 0x21 to 0x18  | len = 9

    char password[31];
    char buffer2[4];

    if (scanf("%23s", &password) != 1)
        ___syscall_malloc();

    // password need to start with '42'
    if(password[1] != '2')
        ___syscall_malloc();
    if(password[0] != '4')
        ___syscall_malloc();
    fflush(0); // clear stdin

    char buffer1[9];
    memset(&buffer1, 0, 9);
    buffer1[0] = '*';
    buffer2[3] = '\0';

    int32_t a = 2;
    int32_t b = 1;

    while(true)
    {
        bool cmp = false;

        if(strlen(&buffer1) < 8)
            cmp = a < strlen(&password);

        if (!cmp)
            break;

        // password is ascii of delabere by pack of 3
        buffer2[0] = password[a];
        buffer2[1] = password[1 + a];
        buffer2[2] = password[2 + a];
        buffer1[b] = atoi(&buffer2);
        a += 3;
        b++;
    }
    buffer1[b] = 0;

    // password "42042042042042042042042"
    switch(strcmp(&buffer1, "********"))
    {
        case 0:
        {
            ____syscall_malloc();
            return 0;
            break;
        }
        case 1:
        {
            ___syscall_malloc();
        }
        case 2:
        {
            ___syscall_malloc();
        }
        case 3:
        {
            ___syscall_malloc();
        }
        case 4:
        {
            ___syscall_malloc();
        }
        case 5:
        {
            ___syscall_malloc();
        }
        case 0x73:
        {
            ___syscall_malloc();
        }
        case 0xfffffffe:
        {
            ___syscall_malloc();
        }
        case 0xffffffff:
        {
            ___syscall_malloc();
        }
    }

    ___syscall_malloc();
    return 0;
}