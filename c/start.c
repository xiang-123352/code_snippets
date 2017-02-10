#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc >= 2)
    {
        printf("%lu\n", (long unsigned) getpid());
        if (execvp(argv[1], &argv[1]) < 0)
        {
            perror(NULL);
            return 127;
        }
    }
    return 0;
}

