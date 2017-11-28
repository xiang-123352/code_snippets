#ifndef __HTTPMLIB_H_
#define __HTTPMLIB_H_

#include <stdio.h>

#define HTTP_DEFAULT_PORT 80
#define HTTP_DEFAULT_TIMEOUT 60

typedef struct {
  char *name;
  char *value;
} http_data_t;

typedef struct {
  char *method;
  char *file;
  char *http_version;
  char *host;
  http_data_t **data; /* NULL terminated array of data */
} http_request_t;

typedef struct {
  FILE *in, *out;  /* streams for reading and writing */
  int fdin, fdout; /* the corresponding filedescs */
  unsigned short int port;
  int timeout;     /* seconds for timeout */
} http_connection_t;

typedef struct {
  int code;
  char *reason;
  char *http_version;
  http_data_t **data;
} http_response_t;

/* general */
int http_parse_link (const char *URI, char **host, char **file,
                     unsigned short int *port);

/* http_data_t */
void free_http_data (http_data_t *d);
http_data_t *new_http_data (const char *name, const char *value);
http_data_t *http_data_from_line (char *line);
void add_http_data_to_array (http_data_t ***array, http_data_t *data);
void fprintf_http_data_array (FILE *f, http_data_t **d);
char *http_get_value_by_name (http_data_t **d, const char *name);

/* http requests */
void free_http_request (http_request_t *r);
http_request_t *new_http_request (const char *method, const char *file,
                                  const char *http_version, const char *host);
void http_request_add_data (http_request_t *r, const char *name, 
                            const char *value);
void http_request_add_authentication (http_request_t *r,
                                      const char *user, const char *password);
/* http responses */
void fprintf_http_response (FILE *f, const http_response_t *r);
void free_http_response (http_response_t *r);
http_response_t *parse_http_response (http_connection_t *c, char **err_msg);

/* low level network functions */
http_connection_t *http_connect (const char *host, unsigned short int port,
                                 char **err_msg, int timeout);
void http_close (http_connection_t *c);
int http_send_request (http_connection_t *c, http_request_t *r);

/* high level network function */
http_connection_t *http_get (const char *host, const char *file, 
                             unsigned short int port, char **err_msg,
                             http_response_t **response, int timeout);
http_connection_t *http_get_1 (const char *URI, char **err_msg, 
                               http_response_t **response, int timeout);
http_response_t *http_head  (const char *host, const char *file, 
                             unsigned short int port, char **err_msg, 
                             int timeout);
http_response_t *http_head_1 (const char *URI, char **err_msg, int timeout);


#endif

