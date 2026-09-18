#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void secret()
{
    puts("Access granted!");
    puts("JDIS{buff3r0verf1ow}");
    exit(0);
}

void vuln()
{
    char buf[64];
    printf("Enter your name:\n");
    fgets(buf, 200, stdin);
    printf("Hello %s\n", buf);
}

int main(void)
{
    setbuf(stdout, NULL);
    vuln();
    puts("Goodbye!");
    return 0;
}
