#include <unistd.h>
#include <stdlib.h>

// gcc -o reload_postfix reload_postfix.c
// chown root reload_postfix
// chmod +s reload_postfix

int main( int argc, char **argv ) {
    setuid( geteuid() );
    system("/etc/init.d/postifx reload");
}
