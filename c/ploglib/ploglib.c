#include <stdio.h>
#include <malloc.h>
#include <string.h>
#include <regex.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "ploglib.h"


tt_type_t subterm[] = {
  {'S', "([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})"}, 
     /* numerical IP of the client */
  {'C', "([a-zA-Z]+)"}, /* command of the client */
  {'c', "([0-9]+)"},    /* response-code of server */
  {'r', "(.*)"},        /* requested file */
  {'b', "([0-9\\-]+)"}, /* number of bytes delivered */
  {'d', "(.*)"},        /* requested domain */
  {'f', "(.*)"},        /* referrer */
  {'B', "(.*)"},        /* browser */

  {'Y', "([0-9]{4})"},    /* 4-digit yearr */
  {'M', "([0-9]{1,2})"},  /* month, 1- or 2-digits */
  {'N', "([a-zA-Z]{3})"}, /* month, 3-letter abbr. */
  {'D', "([0-9]{1,2})"},  /* day, 1- or 2-digits */
  {'E', "([a-zA-Z]{3})"}, /* day, 3-letter abbr. */
  {'h', "([0-9]{1,2})"},  /* hour, 1- or 2-digits */
  {'m', "([0-9]{1,2})"},  /* minute, 1- or 2-digits */
  {'s', "([0-9]{1,2})"},  /* second, 1- or 2-digits */
  {'\0', NULL}
};


/* tests, whether there are chars used twice in the global variable
   subterm. And whether all regular expressions are ok.
   Should be called once at the start of the program. At least if
   something was changed.
   If all things are ok, 0 is returned.
   -1, if a char is used twice.
   n, if the expression subterm[n],syntax is faulty. */
int check_subterms ()
{
  int used[256], i;
  regex_t re;

  for (i=0; i<256; i++) used[i]=0;

  i=0;
  while (subterm[i].syntax!=NULL)
    if (used[(int)(subterm[i++].letter)]++) return -1;

  for (i=0; subterm[i].syntax!=NULL; i++) {
    /* test, whether the substring is read */
    if ((subterm[i].syntax[0]!='(') ||
        (subterm[i].syntax[strlen(subterm[i].syntax)-1]!=')'))
      return i;
    /* test, whether the regular expression is ok */
    if (regcomp (&re, subterm[i].syntax, REG_EXTENDED))
      return i;
  }
  return 0;
}

/******************* functions for management of access_t ***************/

/* all strings in access_t have to be allways extra allocated. */

/* allocates memory for a new access_t and fills it with empty values. */
access_t *new_empty_access_t ()
{
  access_t *res=(access_t*)malloc(sizeof(access_t));

  res->requester =0;
  res->command   =NULL;
  res->rcode     =-1;
  res->bytes     =-1;
  res->request   =NULL;
  res->domain    =NULL;
  res->referrer  =NULL;
  res->browser   =NULL;

  res->dateY =-1;
  res->dateM =-1;
  res->dateD =-1;
  res->timeH =-1;
  res->timeM =-1;
  res->timeS =-1;

  return res;
}


/* frees all memory used by an access_t* */
void free_access_t (access_t *a)
{
  if (a==NULL) return;

  if (a->command)  free (a->command);
  if (a->request)  free (a->request);
  if (a->domain)   free (a->domain);
  if (a->referrer) free (a->referrer);
  if (a->browser)  free (a->browser);

  free (a);
  return;
}

/* makes a deep copy of an access_t */
access_t *copy_access_t (access_t *a)
{
  access_t *res=new_empty_access_t();

  res->requester = a->requester;
  if (a->command)  res->command=strdup(a->command);
  res->rcode     = a->rcode;
  res->bytes     = a->bytes;
  if (a->request)  res->request =strdup(a->request);
  if (a->domain)   res->domain  =strdup(a->domain);
  if (a->referrer) res->referrer=strdup(a->referrer);
  if (a->browser)  res->browser =strdup(a->browser);

  res->dateY = a->dateY;
  res->dateM = a->dateM;
  res->dateD = a->dateD;
  res->timeH = a->timeH;
  res->timeM = a->timeM;
  res->timeS = a->timeS;

  return res;
}


/* compares two access_t. If they are equal, -1 is return, otherwise 0 */
int access_t_equal (access_t *a1, access_t *a2)
{
  if (a1->timeS != a2->timeS) return 0;
  if (a1->timeM != a2->timeM) return 0;
  if (a1->timeH != a2->timeH) return 0;
  if (a1->dateD != a2->dateD) return 0;
  if (a1->dateM != a2->dateM) return 0;
  if (a1->dateY != a2->dateY) return 0;

  if (a1->bytes != a2->bytes) return 0;
  if (a1->rcode != a2->rcode) return 0;
  if (a1->requester != a2->requester) return 0;

  if (strcmp (a1->request, a2->request )) return 0;
  if (strcmp (a1->domain,  a2->domain  )) return 0;
  if (strcmp (a1->referrer,a2->referrer)) return 0;
  if (strcmp (a1->browser, a2->browser )) return 0;
  if (strcmp (a1->command, a2->command )) return 0;

  return -1;
}


/* outputs the access_t without any further information */
void fprint_access_t (FILE *f, access_t *a)
{
  fprintf (f, "%lu\n", a->requester);
  fprintf (f, "%s\n", a->command);
  fprintf (f, "%i\n", a->rcode);
  fprintf (f, "%i\n", a->bytes);
  fprintf (f, "%s\n", a->request);
  fprintf (f, "%s\n", a->domain);
  fprintf (f, "%s\n", a->referrer);
  fprintf (f, "%s\n", a->browser);

  fprintf (f, "%i\n", a->dateY);
  fprintf (f, "%i\n", a->dateM);
  fprintf (f, "%i\n", a->dateD);
  fprintf (f, "%i\n", a->timeH);
  fprintf (f, "%i\n", a->timeM);
  fprintf (f, "%i\n", a->timeS);
  return;
}


/* reads an access_t, which was written with fprint_access_t an returns
   it newly allocated.
   If an io-error or if the file ends, NULL is returned. */
access_t *fscan_access_t (FILE *f)
{
  access_t *res=new_empty_access_t();
  char line[BUFSIZ];
  int ok=0;

  char *truncate_newline (char *s)
    {
      int tmp=strlen(s)-1;
      if ((tmp>=0) && (s[tmp]=='\n')) s[tmp]='\0';
      return s;
    }

  if (fgets (line, BUFSIZ, f)) {res->requester = atol(line); ok++;}
  if (fgets (line, BUFSIZ, f)) {res->command = strdup(truncate_newline(line));
    ok++;}
  if (fgets (line, BUFSIZ, f)) {res->rcode = atoi(line); ok++;}
  if (fgets (line, BUFSIZ, f)) {res->bytes = atoi(line); ok++;}
  if (fgets (line, BUFSIZ, f)) {res->request = strdup(truncate_newline(line));
    ok++;}
  if (fgets (line, BUFSIZ, f)) {res->domain = strdup(truncate_newline(line));
    ok++;}
  if (fgets (line, BUFSIZ, f)) {res->referrer = strdup(truncate_newline(line));
    ok++;}
  if (fgets (line, BUFSIZ, f)) {res->browser = strdup(truncate_newline(line));
    ok++;}

  if (fgets (line, BUFSIZ, f)) {res->dateY = atoi(line); ok++;}
  if (fgets (line, BUFSIZ, f)) {res->dateM = atoi(line); ok++;}
  if (fgets (line, BUFSIZ, f)) {res->dateD = atoi(line); ok++;}
  if (fgets (line, BUFSIZ, f)) {res->timeH = atoi(line); ok++;}
  if (fgets (line, BUFSIZ, f)) {res->timeM = atoi(line); ok++;}
  if (fgets (line, BUFSIZ, f)) {res->timeS = atoi(line); ok++;}

  if (ok<14) {
    free_access_t (res);
    res=NULL;
  }
  return res;
}


/* this function adds the default-filename to all requests an refferer, which
   end with a slash. This happend, if the default-filename is set and
   independent of the ADD_DEFAULT_FILES-flag set or not. */
void add_default_files (access_t *a, logformat_t *lf)
{
  /* adds to s1 the default-filename, if s1 ends with / */
  char *alloc_strcat_dfname (char *s1)
    {
      char *res;
      int s1len;

      if (lf->default_filename==NULL) return s1;
      if ((s1==NULL) || ((s1len=strlen(s1)-1)<0)) return s1;
      if (s1[s1len]!='/') return s1;

      res=(char*)malloc(sizeof(char)*
                        (s1len+strlen(lf->default_filename)+3)),
      strcpy (res, s1);
      strcat (res, lf->default_filename);
      free (s1);
      return res;
    }

  if ((a==0) || (lf->default_filename==NULL)) return;

  a->request  = alloc_strcat_dfname (a->request);
  a->referrer = alloc_strcat_dfname (a->referrer);

  return;
}


/******************* functions for managing logformat_t ****************/

void free_logformat_t (logformat_t *lf)
{
  if (!lf) return;
  if (lf->user_format) free(lf->user_format);
  if (lf->series) free(lf->series);
  if (lf->default_filename) free(lf->default_filename);
  free (lf);
  return;
}

logformat_t *new_logformat (const char *formatstring)
{
  logformat_t *res;
  int np, newsize, chref, count;
  char *p, *q, *qend, *tmp;

  /* searches the char ch in the variable subterm[] an return its number */
  int no_of_char (char ch)
    {
      int res=0;
      while (subterm[res].syntax)
	if (subterm[res].letter==ch) return res;
	else res++;
      return -1;
    }

  if (!formatstring) return NULL;
  tmp=strdup(formatstring);

  /* count, how many percent-signs are in the string, an calculate,
     how much memory we need for the new string. */
  np=0;
  p=tmp;
  newsize=strlen(p);
  while (*p!='\0') {
    if (*p=='%') {
      np++;
      p++;
      chref=no_of_char (*p);
      if (chref==-1) {
	free (tmp);
        return NULL;
      }
      else newsize+=strlen(subterm[chref].syntax)-1;
    }
    p++;
  }

  /* initialize log_format_t */
  res=(logformat_t*)malloc(sizeof(logformat_t));
  res->user_format = strdup(formatstring);
  res->series = (int*)malloc(sizeof(int)*(np+1));
  memset (res->series, 0, sizeof(int)*(np+1));
  res->nmatch_size=np;

  res->default_filename=NULL;
  res->flags=0;

  /* now build the real regular expression in q */
  p=res->user_format;
  qend=q=(char*)malloc(sizeof(char)*(newsize+1));
  memset(q, 0, sizeof(char)*(newsize+1));
  count=0;

  while (*p) {
    if (*p=='%') {
      p++;
      chref=no_of_char(*p);
      res->series[count++]=chref;
      strcpy (qend, subterm[chref].syntax);
      qend+=strlen(qend);
    }
    else { /* if */
      *qend++=*p;
      *qend='\0';
    }
    p++;
  }

#ifdef DEBUG
  fprintf (stderr, "found %i subexpressions.\n", np);
  fprintf (stderr, "regular expression is %s\n", q);
#endif

  /* compile regular expression */
  if (regcomp(&(res->pre_rex), q, REG_EXTENDED)) { /* error */
#ifdef DEBUG
    fprintf (stderr, "error in regular expression.\n");
#endif
    free_logformat_t (res);
    res=NULL;
  }

  /* free temporary memory */
  free (q);
  free (tmp);

  /* set month- and day-abbreviations to standard values. Do not use the
     locale of the computer we run on, because webserver allways run under
     root. */
  if (res) {
    strcpy (res->mon3[ 0], "Jan");
    strcpy (res->mon3[ 1], "Feb");
    strcpy (res->mon3[ 2], "Mar");
    strcpy (res->mon3[ 3], "Apr");
    strcpy (res->mon3[ 4], "May");
    strcpy (res->mon3[ 5], "Jun");
    strcpy (res->mon3[ 6], "Jul");
    strcpy (res->mon3[ 7], "Aug");
    strcpy (res->mon3[ 8], "Sep");
    strcpy (res->mon3[ 9], "Oct");
    strcpy (res->mon3[10], "Nov");
    strcpy (res->mon3[11], "Dec");

    strcpy (res->day3[ 0], "Sun");
    strcpy (res->day3[ 1], "Mon");
    strcpy (res->day3[ 2], "Tue");
    strcpy (res->day3[ 3], "Wed");
    strcpy (res->day3[ 4], "Thi");
    strcpy (res->day3[ 5], "Fri");
    strcpy (res->day3[ 6], "Sat");
  }

  return res;
}

/* sets the 3-letter abbr. of the month. new_month has to contain at least
   12 strings. */
void change_month_abbrevs (logformat_t *lf, char **new_months)
{
  int i;

  for (i=0; i<12; i++) {
    strncpy (lf->mon3[i], new_months[i], 3);
    lf->mon3[i][3]='\0';
  }
  return;
}


/* as change_month_abbrev, only for the day-abbr. */
void change_days_abbrevs (logformat_t *lf, char **new_days)
{
  int i;

  for (i=0; i<7; i++) {
    strncpy (lf->day3[i], new_days[i], 3);
    lf->day3[i][3]='\0';
  }
  return;
}


/* looks for the day-abbreviation in the abbreviations of lf and returns
   the number of the day. 0=sunday. 
   Return -1, if nothing was found. */
int find_day3_abbrev (logformat_t *lf, char *day)
{
  int i;
  for (i=0; i<7; i++)
    if (strncmp(day, lf->day3[i], 3)==0) return i;
  return -1;
}


/* as find_day3_abbrev, only for months */
int find_mon3_abbrev (logformat_t *lf, char *month)
{
  int i;
  for (i=0; i<12; i++)
    if (strncmp(month, lf->mon3[i], 3)==0) return (i+1);
  return -1;
}


/* sets the name of the default filename. Newly allocated memory is used.
   The memory for the old default filename may be freed. The value NULL
   is allowed too. */
void change_default_filename (logformat_t *lf, char *newdefault)
{
  if (lf==NULL) return;
  if (lf->default_filename) free(lf->default_filename);
  if (newdefault) lf->default_filename=strdup(newdefault);
  else lf->default_filename=NULL;
  return;
}


/* If there were a function to copy regular expressions, this would have
   been no problem. But so we have to parse all things once again. */
logformat_t *copy_logformat_t (logformat_t *lf)
{
  logformat_t *res=NULL;

  if (lf==NULL) return NULL;
  res = new_logformat (lf->user_format);

  memcpy (res->mon3, lf->mon3, sizeof(res->mon3));
  memcpy (res->day3, lf->day3, sizeof(res->day3));

  res->flags=lf->flags;
  change_default_filename (res, lf->default_filename);

  return res;
}


/********************* and now the parser itself *******************/

/* parses a line with help of the given log-format and writes the
   result to a newly allocated access_t. In case of an error NULL
   is returnd. It is possible (even probable), that not all entries
   of the result are set. */
access_t *parse_log_line (char *line, logformat_t *lf)
{
  access_t *res=NULL;
  regmatch_t matchptr[lf->nmatch_size+1];
  int i;
  char *tmpstr;

  /* copies a substring */
  char *substrdup (const char *from, int n)
    {
      char *tmp=(char*)malloc(sizeof(char)*(n+1)),
	*p=tmp;
      while ((n>0)&&(*from)) {
	*p=*from;
	n--;
	from++;
	p++;
      }
      *p='\0';
      return tmp;
    }

  /* so, now we parse */
  if (regexec(&(lf->pre_rex), line, lf->nmatch_size+1, matchptr, 0))
    return NULL;

  res=new_empty_access_t ();

  /* ok, things seem to have succeeded. Now we only have to fill the result
     with the right values. */
  for (i=1; i<=lf->nmatch_size; i++) {
    tmpstr = substrdup(line+matchptr[i].rm_so,
		       matchptr[i].rm_eo-matchptr[i].rm_so);
    switch (subterm[lf->series[i-1]].letter) {
    case 'S': /* IP of the client */
      res->requester=inet_addr(tmpstr);
      free (tmpstr);
      break;
    case 'C': /* command */
      res->command=tmpstr;
      break;
    case 'c': /* response code */
      res->rcode = atoi(tmpstr);
      free (tmpstr);
      break;
    case 'r': /* requested file */
      res->request = tmpstr;
      break;
    case 'b': /* bytes */
      res->bytes = atoi(tmpstr);
      break;
    case 'd': /* domain */
      res->domain = tmpstr;
      break;
    case 'f': /* referrer */
      res->referrer = tmpstr;
      break;
    case 'B': /* browser */
      res->browser = tmpstr;
      break;

      /* now the date and time */
    case 'Y':
      res->dateY = atoi (tmpstr);
      free (tmpstr);
      break;
    case 'M':
      res->dateM = atoi (tmpstr);
      free (tmpstr);
      break;
    case 'N':
      res->dateM = find_mon3_abbrev (lf, tmpstr);
      free (tmpstr);
      break;
    case 'D':
      res->dateD = atoi (tmpstr);
      free (tmpstr);
      break;
    case 'E':
      res->dateD = find_day3_abbrev (lf, tmpstr);
      free (tmpstr);
      break;
    case 'h':
      res->timeH = atoi (tmpstr);
      free (tmpstr);
      break;
    case 'm':
      res->timeM = atoi (tmpstr);
      free (tmpstr);
      break;
    case 's':
      res->timeS = atoi (tmpstr);
      free (tmpstr);
      break;

    default:
#ifdef DEBUG
      fprintf (stderr, "unimplemented character for access_t.\n");
#endif
      break;
    }
  }

  /* if necessary add default filename to request and referrer */
  if (lf->flags & LF_FLAG_EXPAND_DEFAULT_FILES) 
    add_default_files (res, lf);
  return res;
}
