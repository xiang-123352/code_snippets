#ifndef __ploglib_h_
#define __ploglib_h_

#include <stdio.h>
#include <malloc.h>
#include <regex.h>

typedef struct {
  unsigned long int requester; /* IP of the requesting computer */
                               /* in networkbyte-order */
  char *command;               /* command (e.g. GET) */
  int rcode;                   /* return-code of the server (e.g. 200) */
  int bytes;                   /* number of delivered bytes */
  char *request;               /* what file was requested */
  char *domain;                /* domain the requested file is in */
  char *referrer;              /* from whree the surver came (ev. NULL) */
  char *browser;               /* what program he uses */

  /* date and time as numbers */
  int dateY, dateM, dateD, timeH, timeM, timeS;
} access_t;


/* every variable of the following type represents a substring of the
   regular expression, which is used for parsing the log-lines. Compare
   the global variable in the c-file. */
typedef struct {
  char letter;  /* the letter, by wich this substring can be used by a user.
                   (e.g. %s --> s) */
  char *syntax;  /* e.g. "(.*)" or "([0-9]*" */
} tt_type_t;


/* flags for logformat_t */
#define LF_FLAG_EXPAND_DEFAULT_FILES 1
/* if this flag is set, after parsing the defaultfilename is added to all
   requests and refferes, which end with an /. */

typedef struct {
  char *user_format;           /* the string as given by the user */
  regex_t pre_rex;             /* compiled regular expression */
  int *series;                 /* nullterminated array, which says, which
                                  meaning the substrings of the regular  
                                  expression have. Refers to the number in the
                                  global variable  subterm[] */
  size_t nmatch_size;          /* number of substrings in the regular 
                                  expression */
  char mon3[12][4];            /* 3-letter abbreviation of month, 0=january */
  char day3[ 7][4];            /* 3-letter abbreviation of day, 0=sunday */

  int flags;
  char *default_filename;      /* s.o. */
} logformat_t;


int check_subterms ();

access_t *new_empty_access_t ();
void free_access_t (access_t *a);
access_t *copy_access_t (access_t *a);
int access_t_equal (access_t *a1, access_t *a2);
void fprint_access_t (FILE *f, access_t *a);
access_t *fscan_access_t (FILE *f);
void add_default_files (access_t *a, logformat_t *lf);

void free_logformat_t (logformat_t *lf);
logformat_t *new_logformat (const char *formatstring);
void change_month_abbrevs (logformat_t *lf, char **new_months);
void change_days_abbrevs (logformat_t *lf, char **new_days);
int find_day3_abbrev (logformat_t *lf, char *day);
int find_mon3_abbrev (logformat_t *lf, char *month);
void change_default_filename (logformat_t *lf, char *newdefault);
logformat_t *copy_logformat_t (logformat_t *lf);

access_t *parse_log_line (char *line, logformat_t *lf);

#endif
