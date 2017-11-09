#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>

int fs_read_data (char * fs, int seek, int len, char * data)
{
    unsigned int fd;
    int result = -1;

    if (fs != NULL)
    {
        if ((fd = open (fs, O_RDONLY)) != -1)
        {
            if (lseek (fd, seek, SEEK_SET) != -1)
            {
                if (read (fd, data, len) != -1)
                {
                    data[len] = '\0';
                    result = 0;
                }

            }
        }

        close (fd);
    }

return result;
}

int main() {

    char * fs = "/dev/scd0";
    int seek =32808;
    int len = 32;

    char * buff = NULL;
    char * volume_name = NULL;

    buff = malloc((sizeof (buff)) * (len+1));

    if (fs_read_data (fs, seek, len, buff) != -1)
    {
        if ((strncmp (buff, "NO NAME", 7) == 0) || (strncmp (buff, " ",1) == 0))
        {
            free (buff);

            buff=NULL;

            volume_name = "None";
        }
        else
        {
            volume_name = strdup (buff);
        }
    }

    printf("%s", volume_name);

    free (buff);

    buff=NULL;

    return 0;
}

