#include <stdio.h>
#include <string.h>

int main()
{
    fputs("What's the password?\n", stdout);

    char strvar[100];
    if (!fgets(strvar, sizeof strvar, stdin))
        return 1;

    strvar[strcspn(strvar, "\r\n")] = '\0';

    if (strcmp(strvar, "SuperSecretPassword") == 0)
    {
        fputs("JDIS{3asyStr1ngsFl4g}\n", stdout);
    }
    else
    {
        fputs("Get out!\n", stdout);
    }

    return 0;
}