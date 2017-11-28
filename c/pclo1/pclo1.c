/*
 * This program may be distributed under the terms of the BSD licence
 * which can be found at http://www.opensource.org/licences/bsd-licence.html
 * (c) 2001 by Michael Becker
 */

#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include "pclo1.h"

/* 
 * This functions parses the command-line for given options.
 * In argv and argc the command-line is given as for main.
 * co is an array with the possible options. It ends with an entry,
 * where the short name of the option is NULL. (s. below for example!)
 *
 * Every option must have a short name and a long name, and a number
 * of required arguments (may be -1 for "arbitrary").
 *
 * The function parses the command-line at the beginning. When it
 * encounters an argument which isn't an option, it stops. All 
 * arguments following are given back as NULL-terminated array
 * *last_vals.
 *
 * "--" says: no more options follows.
 *
 * When successfull, the function return 0, else a bitwise combination
 * of the error-codes defined in pclo1.h.
 *
 * When several options are given, the order is irrelevant. In the
 * command-line a options must not exist twice.
 *
 * If option i was set, the 
 *   int co[i].changed     is !=0.
 *   char **co[i].value    contains an NULL-terminated array of the
 *                         Arguments given for the option.
 *
 * (S. below for examples!)
 */
int parse_commandline_options1 (cl1_option_t co[], char ***res, 
                                char ***last_vals, int argc, char *argv[])
{
  int i, error=0, no_of_vals;
  char **p, **q, *optname;

  /* are res and last_vals set? */
  if ((res==NULL) || (last_vals==NULL) || (argv==NULL) || (co==NULL)) 
    return PCLO1_NULL_PARAMS;

  /* first we copy argv */
  *res=(char**)malloc((argc+1)*sizeof(char*));
  for (i=1; i<argc; i++) {
    (*res)[i-1] = strdup(argv[i]);
  }
  (*res)[argc-1]=(*res)[argc]=NULL;

  *last_vals = NULL;
  p=*res;
  while (*p) {
    /* if *p is not an option, we are ready */
    if ((*p)[0]!='-') {
      /* if there were options before we need a NULL-pointer to mark the
         beginning of the rest. We simply shift it all */
      q=*res+argc;
      while (q!=p) {
        *q=*(q-1);
        q--;
      }
      *p=NULL;
      *last_vals = p+1;
      return error;
    }

    /* if *p is -- we are ready too */
    if (strcmp(*p, "--")==0) {
      free (*p);
      *p = NULL;
      *last_vals = p+1;
      return error;
    }

    /* *p is a option, we try to find it */
    optname = *p;
    while (*optname=='-') optname++;
    for (i=0; co[i].short_name; i++) {
      if ((strcmp(co[i].short_name, optname)==0) ||
          ((co[i].long_name) && (strcmp(co[i].long_name,  optname)==0))) break;
    }

    if (co[i].short_name) { /* option was found */
      if (co[i].changed) /* option was already set by user */
        error |= PCLO1_DOUBLE_OPTION;
      co[i].changed = 1;
      free (*p);
      *p = NULL;
      p++;
      co[i].value = p;
      no_of_vals = co[i].no_arg;
      while ((*p) && ((*p)[0]!='-') &&
             ((no_of_vals>0) || (co[i].no_arg==-1))) {
        no_of_vals--;
        p++;
      }
      /* if still no_of_vals is >0, there weren't enough values */
      if (no_of_vals>0) {
        error |= PCLO1_WRONG_NO_OF_ARGS;
      }

    }
    else { /* no option was found */
      error |= PCLO1_UNKNOWN_OPTION;
      *last_vals = p;
      return error;
    }
  }

  *last_vals = p;
  return error;
}

/* free's the memory as allocated by parse_commandline_options1 */
void free_arguments (int argc, char **res)
{
  int i;
  for (i=0; i<=argc; i++) 
    if (res[i]) free(res[i]);
  free (res);
  return;
}


/* Example: Lets say we have the following options:

    cl1_option_t co[] = {
      {"a", "all", -1, 0, NULL},
      {"n", "none", 0, 0, NULL},
      {"s", "some", 2, 0, NULL},
      {NULL, NULL, 0, 0, NULL}};

  So there is an option "a" or "all" which takes an arbitrary number of args,
    an option "n" or "none" which takes no args, and
    an option "s" or "some" which takes exactly 2 args.

  We have a program a.out, which calls the function parse_commandline_options1:
    char **result;
    char **last_vals;
      [...]
    parse_commandline_options1 (co, &result, &last_vals, argc, argv);

  The variable result is just necessary to allocate memory for the values.
  It is not necessary for the user to read it. Only if the memory allocated
  has to be freed, it is needed (cmp. free_arguments function.)

  a.out -a 1 2 3 4
  a.out -all 1 2 3 4
  a.out ----a 1 2 3 4
    -> co[0].changed is 1 and co[0].values is an NULL-terminated array of
          strings "1", "2", "3", "4", NULL.
       co[1].changed, co[2].changed are 0 and co[1].values and co[2].values
          are NULL.

  a.out -s 1 2 -n 3 4
    -> co[1].changed and co[2].changed are 1
       co[1].values is {NULL}, co[2].values is {"1", "2", NULL}.
       last_vals is {"3", "4", NULL}.

  a.out --some 1 2 3 4 -n
    -> co[2].changed is 1.
       co[2].values is {"1", "2", NULL}.
       last_vals is {"3", "4", "-n", NULL}.

  a.out -s -n
    -> error PCLO1_WRONG_NO_OF_ARGS. (wrong number of arguments for option -s).

  a.out -n -n
    -> error PCLO1_DOUBLE_OPTION (-n -option given more than once).

  a.out -a 1 2 3 4 5 -s 6 7 8 9
    -> co[0].changed and co[2].changed are 1.
       co[0].values is {"1", "2", "3", "4", "5", NULL}.
       co[2].values is {"6", "7", NULL}.
       last_vals is {"8", "9", NULL}.

  a.out -t
    -> error PCLO1_UNKNOWN_OPTION (unknown option).

  a.out -- -s
    -> last_vals is {"-s", NULL}.

  a.out -a -- -s
    -> co[0].changed is 1 and co[0].values is {NULL}.
       last_vals is {"-s", NULL}.

*/
