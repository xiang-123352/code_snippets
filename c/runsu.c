/**
 * Define this to set a fixed command to execute.
 * The shell command line preparation below does NOT
 * escape this command, but the arguments passed through
 * form the command line.
 *
 * #define FIXED_COMMAND "/usr/bin/something -a -r -g --arg file1 file2 ..."
 * #define NO_ARGS 1
 *
 * OR
 *
 * gcc -Wall runsu.c -o runsu -DNO_ARGS=1
 *
 * gcc -Wall runsu.c -o runsu -DFIXED_COMMAND='/bin/ls -lsia /dev/ *'
 *
 * -------------------------------------------------------------------------
 *
 * NOTES: - This source code is published "as is", no warranties are
 *          granted.
 *        - It is only in special cases wise to run programs as root,
 *          especially if no password is required. Consider using `sudo`
 *          (maybe editing /etc/sudoers` as well) before using the method
 *          shown here!
 *        - Consider defining fixed commands using precompiler flags instead
 *          of passing program- or script paths as argument.
 *
 * @file runsu.c
 * @license GPL2
 * @author stfwi
 */
#include <stdlib.h>
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>
 
#ifndef NO_ARGS
#define NO_ARGS (0)
#endif
#ifndef FIXED_COMMAND
#define HAS_FIXED_COMMAND (0)
#define FIXED_COMMAND ""
#else
#define HAS_FIXED_COMMAND (1)
#endif
 
int main(int argc, char** argv)
{
  struct stat st;
  int euid = getuid(), status = -1, i, is_help = 0;
  char line[512], *ps, *pl;
  const char *child;
 
  #if !HAS_FIXED_COMMAND
    child = (const char *) (((argc >= 2) && argv[1]) ? argv[1] : NULL);
    is_help = child && ((!strcmp(child, "-h")) || (!strcmp(child, "--help")));
  #else
    child = FIXED_COMMAND;
    is_help = 0;
  #endif
  #if NO_ARGS
    if (argc > (HAS_FIXED_COMMAND ? 1 : 2)) {
      fprintf(stderr, "No arguments allowed (defined as compiler flag)\n\n");
      exit(-1);
    }
  #endif
 
  /* HELP */
  if (!child || is_help) {
    if (!child) fprintf(stderr, "No program specified to run.\n");
    fprintf(stderr, "Usage: %s <program to run> [arguments]\n\n", argv[0]);
    fprintf(stderr, "  Runs a program or script as root. This script must\n");
    fprintf(stderr, "  be owned by user 'root' and group 'root', and not\n");
    fprintf(stderr, "  readable, writable or executable by anyone else.\n");
    fprintf(stderr, "  This program must be owned by root:root as well,\n");
    fprintf(stderr, "  not readable or writable by others (neither the group)\n");
    fprintf(stderr, "  and the SETUID bit must be set:\n");
    fprintf(stderr, "  (`chmod u=rwxs,g=sx,o=sx '%s'`)\n", argv[0]);
    fprintf(stderr, "  The program passes through STDOUT and STDERR, and\n");
    fprintf(stderr, "  returns the exit code of the executed child program.\n");
    fprintf(stderr, "\n");
    fprintf(stderr, "  (compiler settings: %s%s)\n", NO_ARGS ? "no arguments allowed,"
        : "", HAS_FIXED_COMMAND ? ("command=" FIXED_COMMAND) : "");
    exit(-1);
  /* CHECK MY OWN PERMISSIONS */
  } else if (!argv[0] || stat(argv[0], &st)) {
    fprintf(stderr, "Failed to get permissions of this program.\n");
    exit(-1);
  } else if (st.st_gid || st.st_uid) {
    fprintf(stderr, "This program file must be owned by root (and group root)."
        " Use chown root:root '%s'\n", argv[0]);
    exit(-1);
  } else if (!(st.st_mode & (S_IFREG | S_IRWXU | S_ISUID)) ||
      (st.st_mode & (S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH))) {
    fprintf(stderr, "This program file must have the permissions \"-rws--s--x\"."
        " Use chmod u=rwxs,g=sx,o=sx '%s'\n", argv[0]);
    exit(-1);
  /* CHECK CHILD PROGRAM PERMISSIONS */
  #if !HAS_FIXED_COMMAND
  } else if (!child || stat(child, &st)) {
    fprintf(stderr, "Failed to get permissions of '%s'.\n", child ? child : "(NULL)");
    exit(-1);
  } else if (st.st_gid || st.st_uid) {
    fprintf(stderr, "The program to run must be owned by root (and group root)."
        "Use chown root:root '%s'\n", child);
    exit(-1);
  } else if (!(st.st_mode & S_IFREG)) {
    fprintf(stderr, "The program to run must not be a link\n");
    exit(-1);
  } else if (st.st_mode & (S_IRGRP | S_IWGRP)) {
    fprintf(stderr, "The program to run must not be readable or writable by other"
        "users than root (\"-rwx------\"). Use chmod 700 '%s'\n", child);
    exit(-1);
  #endif
  /* DOUBLE CHECK CHILD PROGRAM PATH */
  } else if (child[0] != '/' && strstr(child, "./") != child) {
    fprintf(stderr, "The path of the program to run must be specified as full path"
        " (e.g. /usr/bin/...) or as relative path starting with './'\n");
    exit(-1);
  /* SWITCH USER TO ROOT */
  } else if (setuid(0) < 0) {
    fprintf(stderr, "Failed to switch to root user (setuid()<0)'\n");
    exit(-1);
  /* REMOVE ALL ENVIRONMENT INFORMATION */
  } else if (clearenv()) {
    setuid(euid);
    fprintf(stderr, "Failed remove the envoronment before executing the program'\n");
    exit(-1);
  }
 
  /* BUILD COMMAND LINE, ENCLOSE AND ESCAPE "'" */
  #define PLOK (pl < (line+(sizeof(line)/sizeof(char))-1))
  memset(line, 0, sizeof (line) / sizeof (char));
  #if HAS_FIXED_COMMAND
    strncpy(line, child, (sizeof (line) / sizeof (char)) - 1);
    pl = line + strlen(line);
    *pl++ = ' ';
  #else
    pl = line;
  #endif
 
  for (i = 1; i < argc && argv[i] && PLOK; i++) {
    *pl++ = '\'';
    if (!PLOK) break;
    for (ps = argv[i]; ps && *ps && PLOK; ps++) {
      if (*ps == '\'') {
        *pl++ = '\'';
        if (!PLOK) break;
        *pl++ = '\\';
        if (!PLOK) break;
        *pl++ = '\'';
        if (!PLOK) break;
        *pl++ = '\'';
        if (!PLOK) break;
      }
      if (!PLOK || !ps || !*ps) break;
      *pl++ = *ps;
      if (!PLOK) break;
    }
    *pl++ = '\'';
    if (!PLOK) break;
    *pl++ = ' ';
    if (!PLOK) break;
  }
  if (!PLOK) {
    setuid(euid);
    fprintf(stderr, "Command line is too long.'\n");
    exit(-1);
  } else if (pl == line || strlen(line) == 0) {
    setuid(euid);
    fprintf(stderr, "Unexpected short command line (--> BUG).'\n");
    exit(-1);
  } else if (line[strlen(line) - 1] == ' ') {
    line[strlen(line) - 1] = '\0';
  }
  #undef PLOK
  status = system(line);
  setuid(euid);
  return WEXITSTATUS(status);
}

