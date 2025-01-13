#include <unistd.h>
#include <string.h>
#include <stdio.h>

int main()
{
    int32_t password;
    strcpy(password, "__stack_check");
    printf("Please enter key: ");
    
    void tocmp;
    scanf("%s", tocmp, &_GLOBAL_OFFSET_TABLE_);

    if(strcmp(&tocmp, &password) != 0)
        printf("Nope.\n");
    else
        printf("Good job.\n");
    return 0;
}
