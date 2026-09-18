#include <stdio.h>
#include <string.h>
#include <stdint.h>

static unsigned char obf[] = {94, 89, 59, 15, 251, 251, 162, 133, 119, 65, 55, 50, 224, 211, 204, 169, 146, 110, 95};
static const size_t expected_len = sizeof obf / sizeof obf[0];

static const unsigned char a[] = {
    31, 48, 65, 82, 99, 116, 133, 150, 167, 184, 201, 218, 235, 252, 13, 30, 47, 64, 81, 98, 115, 132, 149, 166, 183, 200, 217, 234
};
static const unsigned char b[] = {
    43, 20, 8, 1, 24, 227, 171, 225, 178, 183, 140, 112, 138, 119, 42, 52, 4, 54, 20, 16, 194, 225, 207, 139, 189, 181, 49, 22
};

static unsigned char key_for_pos(size_t i)
{
    return (unsigned char)((i * 31 + 13) & 0xFF);
}

int main(void)
{
    puts("What's the password?");

    char strvar[128];
    if (!fgets(strvar, (int)sizeof strvar, stdin))
        return 1;

    strvar[strcspn(strvar, "\r\n")] = '\0';

    size_t len = strlen(strvar);
    if (len != expected_len)
    {
        puts("Get out!");
        return 0;
    }

    for (size_t i = 0; i < len; ++i)
    {
        unsigned char k = key_for_pos(i);
        if (((unsigned char)strvar[i] ^ k) != obf[i])
        {
            puts("Get out!");
            return 0;
        }
    }

    const size_t flag_len = sizeof a / sizeof a[0];
    char flag[64];
    for (size_t i = 0; i < flag_len; ++i)
        flag[i] = (char)(a[i] + b[i]);

    if (flag_len < sizeof flag)
        flag[flag_len] = '\0';

    puts(flag);

    return 0;
}