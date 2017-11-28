#include <malloc.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <netdb.h>
#include <netinet/in.h>
#include <errno.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/socket.h>

#include "httpmlib.h"


/**************************** auxilliary functions *************************/

/* this is an auxilliary function for concatenating strings: Append s2 to *s1.
   *s1 may be NULL, s2 not.  */
static void http_add_msg (char **s1, const char *s2)
{
  int len=strlen(s2)+1;
  char *res=NULL;

  if (s1==NULL) return;
  if (*s1) len+=strlen(*s1);
  res=(char*)malloc(sizeof(char)*len);
  *res='\0';
  if (*s1) {
    strcpy (res, *s1);
    free (*s1);
  }
  strcat (res, s2);
  *s1=res;
  return;
}

/* shifts s */
static void http_skip_leading_blanks (char *s)
{
  char *p=s;
  while (*p==' ') p++;
  while (*p) (*s++ = *p++);
  *s='\0';
  return;
}

/* removes trailing newlines and carriage returns */
static void http_remove_newline (char *s)
{
  char *p=s+strlen(s)-1;
  while ((p>=s) && ((*p=='\n') || (*p=='\r'))) *p-- = '\0';
  return;
}

/* that's just an alarm signal handler for interrupting system calls */
static void httpmlib_timeout_sig_handler (int signo)
{
  return;
}

/* parses a string like http://www.somewhere.de:8080/sub1/index.html and
   splits it into host, port and file (includind possible cgivars). 
   In case of an error, -1 is returned.
   If no port was found, it is set to 80.
   None of the pointers passed may be NULL. All strings are new allocated. */
int http_parse_link (const char *URI, char **host, char **file,
                      unsigned short int *port)
{
  char *start, *s, *pos;

  if (URI==NULL) return -1;
  start = s = strdup(URI);

  if (strncasecmp(s, "http://", 7)==0) s+=7;

  if ((pos = strchr(s, '/'))==NULL) *file=strdup("/");
  else {
    *file=strdup(pos);
    *pos='\0';
  }

  *host=strdup(s);
  if ((pos=strchr(*host, ':'))==NULL) *port=80;
  else {
    *pos='\0';
    *port = atoi (pos+1);
  }

  free (start);
  return 0;
}


/* we need an own function for setting signal handlers to prevent 
   the automatic restart of system calls. 
   Directly taken from Stevens I. Doesn't work on Solaris. */
static void (*httpmlib_signal_intr(int signum, void (*handler)(int)))(int)
{
  struct sigaction act, oact;
  act.sa_handler = handler;
  sigemptyset (&act.sa_mask);
  act.sa_flags = 0;
  if (sigaction(signum, &act, &oact)<0) return SIG_ERR;
  return (oact.sa_handler);
}



/* encodes osrc and writes the coded string into dst, which has to be big
   enough. */
static void httpmlib_base64_encode (char *dst, const char *osrc)
{
  int dstlen, srclen=strlen(osrc), mod;
  const char *endpos, *spos;
  char *dpos;
  char src[srclen+3];

  int map (int c) {
    c &= 077;
    if (c<26) return (c+'A');
    if (c<52) return (c-26+'a');
    if (c<62) return (c-52+'0');
    if (c<63) return ('+');
    return ('/');
  }

  strncpy (src, osrc, srclen);
  src[srclen] = src[srclen+1] = src[srclen+2] = 0;
  endpos = src+srclen;

  for (dstlen=0, dpos=dst, spos=src; 
       spos<endpos;
       dstlen+=4, dpos+=4, spos+=3) {
    dpos[0] = map(spos[0]>>2);
    dpos[1] = map(spos[0]<<6 | spos[1]>>4);
    dpos[2] = map(spos[1]<<2 | spos[2]>>6);
    dpos[3] = map(spos[2]);
  }

  mod = srclen % 3;
  if ((mod>=1) && (dstlen>0)) dst[dstlen-1]='=';
  if ((mod==1) && (dstlen>0)) dst[dstlen-2]='=';

  dst[dstlen]='\0';
  return;
}

/********************************* http data *******************************/

void free_http_data (http_data_t *d)
{
  if (d->name)  free(d->name);
  if (d->value) free(d->value);
  free (d);
  return;
}


/* allocates a new http_data_t with the given data */
http_data_t *new_http_data (const char *name, const char *value)
{
  http_data_t *res=(http_data_t*)malloc(sizeof(http_data_t));
  res->name = strdup(name);
  if (value) res->value=strdup(value);
  else res->value=NULL;
  return res;
}

/* makes a new allocated http_data_t* from a line of the form "name: value" 
   Returns NULL in case of an error. */
http_data_t *http_data_from_line (char *line)
{
  http_data_t *res;
  char *pos;

  if ((pos=strchr(line, ':'))==NULL) return NULL;

  *pos='\0';

  res = (http_data_t*)malloc(sizeof(http_data_t));
  res->name  = strdup (line);
  http_skip_leading_blanks (res->name);
  res->value = strdup (pos+1);
  http_skip_leading_blanks (res->value);

  *pos=':';
  return res;
}


/* adds the given data to the NULL-terminated array (*array). If data is 
   NULL, nothing is done. No checks, whether the data already exists, are
   done. */
void add_http_data_to_array (http_data_t ***array, http_data_t *data)
{
  int i;
  if (data==NULL) return;

  for (i=0; (*array)[i]; i++);
  *array = realloc(*array, sizeof(http_data_t*)*(i+3)); /* +2 should reach */
  (*array)[i] = data;
  (*array)[i+1]=NULL;

  return;
}

void fprintf_http_data_array (FILE *f, http_data_t **d)
{
  int i;
  for (i=0; d[i]; i++)
    fprintf (f, "%s: %s\r\n", d[i]->name, d[i]->value);
  return;
}

/* returns a pointer to the value of the attribute with name name. or NULL,
   if nothing was found. The search is case insensitive */
char *http_get_value_by_name (http_data_t **d, const char *name)
{
  int i;
  for (i=0; d[i]; i++)
    if (strcasecmp(name, d[i]->name)==0)
      return d[i]->value;
  return NULL;
}


/********************** http requests and responses  **********************/

/* free the memory allocated by an http-request */
void free_http_request (http_request_t *r)
{
  int i;

  if (r->method)       free(r->method);
  if (r->file)         free(r->file);
  if (r->http_version) free(r->http_version);
  if (r->host)         free(r->host);
  if (r->data) {
    for (i=0; (r->data)[i]; i++)
      free_http_data ((r->data)[i]);
    free (r->data);
  }
  free (r);
  return;
}


/* allocates a new http_request-structure. method and host are obligatory.
   file may be NULL. If http_version is NULL, 1.1 is used. In case of an
   error NULL is returned. */
http_request_t *new_http_request (const char *method, const char *file,
                                  const char *http_version, const char *host)
{
  http_request_t *res;

  if ((method==NULL) || (host==NULL)) return NULL;
  res = (http_request_t*)malloc(sizeof(http_request_t));
  memset (res, 0, sizeof(http_request_t));

  res->method = strdup (method);
  res->host   = strdup (host);

  if (http_version) res->http_version = strdup(http_version);
  else res->http_version = strdup ("1.1");

  if (file) res->file = strdup(file);

  res->data = (http_data_t**)malloc(sizeof(http_data_t*));
  memset (res->data, 0, sizeof(http_data_t*));

  return res;
}


/* adds the name: value pair to the data of the request r. */
void http_request_add_data (http_request_t *r, const char *name, 
                            const char *value)
{
  add_http_data_to_array (&(r->data), new_http_data(name, value));
  return;
}


/* adds a Authorization field with user and password base64-encoded to the 
   data of the request. */
void http_request_add_authentication (http_request_t *r,
                                      const char *user, const char *password)
{
  char *auth_raw, *auth_enc, *value;
  int len;

  len = strlen(user)+strlen(password)+3;

  auth_raw = (char*)malloc(sizeof(char)*len);
  memset (auth_raw, 0, len);
  sprintf (auth_raw, "%s:%s", user, password);

  auth_enc = (char*)malloc(sizeof(char)*(2*len+3));
  httpmlib_base64_encode (auth_enc, auth_raw);

  value = (char*)malloc(sizeof(char)*(2*len+10));
  sprintf (value, "Basic %s", auth_enc);
  http_request_add_data (r, "Authorization", value);

  free(value);
  free(auth_enc);
  free(auth_raw);

  return;
}


void free_http_response (http_response_t *r)
{
  int i;
  if (r==NULL) return;
  if (r->reason) free(r->reason);
  if (r->http_version) free(r->http_version);
  if (r->data) {
    for (i=0; (r->data)[i]; i++)
      free_http_data ((r->data)[i]);
    free (r->data);
  }
  free (r);
  return;
}




/********************** sending commands and reading responses ***************/

/* opens a HTTP connection to the given host and port and returns it in a new
   allocated http_connect_t structure. 
   If port is 0, the default port is taken. 
   timeout is in seconds. If it is 0, no timeout is set. If timeout is -1,
      the default timeout from httpmlib.h is taken.
*/
http_connection_t *http_connect (const char *host, unsigned short int port,
                                 char **err_msg, int timeout)
{
  http_connection_t *c;
  int hosterrno, cfdin;
  struct hostent *he;
  struct sockaddr_in a;

  /* resolving hostname */
#ifdef _REENTRANT
  struct hostent he_buf;
  char buf[BUFSIZ];

  if ((gethostbyname_r (host, &he_buf, buf, BUFSIZ, &he, &hosterrno)) || 
      (he==NULL)) {
#else
  if (!(he=gethostbyname(host))) {
    hosterrno = h_errno;
#endif
    http_add_msg (err_msg, hstrerror(hosterrno));
    http_add_msg (err_msg, "\n");
    return NULL;
  }

  if ((cfdin=socket(AF_INET,SOCK_STREAM,0))==-1) {
    http_add_msg (err_msg, strerror(errno));
    http_add_msg (err_msg, "\n");
    return NULL;
  }

  if (timeout<0) timeout = HTTP_DEFAULT_TIMEOUT;
  if (port==0) port = HTTP_DEFAULT_PORT;

  a.sin_family=AF_INET;
  a.sin_port=htons(port);
  a.sin_addr=*((struct in_addr*)he->h_addr);
  bzero(&(a.sin_zero),8);

  httpmlib_signal_intr(SIGALRM, httpmlib_timeout_sig_handler);
  alarm (timeout);
  if (connect(cfdin,(struct sockaddr*)&a, sizeof(struct sockaddr))==-1) {
    alarm (0);
    if (errno==EINTR) http_add_msg (err_msg, "Timeout while connecting.\n");
    else {
      http_add_msg (err_msg, strerror(errno));
      http_add_msg (err_msg, "\n");
    }
    return NULL;
  }
  alarm (0);

  c = (http_connection_t*)malloc(sizeof(http_connection_t));
  memset (c, 0, sizeof(http_connection_t));
  c->timeout = timeout;
  c->port    = port;

  c->fdin = cfdin;
  if ((c->fdout=dup(c->fdin))==-1) {
    http_add_msg (err_msg, strerror(errno));
    http_add_msg (err_msg, "\n");
    free (c);
    return NULL;
  }
  c->in =fdopen(c->fdin,"r");
  c->out=fdopen(c->fdout,"w");
  if ((!c->in)||(!c->out)) {
    close (c->fdin);
    free (c);
    http_add_msg (err_msg, strerror(errno));
    http_add_msg (err_msg, "\n");
    return NULL;
  }

  return c;
}


/* closes a http connection */
void http_close (http_connection_t *c)
{
  if (c==NULL) return;
  close (c->fdin);
  fclose (c->out);
  fclose (c->in);
  free (c);
  return;
}


/* sends a HTTP request. The connection has to be already established. 
   This funciton does not read the answer of the server */
int http_send_request (http_connection_t *c, http_request_t *r)
{
  char cmd[BUFSIZ];

  if ((c==NULL) || (c->out==NULL) || (r==NULL)) return -1;

  if (r->file) sprintf (cmd, "%s %s HTTP/%s\r\n", r->method, r->file,
                        r->http_version);
  else sprintf (cmd, "%s HTTP/%s\r\n", r->method, r->http_version);
  fprintf (c->out, "%s", cmd);
  if (r->host) fprintf (c->out, "Host: %s\r\n", r->host);
  fprintf_http_data_array (c->out, r->data);
  fprintf (c->out, "\r\n");
  fflush (c->out);
  return 0;
}

/******************************* http responses **************************/

void fprintf_http_response (FILE *f, const http_response_t *r)
{
  if (r==NULL) return;
  fprintf (f, "HTTP/%s %i %s\n", r->http_version, r->code, r->reason);
  fprintf_http_data_array (f, r->data);
  return;
}

/* reads the server response and puts it into a new allocated http_response-
   structure. Possibly additional data, e.g. a file delivered, is not read:
   The function only reads the header of the server response.
   The connection has to be already established. */
http_response_t *parse_http_response (http_connection_t *c, char **err_msg)
{
  char line[BUFSIZ], *pos;
  http_response_t *res=NULL;

  if ((c==NULL) || (c->in==NULL)) return NULL;

  httpmlib_signal_intr(SIGALRM, httpmlib_timeout_sig_handler);
  alarm (c->timeout);
  if (fgets(line, BUFSIZ, c->in)==NULL) {
    alarm (0);
    if (errno==EINTR) http_add_msg (err_msg, "Timeout while reading.\n");
    else http_add_msg (err_msg, "Can't read from connection.\n");
    return NULL;
  }
  alarm (0);

  res = (http_response_t*)malloc(sizeof(http_response_t));
  res->data = (http_data_t**)malloc(sizeof(http_data_t*));
  res->data[0]=NULL;

  /* now line has the form  "HTTP/x.x code reason\r\n". We parse it */
  if ((pos=strchr (line, '/'))==NULL) {
    free (res);
    http_add_msg (err_msg, "Illegal response from server. No HTTP version.\n");
    return NULL;
  }
  http_remove_newline (line);

  res->http_version = strdup("\0\0\0\0");
  strncpy (res->http_version, pos+1, 3);

  pos += 4;
  while (*pos==' ') pos++;
  res->code = atoi (pos);
  pos += 4;
  res->reason = strdup(pos);

  /* now we can read and parse the rest of the answer */
  alarm (c->timeout);
  while (fgets(line, BUFSIZ, c->in)) {
    if (errno==EINTR) {
      alarm (0);
      http_add_msg (err_msg, "Timeout while reading.\n");
      break;
    }
    alarm (0);
    http_remove_newline (line);
    if (line[0]=='\0') break;

    add_http_data_to_array (&(res->data), http_data_from_line(line));
    alarm (c->timeout);
  }
  alarm (0);

  return res;
}


/****************************** high level API ******************************/

/* sends a GET command to the given server. The function returns NULL in case
   of an error, or a new allocated http_connection_t, so that the sent file
   can be read from its in-element.
   If !=NULL in response the http_response is returned. 
   If the response code of the server if !=200, no connection is returned
   an an err_msg is generated. The user has to interpret the response to
   know what happened. */
http_connection_t *http_get (const char *host, const char *file, 
                             unsigned short int port, char **err_msg,
                             http_response_t **response, int timeout)
{
  http_connection_t *c=NULL;
  http_request_t *req;
  http_response_t *res;
  char msg[BUFSIZ];

  if ((req = new_http_request ("GET", file, "1.0", host))==NULL) return NULL;
  if ((c    = http_connect (host, port, err_msg, timeout))==NULL) return NULL;
  http_send_request (c, req);
  res = parse_http_response (c, err_msg);
  if (response) *response=res;
  if (res==NULL) {
    http_close (c);
    return NULL;
  }
  if (res->code!=200) {
    sprintf (msg, "%i %s\n", res->code, res->reason);
    http_add_msg (err_msg, msg);
    http_close (c);
    return NULL;
  }
  return c;
}


/* as http_get, only that this function takes a string with http:/... */
http_connection_t *http_get_1 (const char *URI, char **err_msg, 
                               http_response_t **response, int timeout)
{
  char *file, *host;
  unsigned short int port;
  http_connection_t *res;

  if (http_parse_link (URI, &host, &file, &port)) {
    http_add_msg (err_msg, "Couldn't parse URI.\n");
    return NULL;
  }
  res = http_get (host, file, port, err_msg, response, timeout);
  free (file);
  free (host);
  return res;
}


/* sends a HEAD command to the given server. The function returns the
   response of the server in a new allocated structure, or NULL in case
   of an error. 
   If the server responds in some way or another, then no error message
   is generated. This is only done, when connection errors occur. */
http_response_t *http_head  (const char *host, const char *file, 
                             unsigned short int port, char **err_msg,
                             int timeout)
{
  http_connection_t *c=NULL;
  http_request_t *req;
  http_response_t *res;
  char msg[BUFSIZ];

  if ((req = new_http_request ("HEAD", file, "1.0", host))==NULL) return NULL;
  if ((c    = http_connect (host, port, err_msg, timeout))==NULL) return NULL;
  http_send_request (c, req);
  res = parse_http_response (c, err_msg);
  http_close (c);

  if (res && (res->code!=200)) {
    sprintf (msg, "%i %s\n", res->code, res->reason);
    http_add_msg (err_msg, msg);
  }
  return res;
}


/* as http_head, only that this function takes a string with http:/... */
http_response_t *http_head_1 (const char *URI, char **err_msg, int timeout)
{
  char *file, *host;
  unsigned short int port;
  http_response_t *res;
  if (http_parse_link (URI, &host, &file, &port)) {
    http_add_msg (err_msg, "Couldn't parse URI.\n");
    return NULL;
  }
  res = http_head (host, file, port, err_msg, timeout);
  free (file);
  free (host);
  return res;
}


/***************************************************************************

Error return codes for making connections:

number   error whie
 -1    : gethostbyname
 -2    : socket
 -3    : connect
 -4    : fdopen
 -5    : dup
 -6    : bind
 -7    : listen
 -8    : accept
 -9    : some ftp command
-10    : getsockname
-11    : fopen
-12    : timeout

*/
