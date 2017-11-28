#include <stdio.h>
#include <string.h>
#include <malloc.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <stdlib.h>

#include "nntpmlib.h"

/************************************************************************/
/* some auxilliary functions */

/* allocates memory for a new article_t and initializes it with empty and
   null values */
article_t *new_article_t ()
{
  article_t *a=(article_t*)malloc(sizeof(article_t));
  memset (a, '\0', sizeof(article_t));
  return a;
}

/* frees memory allocated by a and all it strings */
void free_article_t (article_t *a)
{
  if (a->subject)    free(a->subject);
  if (a->from)       free(a->from);
  if (a->id)         free(a->id);
  if (a->newsgroups) free(a->newsgroups);
  if (a->date)       free(a->date);
  if (a->references) free(a->references);
  if (a->fu2)        free(a->fu2);
  if (a->reply_to)   free(a->reply_to);
  free(a);
  return;
}


article_t *copy_article_t (const article_t *a)
{
  article_t *b=new_article_t ();
  if (a->subject)    b->subject    =strdup(a->subject);
  if (a->from)       b->from       =strdup(a->from);
  if (a->id)         b->id         =strdup(a->id);
  if (a->newsgroups) b->newsgroups =strdup(a->newsgroups);
  if (a->date)       b->date       =strdup(a->date);
  if (a->references) b->references =(a->references);
  if (a->fu2)        b->fu2        =strdup(a->fu2);
  if (a->reply_to)   b->reply_to   =strdup(a->reply_to);
  b->lines   =a->lines;
  b->no      =a->no;
  b->bytes   =a->bytes;
  return b;
}


/* prints the data in article_t to stdout */
void printf_article_t (article_t *a)
{
  printf ("Subject      : %s\n", a->subject);
  printf ("From         : %s\n", a->from);
  printf ("Message-ID   : %s\n", a->id);
  printf ("Newsgroups   : %s\n", a->newsgroups);
  printf ("Date         : %s\n", a->date);
  printf ("References   : %s\n", a->references);
  printf ("Follow-up-to : %s\n", a->fu2);
  printf ("Reply-to     : %s\n", a->reply_to);
  printf ("Lines        : %i\n", a->lines);
  printf ("Bytes        : %li\n", a->bytes);
  printf ("(number      : %li)\n", a->no);
  return;
}




/* allocates memory for an group_t and initializes it with 0 */
group_t *new_group_t ()
{
  group_t *g=(group_t*)malloc(sizeof(group_t));
  memset (g, '\0', sizeof(group_t));
  return g;
}

void free_group_t (group_t *g)
{
  if (g->name) free (g->name);
  free(g);
  return;
}

void printf_group_t (group_t *g)
{
  printf ("Group   : %s\n", g->name);
  printf ("  first : %li\n", g->first);
  printf ("  last  : %li\n", g->last);
  printf ("  posting %sallowed\n", (g->flags & POSTING_ALLOWED) ? "" : "not ");
  return;
}


/* The parameters may contain e.g. name="Subject:" and value="Re: some article"
   The function inserts this information into the right place in the
   article_t a.
   Returns 0, if the info could be inserted. -1 otherwise.
   The inserted value is newly allocated.
   The colon at the end of "name" is important.*/
int insert_value_into_article_t (article_t *a, 
				 const char *name, const char *value)
{
  int res=0;

  if ((name==NULL) || (a==NULL)) return -1;

  if (strcasecmp(name,"subject:")   ==0) a->subject   =strdup(value); else
  if (strcasecmp(name,"from:")      ==0) a->from      =strdup(value); else
  if (strcasecmp(name,"date:")      ==0) a->date      =strdup(value); else
  if (strcasecmp(name,"message-id:")==0) a->id        =strdup(value); else
  if (strcasecmp(name,"lines:")     ==0) a->lines     =atoi(value);   else
  if (strcasecmp(name,"bytes:")     ==0) a->bytes     =atol(value);   else
  if (strcasecmp(name,"references:")==0) a->references=strdup(value); else
  if (strcasecmp(name,"newsgroups:")==0) a->newsgroups=strdup(value); else
  if (strcasecmp(name,"follow-up-to:")==0) a->fu2     =strdup(value); else
  if (strcasecmp(name,"reply-to:")  ==0) a->reply_to  =strdup(value); else
    res=-1;

  return res;
}


/* line contains a line of an article-header. The function parses it and
   inserts the iformation contained in it into the article_t a.
   Return 0, if something was inserted, -1 otherwise. */
int parse_article_header_line (article_t *a, const char *line)
{
  char *p;
  int res;

  p=strchr(line, ' ');
  if (p==NULL) return -1;
  *p='\0';
  res=insert_value_into_article_t (a, line, p+1);
  *p=' ';
  return res;
}


/************************************************************************/
/* communication with the server */

/* trunctates line at the first linefeed or return. Returns 1, if the 
   line was truncated, 0 if none of the two chars as found. */
int truncate_newline (char *line)
{
  char *p=line;
  int res;
  if (strchr(line,'\n')) res=1;
  else res=0;

  while ((*p) && (*p!='\r') && (*p!='\n')) p++;
  if (*p) *p='\0';
  return res;
}


/* reads a line from ns. Deletes returns and newlines at the end, and
   returns the line in a new allocated string.
   processes lines beginning with .
   If the line (containing only a .) is the last line from server, the
   function return NULL and sets (if fin!=NULL) *fin=1, otherwise *fin=0.
   In case of an error NULL is returned too, but *fin isn't set. */
char *get_line_from_server (nntp_server *ns, int *fin)
{
  int buflen=EXPECTED_MAXLINE;
  char *line=(char*)malloc(sizeof(char)*buflen), *p;

  if (fin) *fin=0;

  /* read until a newline or a return comes. resize the allocated memroy
     if necessary */
  if (fgets (line, EXPECTED_MAXLINE, ns->fin)==NULL) {free(line); return NULL;}
    while (!truncate_newline(line)) {
      line=(char*)realloc(line,buflen+=EXPECTED_MAXLINE);
      p=line+strlen(line);
      if (fgets(p, EXPECTED_MAXLINE, ns->fin)==NULL) {free(line); return NULL;}
    }

  /* was this the end? */
  if (strcmp(line,".")==0) {
    free(line);
    if (fin) *fin=1;
    line=NULL;
  }
  else {
    /* if line begins witz two points, remove the first */
    if ((line[0]=='.') && (line[1]=='.')) {
      p=line+1;
      do *p=*(p+1);
      while (*(++p));
    }
  }

  return line;
}


/* reads from server, until the transmission is over. Saves all lines in
   a NULL-terminated array of char*, which is returned.
   In approx_lines the approcimate number of lines should be given. If the
   allocated memory isn't sufficient, it is enlarged by 50%. If 
   approx_lines==0, a default-value is used.
   If no_lines is !=NULL, the number of lines read is returned therein. */
char **get_lines_from_server (nntp_server *ns, int approx_lines, int *no_lines)
{
  char **res;
  int i=0;

  if (approx_lines==0) approx_lines=30;
  res=(char**)malloc(sizeof(char*)*approx_lines);

  while ((res[i]=get_line_from_server(ns, NULL))) {
    i++;
    if (i>=approx_lines) {
      approx_lines=approx_lines*1.5+1;
      res=realloc(res, sizeof(char)*approx_lines);
    }
  }

  if (no_lines) *no_lines=i-1;
  return res;
}



/* reads the return-line of the server. 
   If response!=NULL, *response will contain this line (new allocated).
   If rcode!=NULL, *rcode will contain the (numerical) return code of the 
      server.
   In ok_codes a NULL-terminated array with positive responses has to be
      given. In err_codes a NULL-terminated array with negative responses.
   If all is ok, the function return 0. In an other case the return-code
      of the server. If another error occurs, -1.
   ok_codes and err_codes do not have to contain 4xx and 5xx responses. */
int read_server_response (nntp_server *ns, char **response, int *rcode,
			  int *ok_codes, int *err_codes,
			  void (*log_func)(char*),
			  void (*error_func)(char*))
{
  int fin, rc, i, codetype=0;
  char *line, line3;

  if ((ns==NULL) || (ns->fin==NULL) || (ns->fout==NULL)) {
    if (error_func) error_func (ERR_NOCONNECTION);
    return -1;
  }

  if ((line=get_line_from_server(ns,&fin))==NULL) { /* error */
    if (error_func) error_func (ERR_NORESPONSE);
    return -1;
  }

  if (response) *response=strdup(line);
  if (log_func) log_func(line);

  /* find return-code */
  line3=line[3];
  line[3]='\0';
  rc = atoi (line);
  line[3]=' ';
  if (rcode) *rcode=rc;

  /* return code ok? */
  i=0;
  while (ok_codes[i])
    {
      if (ok_codes[i]==rc) 
        {
          codetype=1;
          break;
        }
      i++;
    }

  /* return code an error? */
  if (codetype==0) {
    i=0;
    while (err_codes[i]) {
      if (err_codes[i]==rc)
	{
	  if (error_func) error_func (line);
	  codetype=2;
	  break;
	}
      i++;
    }
  }

  /* after an 400-response the server has closed the connection */
  if (rc==400) {
    fclose (ns->fin);  ns->fin =NULL;
    fclose (ns->fout); ns->fout=NULL;
    if (error_func) error_func (line);
    codetype=2;
  }

  /* after an 500-response the server didn't understand the command, but
     still responds correctly */
  if (rc>=500) {
    if (error_func) error_func (line);
    codetype=2;
  }

  /* otherwise it was in illegal response */
  if(codetype==0) {
    if (error_func) {
      error_func (ERR_ILLEGALRESPONSE);
      error_func (line);
    }
    codetype=2;
  }

  if (line) free(line);
  return ((codetype==1) ? 0 : -1);
}


/* send a command to the server and reads the reponse line. The command
   must not end with \r\n. These chars will be added by this function. */
int nntp_send_command (nntp_server *ns, char *command,
		       char **response, int *rcode,
		       int *ok_codes, int *err_codes,
		       void (*log_func)(char*),
		       void (*error_func)(char*))
{
  if ((ns==NULL) || (ns->fin==NULL) || (ns->fout==NULL)) {
    if (error_func) error_func (ERR_NOCONNECTION);
    return -1;
  }

  if (log_func) log_func(command);

  fprintf (ns->fout, "%s\r\n", command);
  fflush (ns->fout);

  return (read_server_response (ns, response, rcode, ok_codes, err_codes,
				log_func, error_func));
}



/* connects to a nntp-server. 
   Return NULL in case of an error, otherwise a pointer to a new
      nntp_server structure.
   If an error occurs during the making of the TCP-connection, 
      connection_error is set (if !=NULL). If the server refuses the
      connection, connection_error is set to 0. */
nntp_server *nntp_connect (const char *dst,
			   unsigned short int port,
			   void (*log_func)(char*),
			   void (*error_func)(char*),
			   int *connection_error)
{
  int  ok_codes[]={200, 201, 0};
  int err_codes[]={0};
  struct hostent *he;
  struct sockaddr_in a;
  nntp_server *ns=(nntp_server*)malloc(sizeof(nntp_server));

  /* resolve servername an initialize socket */
  if (port==0) port=NNTP_DEFAULT_PORT;

  if (!(he=gethostbyname(dst))) {
    char *tmp=strdup(hstrerror(h_errno));
    if (error_func) error_func(tmp);
    free(tmp);
    free (ns);
    if (connection_error) *connection_error=1;
    return NULL;
  }

  if ((ns->fdin=socket(AF_INET,SOCK_STREAM,0))==-1) {
    if (error_func) error_func(strerror(errno));
    free(ns);
    if (connection_error) *connection_error=1;
    return NULL;
  }

  a.sin_family=AF_INET;
  a.sin_port=htons(port);
  a.sin_addr=*((struct in_addr*)he->h_addr);
  bzero(&(a.sin_zero),8);

  /* connect */
  if (connect(ns->fdin,(struct sockaddr*)&a, sizeof(struct sockaddr))==-1) {
    if (error_func) error_func(strerror(errno));
    close (ns->fdin);
    free(ns);
    if (connection_error) *connection_error=1;
    return NULL;
  }

  /* connect filedescriptors mit a FILE* */
  ns->fin =fdopen(ns->fdin,"r");
  if ((ns->fdout=dup(ns->fdin))==-1) {
    if (error_func) error_func(strerror(errno));
    close (ns->fdin);
    free(ns);
    if (connection_error) *connection_error=1;
    return NULL;
  }
  ns->fout=fdopen(ns->fdout,"w");
  if ((!ns->fin)||(!ns->fout)) {
    if (error_func) error_func(strerror(errno));
    close (ns->fdin);
    free(ns);
    if (connection_error) *connection_error=1;
    return NULL;
  }

  /* now we are reade, and the greeting line of the server can be read. */
  read_server_response (ns, NULL, NULL, ok_codes, err_codes, 
			log_func, error_func);
  if (connection_error) *connection_error=0;
  return ns;
}


/* send the "quit" to the server an closes the tcp-connection.
   frees the memory allocated by the nntp_server */
void nntp_close (nntp_server *ns,
		 void (*log_func)(char*),
		 void (*error_func)(char*))
{
  int  ok_codes[]={205, 0};
  int err_codes[]={0};

  if (nntp_send_command (ns, "QUIT", NULL, NULL, ok_codes, err_codes,
			 log_func, error_func)==0) {
    fclose (ns->fin);
    fclose (ns->fout);
    free(ns);
  }
  return;
}


/* sets the actual group. If n, f, l are different from NULL, the following
   number are returns in it:
   n : approx. number of articles in this group
   f : number of the first article
   l : number of the last article */
int nntp_group (nntp_server *ns, const char *group,
		int *n, int *f, int *l,
		void (*log_func)(char*),
		void (*error_func)(char*))
{
  int  ok_codes[]={211, 0};
  int err_codes[]={411, 0};
  char *command=(char*)malloc(sizeof(char)*(strlen(group)+7));
  char *response, *p;

  sprintf (command, "GROUP %s", group);

  if (nntp_send_command(ns, command, &response, NULL, ok_codes, err_codes,
			log_func, error_func)) {  /* error */
    free(command);
    return -1;
  }

  /* parse response of form "n f l s group selected" */
  p = strchr(response, ' ')+1; if (n) *n=atoi(p);
  p = strchr(p,' ')+1;         if (f) *f=atoi(p);
  p = strchr(p,' ')+1;         if (l) *l=atoi(p);

  free (response);
  return 0;
}


/* Lets the server send a list of all his groups. This list must be read
   by the user itself. */
int nntp_list_groups (nntp_server *ns,
		      void (*log_func)(char*),
		      void (*error_func)(char*))
{
  int  ok_codes[]={215, 0};
  int err_codes[]={0};

  return (nntp_send_command (ns, "list", NULL, NULL, ok_codes, err_codes,
			     log_func, error_func));
}

/* an nntp_list_groups, but only groups created after the given time, which
      fit to "distribution" are returned.
   datetime_string must(!) have the form "YYMMDD hhmmss". Ist gmt!=0, this
      time will be considers GMT.
   distribution may contain one or more search patterns, i.e. a comma-seperated
      list of strings. The whole string has to begin with < and end with >.
      distribution may also be NULL. But datetimestring not. */
int nntp_newgroups (nntp_server *ns,
		    const char *datetime_string, int gmt,
		    const char *distribution,
		    void (*log_func)(char*),
		    void (*error_func)(char*))
{
  char *command=(char*)malloc(sizeof(char)*EXPECTED_MAXLINE);
  int  ok_codes[]={231, 0};
  int err_codes[]={0};
  int res;

  sprintf (command, "newgroups %s %s %s", datetime_string, 
	   (gmt ? "gmt" : ""), (distribution ? distribution : ""));
  res=nntp_send_command (ns, command, NULL, NULL, ok_codes, err_codes,
			 log_func, error_func);
  free(command);
  return res;
}

/* line contains a line as given by the server after the LINE-command. It
   will be parsed and the result will be written to a new allocates group_t. */
group_t *parse_list_line (char *line)
{
  char *p, *q;
  group_t *g=(group_t*)malloc(sizeof(group_t));

  q=strchr (line, ' ');
  if (q==NULL) {free(g); return NULL;}
  p=q+1;

  g->first=atol(p);
  p=strchr(p, ' ')+1;
  if (p==NULL) {free(g); return NULL;}
  g->last=atol(p);
  p=strchr(p, ' ')+1;
  if (p==NULL) {free(g); return NULL;}
  switch (*p) {
  case 'y':
  case 'Y':
    g->flags=POSTING_ALLOWED;
    break;
  case 'n':
  case 'N':
    g->flags=0;
    break;
  default:
    break;
  }

  *q='\0';
  g->name=strdup(line);
  *q=' ';

  return g;
}


/* send a xover-command to the server. min_no and max_no may contain an
   article-region:
     min_no==-1, max_no==-1 : no region is given (doesn't function on many
                              server)
     min_no==max_no!=-1     : the region contains only this article
     min_no!=-1, max_no==-1 : all articles from min_no
     min_no!=-1, max_no!=-1 : articles from min_no to max_no */
int nntp_xover (nntp_server *ns, int min_no, int max_no,
		void (*log_func)(char*),
		void (*error_func)(char*))
{
  char *command=(char*)malloc(sizeof(char)*EXPECTED_MAXLINE);
  int  ok_codes[]={224, 0};
  int err_codes[]={412, 420, 0};
  int res;

  /* compose command */
  if (min_no==max_no) 
    if (min_no==-1) sprintf (command, "xover"); /* both are -1 */
    else sprintf (command, "xover %i", min_no); /* both equal, but !=-1 */
  else if (max_no==-1) sprintf (command, "xover %i-", min_no);
  else sprintf (command, "xover %i-%i", min_no, max_no);

  res = nntp_send_command(ns, command, NULL, NULL, ok_codes, err_codes,
			  log_func, error_func);
  free(command);
  return res;
}


/* sends the next-command
   in n (if !=NULL) the number of the article is returned.
   in a (if !=NULL) the article-id is returned (new allocated).
   mode is either SET_TO_NEXT (next article), or
                  SET_TO_LAST (previous article). */
int nntp_next (nntp_server *ns, int *n, char **a, int mode,
	       void (*log_func)(char*),
	       void (*error_func)(char*))
{
  int  ok_codes[]={223, 0};
  int err_codes[]={412, 420, 421, 422, 0};
  int res;
  char *response, *p, *q;

  res = nntp_send_command(ns, ((mode==SET_TO_NEXT) ? "next" : "last"), 
			  &response, NULL, ok_codes, err_codes,
			  log_func, error_func);

  if (res) return res;

  /* parse respons of the form "n a article retrieved ...." */
  p = strchr(response, ' ')+1; if (n) *n=atoi(p);
  p = strchr(p,' ')+1;
  if ((q = strchr(p,' '))) *q='\0';
  if (a) *a=strdup(p);

  free (response);
  return 0;
}


/* given a line, which was sent by the server after an xover-command, the
   function parses it and inserte the result into new allocated article_t.
   In case of an error, NULL is returned. */
article_t *parse_xover_line (char *line, const char **format)
{
  const char *default_format[]={"subject:", "from:", "date:", "message-id:",
				"references:", "bytes:", "lines:", NULL};
  article_t *a;
  char *p, tmpchar;
  int i=-1;

  if (line==NULL) return NULL;
  if (format==NULL) format=default_format;
  a=new_article_t();

  while ((i==-1) || (format[i])) {
    p=strchr (line, '\t');
    if (p==NULL) {free_article_t(a); return NULL;}
    tmpchar=*p;
    *p='\0';
    if (i==-1) a->no=atol(line);
    else insert_value_into_article_t(a, format[i], line);
    *p=tmpchar;
    line=p+1;
    i++;
  }

  return a;
}



/* reads an article from server. Depending on the values of by_mode 
   the article is requested by message_id, message_no or the
   current article is requested. Depending on get_what the header, the
   body or all of the article is requested.
   In case of an error -1 is returned, otherwise 0.
   ar may be NULL, if by_mode==BY_NONE. */
int nntp_get_article (nntp_server *ns, article_t *ar,
                 int by_mode, int get_what,
                 void (*log_func)(char*),
                 void (*error_func)(char*))
{
  char *command=(char*)malloc(sizeof(char)*EXPECTED_MAXLINE);
  char *response, *p1, *p2;
  int res;
  int  ok_codes[]={220, 221, 222, 223, 0};
  int err_codes[]={412, 420, 423, 430, 0};

  command[0]='\0';

  switch (get_what) {
  case GET_HEAD:
    strcat (command,"HEAD");
    break;
  case GET_BODY:
    strcat (command,"BODY");
    break;
  case GET_ALL:
    strcat (command,"ARTICLE");
    break;
  case GET_STAT:
    strcat (command,"STAT");
    break;
  default:
    if (error_func) error_func ("wrong option \"get_what\"for get_article\n");
    free(command);
    return -1;
  }

  switch (by_mode) {
  case BY_MESSAGEID:
    strcat (command," ");
    strcat (command,ar->id);
    break;
  case BY_MESSAGENO:
    sprintf (command+strlen(command), " %li", ar->no);
    break;
  case BY_NONE:
    break;
  default:
    if (error_func) error_func ("wrong option \"by_what\"for get_article\n");
    free(command);
    return -1;
  }

  res=nntp_send_command (ns, command, &response, NULL, ok_codes, err_codes,
			 log_func, error_func);

  /* if all is ok, parse the response line and get no and message-id */
  if (res==0) {
    if (ar!=NULL) {
      p1=strchr (response, ' '); if (p1) while (*p1==' ') p1++;
      p2=strchr (p1,' '); if (p2) *p2='\0';
      ar->no=atol(p1);

      if (ar->id==NULL) {
	p1=p2+1;  while (*p1==' ') p1++;
	p2=strchr(p1,' '); if (p2) *p2='\0';
	ar->id=strdup(p1);
      }
    }
    free(response);
  }

  free(command);
  return res;
}


/* after a HEAD- or ARTICLE-command was sent, this function read the lines
   containing the article-header (until the blank line or the "."-line.),
   parses ist and inserts the information into a new allocated article_t-
   structure. */
article_t *nntp_read_header_lines (nntp_server *ns)
{
  article_t *res=new_article_t();
  char *line=NULL;

  do {
    if (line!=NULL) free(line);
    line = get_line_from_server (ns, NULL);
    if (line!=NULL) {
      if (line[0]=='\0') {
	free(line);
	line=NULL;
      }
      else parse_article_header_line (res, line);
    }
  } while (line!=NULL);

  return res;
}


/* sends a POST-command to the server.
   text has to contain a null-terminated array with the lines to be posted.
   The user has to look for himself, that they are well formated. In 
   particular the function does not add a \r\n and does not add an article
   header.
   The line ending the posting (containing only a ".") is added by the 
   function. */
int nntp_post (nntp_server *ns, const char **text,
	       void (*log_func)(char*),
	       void (*error_func)(char*))
{
  int ok1_codes[]={340, 0};
  int ok2_codes[]={240, 0};
  int err_codes[]={440, 441, 0};

  if (nntp_send_command(ns, "post", NULL, NULL, ok1_codes, err_codes,
			log_func, error_func)) return -1;

  while (*text) fprintf (ns->fout, "%s", *text++);
  fprintf (ns->fout, ".\r\n");
  fflush (ns->fout);

  if (read_server_response(ns, NULL, NULL, ok2_codes, err_codes,
			   log_func, error_func))
    return -2;
  return 0;
}


/* sends a HELP-command to the server. The list with the possible commands
   has to be read by the user himself. */
int nntp_help (nntp_server *ns, 
	       void (*log_func)(char*), void (*error_func)(char*))
{
  int  ok_codes[]={100, 0};
  int err_codes[]={0};

  return (nntp_send_command (ns, "help", NULL, NULL, ok_codes, err_codes,
			     log_func, error_func));
}


/* informs the server, whether we are are a news-reader oder a second
   news-server. */
int nntp_set_mode (nntp_server *ns, int mode, int *posting_allowed,
		      void (*log_func)(char*), void (*error_func)(char*))
{
  int ok1_codes[]={200, 201, 0};
  int ok2_codes[]={202, 0};
  int err_codes[]={0};
  int rcode, res;

  if (mode==NNTP_MODE_SLAVE) {
    res = nntp_send_command (ns, "slave", NULL, NULL,
			     ok2_codes, err_codes, log_func, error_func);
  }
  else {
    res = (nntp_send_command (ns, "mode reader", NULL, &rcode,
			      ok1_codes, err_codes, log_func, error_func));
    if (posting_allowed) {
      if (rcode==200) *posting_allowed = 1;
      else *posting_allowed = 0;
    }
  }

  return res;
}

/************************************************************************
 Changelog

 10.06.2001 Creation
 17.06.2001 HELP, MODE READER and SLAVE-commands added
 19.01.2002 Corrected a segmentation fault in get_lines_from_server.
            Corrected documentation for nntp_connect
            Changed commentaries to english

 */
