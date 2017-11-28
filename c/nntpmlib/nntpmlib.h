#ifndef __nntpmlib_h_
#define __nntpmlib_h_

#include <stdio.h>

typedef struct {
  int fdin, fdout;
  FILE *fin, *fout;
} nntp_server;

#define NNTP_DEFAULT_PORT 119

#define EXPECTED_MAXLINE 200

#define ERR_NOCONNECTION     "no connection to server"
#define ERR_NORESPONSE       "can't read response from server"
#define ERR_ILLEGALRESPONSE  "illegal response from server"


typedef struct {
  char *subject, *from, *id, *newsgroups, *date, *references, *fu2, *reply_to;
  int lines;
  long no, bytes;
} article_t;


#define POSTING_ALLOWED 1

typedef struct {
  char *name;
  long int first, last;
  int flags;
} group_t;

article_t *new_article_t ();
void free_article_t (article_t *a);
article_t *copy_article_t (const article_t *a);
void printf_article_t (article_t *a);
int insert_value_into_article_t (article_t *a, 
				 const char *name, const char *value);
int parse_article_header_line (article_t *a, const char *line);


group_t *new_group_t ();
void free_group_t (group_t *g);
void printf_group_t (group_t *g);



char *get_line_from_server (nntp_server *ns, int *fin);
char **get_lines_from_server (nntp_server *ns, int approx_lines,int *no_lines);

int read_server_response (nntp_server *ns, char **response, int *rcode,
			  int *ok_codes, int *err_codes,
			  void (*log_func)(char*),
			  void (*error_func)(char*));
int nntp_send_command (nntp_server *ns, char *command,
		       char **response, int *rcode,
		       int *ok_codes, int *err_codes,
		       void (*log_func)(char*),
		       void (*error_func)(char*));

nntp_server *nntp_connect (const char *dst,
			   unsigned short int port,
			   void (*log_func)(char*),
			   void (*error_func)(char*),
			   int *connection_error);
void nntp_close (nntp_server *ns,
		 void (*log_func)(char*),
		 void (*error_func)(char*));



int nntp_group (nntp_server *ns, const char *group,
		int *n, int *f, int *l,
		void (*log_func)(char*),
		void (*error_func)(char*));

int nntp_list_groups (nntp_server *ns,
		      void (*log_func)(char*),
		      void (*error_func)(char*));
int nntp_newgroups (nntp_server *ns,
		    const char *datetime_string, int gmt,
		    const char *distribution,
		    void (*log_func)(char*),
		    void (*error_func)(char*));
group_t *parse_list_line (char *line);



int nntp_xover (nntp_server *ns, int min_no, int max_no,
		void (*log_func)(char*),
		void (*error_func)(char*));
article_t *parse_xover_line (char *line, const char **format);

#define SET_TO_NEXT 0
#define SET_TO_LAST 1
int nntp_next (nntp_server *ns, int *n, char **a, int mode,
	       void (*log_func)(char*),
	       void (*error_func)(char*));


#define BY_MESSAGEID 2
#define BY_MESSAGENO 1
#define BY_NONE 0

#define GET_HEAD 0
#define GET_BODY 1
#define GET_ALL 2
#define GET_STAT 3

int nntp_get_article (nntp_server *ns, article_t *ar,
                 int by_mode, int get_what,
                 void (*log_func)(char*),
                 void (*error_func)(char*));

article_t *nntp_read_header_lines (nntp_server *ns);

int nntp_post (nntp_server *ns, const char **text,
	       void (*log_func)(char*),
	       void (*error_func)(char*));

int nntp_help (nntp_server *ns, 
	       void (*log_func)(char*), void (*error_func)(char*));

#define NNTP_MODE_READER 0
#define NNTP_MODE_SLAVE 1
int nntp_set_mode_reader (nntp_server *ns, int mode, int *posting_allowed,
			  void (*log_func)(char*), void (*error_func)(char*));



#endif
