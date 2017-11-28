#ifndef __FTPMLIB_H_
#define __FTPMLIB_H_

#include <stdio.h>

#define LINE_LENGTH 1024
#define SERVER_DEFAULT_PORT 21
#define EXPECTED_LIST_LENGTH 20
#define FTPMLIB_TIMEOUT_DEFAULT 20
/* expected number of lines after as LIST command. Has to be >0 */


#define MODE_ACTIVE 0
#define MODE_PASSIVE 1

/* lower two bits of transmission type */
#define TTYPE_1_ASCII 0
#define TTYPE_1_IMAGE 1
#define TTYPE_1_EBCDIC 2
#define TTYPW_1_LOCAL 3
/* upper bits */
#define TTYPE_2_NONPRINT 4
#define TTYPE_2_TELNET 8
#define TTYPE_2_ASA 16

#define TMODE_STREAM 0
#define TMODE_BLOCK 1
#define TMODE_COMPRESSED 2

typedef struct {
  FILE *ccin, *ccout;               /* command channel                    */
  int fdcin, fdcout;                /* filedescriptors command-channel    */
  FILE *dcin, *dcout;               /* data channel                       */
  int fddin, fddout;                /* filedescriptors data-channel       */
                                    /* fddin is the host, fddout the server */
  int active_socket;                /* socket for data-channel */
  unsigned short int scport;        /* server-port for command (hostbyte-
                                       order  */
  unsigned short int cdport, sdport;/* client- and server-port for data 
                                       (hostbyte-order)  */
  unsigned long int dadr;           /* server-adress for data in network-
                                       byte-order */
  int mode;                         /* active or passive                  */
  int ttype;               /* transmission-type: ascii, image, ebcdic...   */
  int tmode;               /* transmission-mode: stream, block, compressed */
  int timeout;             /* timeout in seconds */
} ftp_server;



/********************************* general ********************************/

int ftp_get_response (ftp_server *fs, char **return_line,
                      char **log_msg, char **err_msg);

int ftp_send_command (ftp_server *fs, const char *command,
		      int *ok_returns, int *err_returns,
                      int *return_code, char **return_line,
                      char **log_msg, char **err_msg);


/********************** making connections, login *************************/

ftp_server *ftpserver_connect (const char *servername, unsigned short int port,
                               char **log_msg, char **err_msg);
int ftpserver_close (ftp_server *fs, char **log_msg, char **err_msg);

int ftp_logon (ftp_server *fs, const char *username, const char *password,
	       const char *account, char **log_msg, char **err_msg);


/*********************** working with directories ************************/

int ftp_change_dir (ftp_server *fs, int up, const char *path,
                    char **log_msg, char **err_msg);

int ftp_remove_dir (ftp_server *fs, const char *path,
                    char **log_msg, char **err_msg);

/* make or get a directory */
char *mk_working_dir (ftp_server *fs, int makedir, const char *path,
                      char **log_msg, char **err_msg);


/************************ making a data connection ***********************/

/* the port and pasv commands are mainly for internal use */
int ftp_pasv (ftp_server *fs, char **log_msg, char **err_msg);
int ftp_port (ftp_server *fs, char *hostadr, char **log_msg, char **err_msg);

int ftp_make_data_connection (ftp_server *fs, const char *command,
                              int *return_code, char **return_line,
                              char **log_msg, char **err_msg);
int ftp_close_data_connection (ftp_server *fs, char **log_msg, char **err_msg);

void ftp_toggle_passive (ftp_server *fs, int passiveon);

int ftp_list (ftp_server *fs, const char *dir, int names_only, char ***lines,
              char **log_msg, char **err_msg);

int ftp_set_transfer_type (ftp_server *fs, int ttype,
			   char **log_msg, char **err_msg);

/**************************** working with files **************************/

int ftp_get_file (ftp_server *fs, 
                  const char *local_name, const char *remote_name,
                  char **log_msg, char **err_msg);
int ftp_put_file (ftp_server *fs, 
                  const char *local_name, const char *remote_name,
                  char **log_msg, char **err_msg);

int ftp_delete_file (ftp_server *fs, const char *remote_name,
                     char **log_msg, char **err_msg);

int ftp_rename_file (ftp_server *fs, 
                     const char *from_name, const char *to_name,
                     char **log_msg, char **err_msg);


#endif
