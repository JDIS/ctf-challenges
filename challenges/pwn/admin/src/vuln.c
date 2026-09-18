#include <stdio.h>
#include <stdlib.h>

void vuln()
{
    volatile int is_admin = 0;
    char buf[32];

    printf("Enter password:\n");
    gets(buf);

    if (is_admin)
    {
        puts("Access granted!");
        puts("REDACTED");
    }
    else
    {
        puts("Access denied!");
    }
}

int main(void)
{
    setbuf(stdout, NULL);
    vuln();
    return 0;
}