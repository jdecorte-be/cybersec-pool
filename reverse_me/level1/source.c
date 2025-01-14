#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>

int main()
{
    char password[] = "__stack_check";
    printf("Please enter key: ");
    
    char tocmp[100];
    scanf("%s", &tocmp);

    if(strcmp(&tocmp, &password) != 0)
        printf("Nope.\n");
    else
        printf("Good job.\n");
    return 0;
}
