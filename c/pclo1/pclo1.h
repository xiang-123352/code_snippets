#ifndef __pclo1_h_
#define __pclo1_h_

typedef struct {
  char *short_name;
  char *long_name;
  int no_arg;  /* number of arguments. currently ignored */
  int changed; /* is set to 1, if a option was set */
  char **value;
} cl1_option_t;

#define PCLO1_UNKNOWN_OPTION 1     /* an unknown option was given */
#define PCLO1_WRONG_NO_OF_ARGS 2   /* some option has not enough arguments */
#define PCLO1_DOUBLE_OPTION 4      /* an option was given twice */
#define PCLO1_NULL_PARAMS 8        /* there were NULL-pointers given to the fuction */

int parse_commandline_options1 (cl1_option_t co[], char ***res, 
                                char ***last_vals, int argc, char *argv[]);

void free_arguments (int argc, char **res);

#endif
