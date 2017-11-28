/*

Copyright (C) 2000 Michael Becker

This library is under the BSD licence. It can be used for free for
free or for commercial programs. It may be changed arbitrily.

Furthermore the author confirms, that he has created this library to the best
of his knowledge and belief. But he takes no responsiblity or garantee for
whatever.

Michael Becker (http://www.ijon.de/comp/libs/index.html)
email momentarily: michael.w01@ijon.de
29.10.2000

changelog see below!

*/

#include <stdio.h>
#include <malloc.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <ctype.h>
#include <signal.h>
#include "ftpmlib.h"

int ftpmlib_global_timeout=FTPMLIB_TIMEOUT_DEFAULT;


/* this is an auxilliary function for concatenating strings: Append s2 to *s1.
   *s1 may be NULL, s2 not.  */
static void ftp_add_msg (char **s1, const char *s2)
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

/* that's just an alarm signal handler for interrupting system calls */
static void ftpmlib_timeout_sig_handler (int signo)
{
  return;
}

/* we need an own function for setting signal handlers to prevent 
   the automatic restart of system calls. 
   Directly taken from Stevens I. Doesn't work on Solaris. */
static void (*ftpmlib_signal_intr(int signum, void (*handler)(int)))(int)
{
  struct sigaction act, oact;
  act.sa_handler = handler;
  sigemptyset (&act.sa_mask);
  act.sa_flags = 0;
  if (sigaction(signum, &act, &oact)<0) return SIG_ERR;
  return (oact.sa_handler);
}



/* initializes a new ftp_server structure and sets its values to default. */
ftp_server *new_ftp_server ()
{
  ftp_server *res=(ftp_server*)malloc(sizeof(ftp_server));

  res->ccin = res->ccout = NULL;
  res->dcin = res->dcout = NULL;
  res->fdcin= res->fdcout=0;
  res->fddin= res->fddout=0;
  res->active_socket=0;
  res->scport= SERVER_DEFAULT_PORT;
  res->cdport = 0; res->sdport = 20;
  res->dadr = 0;
  res->mode  = MODE_ACTIVE;
  res->ttype = (TTYPE_1_ASCII | TTYPE_2_NONPRINT);
  res->tmode = TMODE_STREAM;

  res->timeout = ftpmlib_global_timeout;
  if (res->timeout==-1) res->timeout = FTPMLIB_TIMEOUT_DEFAULT;

  return res;
}


/* opens a TCP connection to the specified adress dst on the port, which
   is specified in fs as command-server-port.
   Sets the filedescriptors and the FILEs for reading and writing in fs.
   If an error occured while resolving the hostname, the h_errno is returned
   in *herrno. (herrno must not be NULL.) (This is necessary for thread
   safety.) 
   timeout may be 0 (no timeout), but not <0; */
int ftp_open_command_channel (const char *dst, ftp_server *fs, int *herrno,
                              int timeout)
{
  struct hostent *he;
  struct sockaddr_in a;

#ifdef _REENTRANT
  struct hostent he_buf;
  char buf[BUFSIZ];

  if (gethostbyname_r(dst, &he_buf, buf, BUFSIZ, &he, herrno)) return -1;
#else
  if (!(he=gethostbyname(dst))) {
    *herrno = h_errno;
    return -1;
  }
#endif

  if ((fs->fdcin=socket(AF_INET,SOCK_STREAM,0))==-1) return -2;

  a.sin_family=AF_INET;
  a.sin_port=htons(fs->scport);
  a.sin_addr=*((struct in_addr*)he->h_addr);
  bzero(&(a.sin_zero),8);

  ftpmlib_signal_intr(SIGALRM, ftpmlib_timeout_sig_handler);
  alarm (timeout);
  if (connect(fs->fdcin,(struct sockaddr*)&a, sizeof(struct sockaddr))==-1) {
    alarm(0);
    if (errno==EINTR) return -12;
    return -3;
  }
  alarm (0);

  fs->ccin =fdopen(fs->fdcin,"r");
  if ((fs->fdcout=dup(fs->fdcin))==-1) return -5;
  fs->ccout=fdopen(fs->fdcout,"w");
  if ((!fs->ccin)||(!fs->ccout)) return -4;

  return 0;
}


/* reads the response of the server on the command channel. Possibly prints
   it into the log_msg. An error processing has to be done afterwards by 
   the user himself.
   Returns the response-code of the server, and in return_line (if !=NULL),
   the first response line. */
int ftp_get_response (ftp_server *fs, char **return_line,
                      char **log_msg, char **err_msg)
{
  char line[LINE_LENGTH], line3;
  int rcode, newrcode=-1;

  alarm (fs->timeout);
  if (!fgets (line, LINE_LENGTH, fs->ccin)) {
    alarm (0);
    if (errno==EINTR) 
      ftp_add_msg (err_msg, "timeout while reading server response\n");
    else ftp_add_msg (err_msg, "server has closed connection\n");
    fclose (fs->ccout);
    fclose (fs->ccin);
    fs->ccout=fs->ccin=NULL;
    if (errno==EINTR) return -14;
    return -1;
  }
  alarm (0);

  ftp_add_msg (log_msg, line);
  if (return_line) *return_line=strdup (line);

  /* find return-code */
  line3=line[3];
  line[3]='\0';
  rcode = atoi (line);
  line[3]=line3;

  /* if necessary, read further lines */
  while (line3=='-') {
    alarm (fs->timeout);
    if (!fgets (line, LINE_LENGTH, fs->ccin)) {
      alarm (0);
      if (errno==EINTR)
        ftp_add_msg (err_msg, "timeout while reading server response\n");
      else ftp_add_msg (err_msg, "server has closed connection\n");
      fclose (fs->ccout);
      fclose (fs->ccin);
      if (errno==EINTR) return -14;
      return -1;
    }
    alarm (0);
    ftp_add_msg (log_msg, line);
    line3=line[3];
    line[3]='\0';
    newrcode=atoi(line);
    line[3]=line3;
  }

  return rcode;
}


/* sends a command to the server. Interprets the response line. If the
   response code is in the NULL-terminated array ok_returns, a log-message
   is written and 0 returned.
   In return_code the return code of thes server is returned. (If !=NULL)
   If the return code is in err_returns, an error message is generated, and
   -1 returned. 
   If the return code is neither in ok_returns nor in err_returns, an error
   message is generated and -1 returned too.
   command has to end with a \r\n
   If return_line!=NULL, the response line is copied into it. The memory for
   *return_line is newly allocated. */
int ftp_send_command (ftp_server *fs, const char *command,
		      int *ok_returns, int *err_returns,
                      int *return_code, char **return_line,
                      char **log_msg, char **err_msg)
{
  char *line=NULL;
  int rcode, i, codetype=0;

  if (!fs->ccout) {
    ftp_add_msg (err_msg, "command connection is closed\n");
    return -1;
  }
  ftp_add_msg (log_msg, command);
  fprintf (fs->ccout,"%s",command);
  fflush (fs->ccout);

  rcode=ftp_get_response (fs, &line, log_msg, err_msg);
  if (return_code) *return_code=rcode;
  if (return_line) *return_line=strdup(line);

  if (rcode==421) { /* service not available. server has closed connection */
    fclose (fs->ccout);
    fclose (fs->ccin);
    fs->ccout = fs->ccin = NULL;
  }

  /* response code ok ? */
  for (i=0; ok_returns[i]; i++) {
    if (ok_returns[i]==rcode) {
      codetype=1;
      break;
    }
  }

  /* response code signifies an error? */
  if (!codetype) {
    for (i=0; err_returns[i]; i++) {
      if (err_returns[i]==rcode) {
        ftp_add_msg (err_msg, line);
        codetype=2;
        break;
      }
    }
  }

  /* otherwise it was an illegal response. */
  if (!codetype) {
    if (rcode>=0) ftp_add_msg (err_msg, "illegal response from server\n");
    /* else some network error occurred and we already have the err_msg */
    codetype=2;
  }

  if (line) free(line);
  return ((codetype==1) ? 0 : -1);
}


/* makes a connection to ftp_server. In case of an error, NULL is returned.
   If the login fails, the connection is closed again and NULL is returned.
   If 0 is given as port, the SERVER_DEFAULT_PORT is used. */
ftp_server *ftpserver_connect (const char *servername, unsigned short int port,
                               char **log_msg, char **err_msg)
{
  ftp_server *fs=new_ftp_server();
  char line[LINE_LENGTH];
  int rcode, herrno, err;

  if (port) fs->scport=port;
  if ((err=ftp_open_command_channel(servername, fs, &herrno, fs->timeout))) {
    free (fs);
    if (err==-1) ftp_add_msg (err_msg, hstrerror(herrno));
    if (err==-12) ftp_add_msg (err_msg, "timeout during connect.");
    else ftp_add_msg (err_msg, strerror(errno));
    ftp_add_msg (err_msg, "\n");
    return NULL;
  }

  if (!fgets (line, LINE_LENGTH, fs->ccin)) {
    ftp_add_msg (err_msg, "unable to read greetings from server\n");
    fclose (fs->ccin);
    fclose (fs->ccout);
    free (fs);
    return NULL;
  }

  ftp_add_msg (log_msg, line);

  line[3]='\0';
  rcode=atoi(line);
  if (rcode!=220) { /* Yet no implementation for 120 */
    line[3]=' ';
    ftp_add_msg (err_msg, line);
    fclose (fs->ccin);
    fclose (fs->ccout);
    free (fs);
    return NULL;
  }
  return fs;
}


/* Closes the connection to ftp_server. In case of an error, the last response
   code of the server is returned. Otherwise 0. */
int ftpserver_close (ftp_server *fs, char **log_msg, char **err_msg)
{
  int quit_ok_codes[2] = {221, 0},
      quit_err_codes[2]= {500, 0},
      rcode;

  if (ftp_send_command (fs, "QUIT\r\n", quit_ok_codes, quit_err_codes,
                        &rcode, NULL, log_msg, err_msg))
    return rcode;
  fclose (fs->ccin);
  fclose (fs->ccout);
  free (fs);
  return 0;
}


/* Tries to login on fs with the given data. In case of a success 0 is
   returned. Otherwise the last response code of the server. */
int ftp_logon (ftp_server *fs, const char *username, const char *password,
	       const char *account, char **log_msg, char **err_msg)
{
  int rcode;
  char command[LINE_LENGTH];
  int user_ok_codes[4] = {230, 331, 332, 0},
      user_err_codes[5]= {421, 500, 501, 530, 0},
      pass_ok_codes[3] = {230, 332, 0},
      pass_err_codes[7]= {202, 421, 500, 501, 503, 530, 0},
      acct_ok_codes[2] = {230, 0},
      acct_err_codes[6]= {202, 421, 500, 503, 530, 0};

  /* send USER command */
  sprintf (command, "USER %s\r\n", username);
  if (ftp_send_command (fs, command, user_ok_codes, user_err_codes,
                        &rcode, NULL,  log_msg, err_msg))
    return rcode;

  if (rcode==230) /* ok, we are in already */ 
    return 0;

  if (rcode==331)  {
    sprintf (command, "PASS %s\r\n", password);
    if (ftp_send_command (fs, command, pass_ok_codes, pass_err_codes,
                          &rcode, NULL, log_msg, err_msg))
      return rcode;
    if (rcode==230) return 0;
    /* otherwise it has to be 332 */
  }

  /* send account */
  sprintf (command, "ACCT %s\r\n", account);
  if (ftp_send_command(fs, command, acct_ok_codes, acct_err_codes,
		       &rcode, NULL, log_msg, err_msg))
    return rcode;

  return 0;
}


/* changes the working directory: Is up!=0, it is changed into the parent
   directory. Otherwise into the directory path (absolute or relative path).*/
int ftp_change_dir (ftp_server *fs, int up, const char *path,
                   char **log_msg, char **err_msg)
{
  int rcode;
  char command[LINE_LENGTH];
  int cd_ok_codes[3] = {200, 250, 0},
    cd_err_codes[7]= {421, 500, 501, 502, 530, 550, 0};

  /* send command */
  if (up) sprintf (command, "CDUP\r\n");
  else sprintf (command, "CWD %s\r\n", path);
  if (ftp_send_command (fs, command, cd_ok_codes, cd_err_codes,
                        &rcode, NULL, log_msg, err_msg))
    return rcode;
  return 0;
}


/* tries to remove the directory dir. It has to be empty. */
int ftp_remove_dir (ftp_server *fs, const char *path,
                   char **log_msg, char **err_msg)
{
  int rcode;
  char command[LINE_LENGTH];
  int rmd_ok_codes[2] = {250, 0},
      rmd_err_codes[7]= {421, 500, 501, 502, 530, 550, 0};

  /* send command */
  sprintf (command, "RMD %s\r\n", path);
  if (ftp_send_command (fs, command, rmd_ok_codes, rmd_err_codes,
                        &rcode, NULL, log_msg, err_msg))
    return rcode;
  return 0;
}


/* tries to get the working directory or to make a new directory, depending
   of whether makedir==0 or !=0. In all cases a pointer to a newly allocated
   string with the absolute path is returned, or NULL in case of no success. */
char *mk_working_dir (ftp_server *fs,
                      int makedir, const char *path,
                      char **log_msg, char **err_msg)
{
  char *res=NULL, *line=NULL, *pos, command[LINE_LENGTH];
  int rcode,
    pwd_ok_codes[2] = {257, 0},
    pwd_err_codes[7]= {421, 500, 501, 502, 530, 550, 0};

    if (makedir) sprintf (command, "MKD %s\r\n", path);
    else sprintf (command, "PWD\r\n");
    if (ftp_send_command(fs, command, pwd_ok_codes, pwd_err_codes,
			 &rcode, &line, log_msg, err_msg)) {
      if (line) free(line);
      line=NULL;
      return NULL;
    }

    if ((pos=strchr(line+5, '"'))) {
      *pos='\0';
      res=strdup(line+5);
    }
    free (line);
    return res;
}


/* sends the PASV command and reads the port, to which the server wants to
   be connected. Sets the PASSIVE-flag.
   Sets the elements sdport and dadr in the ftp_server structure. */
int ftp_pasv (ftp_server *fs, char **log_msg, char **err_msg)
{
  char *line=NULL, *data_start, *data_end, *pos;
  int rcode, no_komma=0,
    pasv_ok_codes[2]  = {227, 0},
    pasv_err_codes[5] = {421, 500, 501, 502, 0};
    int h[6], i;

  if (ftp_send_command(fs,"PASV\r\n",pasv_ok_codes, pasv_err_codes,
                       &rcode, &line, log_msg, err_msg)) {
    if (line) free(line);
    line=NULL;
    return -1;
  }

  /* somewhere in the response there has to be string, which consists only
     of ciphers and exactly 5 commata. We have to search it. */
  data_end=line+4;
  while (no_komma<5) {
    data_start=data_end;
    while ((*data_start)&&(!isdigit(*data_start))) data_start++;
    if (!*data_start) break;
    data_end=data_start;
    no_komma=0;
    while ((isdigit(*data_end))||(*data_end==',')) {
      data_end++;
      if (*data_end==',') no_komma++;
    }
  }
  if ((!*data_start)||(no_komma>5)) {
    ftp_add_msg (err_msg, "can't interprete response from server\n");
    free (line);
    return -1;
  }
  *data_end=',';

  /* Now we have to read adress and port out of this string. 
     The string has the format h1,h2,h3,h4,p1,p2 */

  for (i=0; i<6; i++) {
    pos=strchr (data_start,',');
    *pos='\0';
    h[i]=atoi(data_start);
    data_start=pos+1;
  }

  fs->dadr=0;
  for (i=0; i<4; i++) fs->dadr=(fs->dadr*256)+h[i];
  fs->sdport=0;
  for (i=4; i<6; i++) fs->sdport=(fs->sdport*256)+h[i];

  /* finally change the adress to network byte order */
  fs->dadr=htonl(fs->dadr);

  fs->mode=MODE_PASSIVE;

  free (line);
  return 0;
}


/* toggles the MODE_ACTIVE or MODE-PASSIVE flag. */
void ftp_toggle_passive (ftp_server *fs, int passiveon)
{
  if (passiveon) fs->mode=MODE_PASSIVE;
  else fs->mode=MODE_ACTIVE;
  return;
}


/* sends a PORT command. Sets the port fs->cdport and the host-adress, which
   is given in the form "x.x.x.x". If the latter is NULL, the host adress
   used in the command channel is also used here.
   port has to be in hostbyte order.
   sets to active ftp.
   sets the element cdport in the ftp_server structure. */
int ftp_port (ftp_server *fs, char *hostadr, char **log_msg, char **err_msg)
{
  struct sockaddr_in s_name;
  socklen_t s_name_len=sizeof(s_name);
  char command[LINE_LENGTH], host_addr[20], *pos;
  int rcode,
    port_ok_codes[2] = {200, 0},
    port_err_codes[5]= {421, 500, 501, 530, 0};

    if (!hostadr) {
      /* first we have to find the adress of the host. The data channel will
         probably come on the same interface, on which the command channel 
         goes out */
      if (getsockname(fs->fdcin,(struct sockaddr *) &s_name, &s_name_len)) {
        ftp_add_msg (err_msg, strerror(errno));
        ftp_add_msg (err_msg, "\n");
	return -1;
      } /* No it is in s_name.sin_addr in network byte order */

      strcpy(host_addr, inet_ntoa(s_name.sin_addr));
      for (pos=host_addr; *pos; pos++)
	if (*pos=='.') *pos=',';
    }
    else strcpy(host_addr,hostadr);

  /* make the command and send it. */
  sprintf (command, "PORT %s,%i,%i\r\n", host_addr, 
           fs->cdport/256, fs->cdport%256);
  if (ftp_send_command(fs, command, port_ok_codes, port_err_codes,
                       &rcode, NULL, log_msg, err_msg))
    return rcode;

  fs->mode=MODE_ACTIVE;
  return 0;
}



/* processes the command command, which needs a data channel. Before it
   negotiates with the PORT or PASV command, which ports and adresses are
   used. The order for active and passive is as follows:
   active:  bind - PORT - listen - (command) - accept
   passive: PASV - (command) - connect */
int ftp_make_data_connection (ftp_server *fs, const char *command,
                              int *return_code, char **return_line,
                              char **log_msg, char **err_msg)
{
  struct sockaddr_in a, serv_a, s_name;
  socklen_t s_name_len=sizeof(s_name);
  int tmp_socket, a_size,
      ok_codes[3]  = {125, 150, 0},
      err_codes[16]= {421, 425, 426, 450, 451, 452, 500, 501, 502, 530, 
                      532, 550, 551, 552, 553, 0},
      rcode;

  if (fs->dcin && fs->dcout) { /* data channel seems to be already open */
    ftp_send_command(fs, command, ok_codes, err_codes, return_code,
                     return_line, log_msg, err_msg);
  if (*return_code>=500) return -9; /* command was faulty */
  if (*return_code==125) return 0; /* ok */
  if (*return_code==426) { /* server has cut off connection */
    fs->dcin=fs->dcout=NULL;
    return -9;
    }
  if ((*return_code==450)||(*return_code==451)) 
    return -9; /* some other error occured */
  if (*return_code!=425) return -9; /* illegal response from server */
  /* if the function come up to here, the data channel probably wasn't open
     after all */
  }

  /* data channel not yet open */
  if ((tmp_socket=socket(AF_INET,SOCK_STREAM,0))==-1) return -2;
  a.sin_family=AF_INET;
  a.sin_port=0;
  a.sin_addr.s_addr=INADDR_ANY;
  bzero(&(a.sin_zero),8);

  if (fs->mode==MODE_ACTIVE) { /* active FTP */
    fs->active_socket=tmp_socket;
    if (bind(fs->active_socket, (struct sockaddr*)&a, 
             sizeof(struct sockaddr))) {
      close(fs->active_socket);
      fs->active_socket=0;
      return -6;
    }

    /* now we have the socket and again have to find port and adress */
    if (getsockname(fs->active_socket, (struct sockaddr*) &s_name, 
                    &s_name_len)) {
      close(fs->active_socket);
      fs->active_socket=0;
      return -10;
    }

    fs->cdport=ntohs(s_name.sin_port);

    if (ftp_port(fs, NULL, log_msg, err_msg)) {
      close(fs->active_socket);
      fs->active_socket=0;
      return -9;
    }

    if (listen(fs->active_socket, 1)) {
      close(fs->active_socket);
      fs->active_socket=0;
      return -7;
    }

    /* send command */
    if (ftp_send_command (fs, command, ok_codes, err_codes, 
                          return_code, return_line, log_msg, err_msg)) {
      close(fs->active_socket);
      fs->active_socket=0;
      return -9;
    }

    a_size=sizeof(struct sockaddr_in);
    alarm (fs->timeout);
    if ((fs->fddin=accept(fs->active_socket, (struct sockaddr*) &serv_a, 
                          &a_size))<0) {
      alarm (0);
      close(fs->active_socket);
      fs->active_socket=0;
      if (errno==EINTR) {
        ftp_add_msg (err_msg, "timeout waiting for data channel\n");
        return -13;
      }
      return -8;
    }
    alarm (0);
  }
  else { /* passive FTP */
    /* send PASV command and set sdport and dadr */
    if (ftp_pasv (fs, log_msg, err_msg)) {
      close (tmp_socket);
      return -9;
    }

    fs->fddin=tmp_socket;

    /* enter server adress and port */
    serv_a.sin_family=AF_INET;
    serv_a.sin_port=htons(fs->sdport);
    serv_a.sin_addr.s_addr=fs->dadr; /* is already in networkbyte order */
    bzero (&(serv_a.sin_zero),8);

    /* send command. This is not possible with the ftp_send_command, because
       we can't expect a response from the server, until the other 
       connection is established. */
    ftp_add_msg (log_msg, command);
    fprintf (fs->ccout, "%s", command);
    fflush (fs->ccout);

    /* make data connection */
    alarm (fs->timeout);
    if (connect(fs->fddin,(struct sockaddr*)&serv_a,sizeof(struct sockaddr))) {
      alarm (0);
      close (fs->fddin);
      if (errno==EINTR) {
        ftp_add_msg (err_msg, "timeout during connect.\n");
        return -12;
      }
      return -3;
    }
    alarm (0);

    rcode=ftp_get_response(fs, NULL, log_msg, err_msg);
    if ((rcode!=125)&&(rcode!=150)) return -9;
    /* in this case an error message should be generated again, because 
       ftp_get_response doesn't do this itself. */
  }

  /* bind data connection to *FILEs and return. */
  fs->dcin =fdopen(fs->fddin,"r");
  if ((fs->fddout=dup(fs->fddin))==-1) return -5;
  fs->dcout=fdopen(fs->fddout,"w");
  if ((!fs->dcin)||(!fs->dcout)) return -4;

  return 0;
}


/* closes the data channel and waits for a confirmation of the server */
int ftp_close_data_connection (ftp_server *fs, char **log_msg, char **err_msg)
{
  int rcode;
  char *rline;

  fclose (fs->dcin);  fs->dcin =NULL;
  fclose (fs->dcout); fs->dcout=NULL;

  if (fs->active_socket) {
    close(fs->active_socket);
    fs->active_socket=0;
  }

  rcode=ftp_get_response (fs, &rline, log_msg, err_msg);
  if ((rcode!=226)&&(rcode!=250)) {
    ftp_add_msg (err_msg, rline);
    return -9;
  }
  return 0;
}


/* sends a LIST command to the server and returns a NULL terminated array of
   the lines. Attention: Not every line has to contain a file.
   If dir==NULL, the working dir is used.
   If names_only!=0, a list file file names without further information is
   returned.
   Attention: The function also returns successfully, if the directory doesn't
   exist. Then in the lines returned the error message of /bin/ls can be
   found. */
int ftp_list (ftp_server *fs, const char *dir, int names_only, char ***lines,
              char **log_msg, char **err_msg)
{
  int rcode, fcode, buflen=EXPECTED_LIST_LENGTH, line_no=0;
  char line[LINE_LENGTH], command[LINE_LENGTH];

  *lines=(char**)malloc(sizeof(char*)*(buflen+1));

  if (dir) sprintf (command,"LIST %s\r\n",dir);
  else sprintf (command,"LIST\r\n");
  if (names_only) { /* change LIST to NLST */
    command[0]='N';
    command[1]='L';
  }

  if ((fcode=ftp_make_data_connection(fs, command, &rcode, NULL, 
                                      log_msg, err_msg))) {
    if ((fcode<0)&&(fcode!=-9)) {
      ftp_add_msg (err_msg, strerror(errno));
      ftp_add_msg (err_msg, "\n");
    }
    return rcode;
  }

  /* data channel should be open. Now we can read. */
  alarm (fs->timeout);
  while (fgets(line, LINE_LENGTH-1, fs->dcin)) {
    alarm (0);
    if (line_no>=buflen) {
      buflen*=2;
      *lines=realloc(*lines, sizeof(char*)*(buflen+1));
    }
    (*lines)[line_no]=strdup(line);
    line_no++;
    if (errno==EINTR) break;
    alarm (fs->timeout);
  }
  alarm (0);
  (*lines)[line_no]=NULL;

  fcode = ftp_close_data_connection(fs, log_msg, err_msg);

  if (errno==EINTR) {
    ftp_add_msg (err_msg, "timeout reading data\n");
    return -14;
  }

  return fcode;
}


/* Sets the transfer type. Returns 0 in case of succes, -1, if a wrong
   value for type was passed. The value local is not implemented. */
int ftp_set_transfer_type (ftp_server *fs, int ttype,
			   char **log_msg, char **err_msg)
{
  int type_ok_codes[2] = {200, 0},
      type_err_codes[6]= {421, 500, 501, 504, 530, 0},
      rcode;
  char command[10]="TYPE x\r\n";

  switch (ttype) {
  case TTYPE_1_ASCII:
    command[5]='a';
    break;
  case TTYPE_1_IMAGE:
    command[5]='i';
    break;
  case TTYPE_1_EBCDIC:
    command[5]='e';
    break;
  default:
    return -1;
  }
  if (ftp_send_command (fs, command, type_ok_codes, type_err_codes,
                        &rcode, NULL, log_msg, err_msg))
    return rcode;

  return 0;
}


/* tries to GET the file remote_name from the server and save it under
   the name local_name */
int ftp_get_file (ftp_server *fs, 
                  const char *local_name, const char *remote_name,
                  char **log_msg, char **err_msg)
{
  int rcode, fcode, ch;
  char command[LINE_LENGTH];
  FILE *output;

  sprintf (command, "RETR %s\r\n", remote_name);

  /* open the local file for writing */
  if (!(output=fopen(local_name,"w"))) {
    ftp_add_msg (err_msg, "can't open file\n");
    return -11;
  }

  if ((fcode=ftp_make_data_connection(fs, command, &rcode, NULL, 
                                      log_msg, err_msg))) {
    fclose (output);
    if ((fcode<0)&&(fcode!=-9)) {
      ftp_add_msg (err_msg, strerror(errno));
      ftp_add_msg (err_msg, "\n");
    }
    return rcode;
  }

  /* data channel should now be open. We can read. */
  alarm (fs->timeout);
  while ((ch=fgetc(fs->dcin))!=EOF) {
    if (errno==EINTR) break;
    fputc (ch, output);
    alarm (fs->timeout); /* reset alarm */
  }
  alarm (0);
  fclose (output);

  fcode =  ftp_close_data_connection(fs, log_msg, err_msg);

  if (errno==EINTR) {
    ftp_add_msg (err_msg, "timeout reading data\n");
    return -14;
  }

  return fcode;
}


/* tries to upload the local file to the server */
int ftp_put_file (ftp_server *fs, 
                  const char *local_name, const char *remote_name,
                  char **log_msg, char **err_msg)
{
  int rcode, fcode, ch;
  char command[LINE_LENGTH];
  FILE *input;

  sprintf (command, "STOR %s\r\n", remote_name);

  /* open the local file for reading */
  if (!(input=fopen(local_name,"r"))) {
    ftp_add_msg (err_msg, "can't open file\n");
    return -11;
  }

  if ((fcode=ftp_make_data_connection(fs, command, &rcode, NULL, 
                                      log_msg, err_msg))) {
    fclose (input);
    if ((fcode<0)&&(fcode!=-9)) {
      ftp_add_msg (err_msg, strerror(errno));
      ftp_add_msg (err_msg, "\n");
    }
    return rcode;
  }

  /* now data channel should be open. We can write */
  alarm (fs->timeout);
  while ((ch=fgetc(input))!=EOF) {
    fputc (ch, fs->dcout);
    if (errno==EINTR) break;
    alarm (fs->timeout); /* reset alarm */
  }
  alarm (0);
  fclose (input);

  fcode =  ftp_close_data_connection(fs, log_msg, err_msg);

  if (errno==EINTR) {
    ftp_add_msg (err_msg, "timeout sending data\n");
    return -15;
  }

  return fcode;
}


/* remove a file */
int ftp_delete_file (ftp_server *fs, const char *remote_name,
                     char **log_msg, char **err_msg)
{
  int rcode,
    dele_ok_codes[2]  = {250, 0},
    dele_err_codes[8] = {421, 450, 500, 501, 502, 530, 550, 0};
  char command[LINE_LENGTH];

  /* send command */
  sprintf (command, "DELE %s\r\n", remote_name);
  if (ftp_send_command (fs, command, dele_ok_codes, dele_err_codes,
                        &rcode, NULL, log_msg, err_msg))
    return rcode;
  return 0;
}


/* renames a file from from_name to to_name. */
int ftp_rename_file (ftp_server *fs, 
                     const char *from_name, const char *to_name,
                     char **log_msg, char **err_msg)
{
  int rcode,
      rnfr_ok_codes[2] = {350, 0},
      rnfr_err_codes[8]= {421, 450, 500, 501, 502, 530, 550, 0},
      rnto_ok_codes[2] = {250, 0},
      rnto_err_codes[8]= {421, 500, 501, 502, 530, 532, 553, 0};
  char command[LINE_LENGTH];

  sprintf (command, "RNFR %s\r\n", from_name);
  if (ftp_send_command (fs, command, rnfr_ok_codes, rnfr_err_codes,
                        &rcode, NULL, log_msg, err_msg))
    return rcode;

  sprintf (command, "RNTO %s\r\n", to_name);
  if (ftp_send_command (fs, command, rnto_ok_codes, rnto_err_codes,
                        &rcode, NULL, log_msg, err_msg))
    return rcode;

  return 0;
}

/***************************************************************************
  There is still no implementation of the following response codes:
    120 (after connection establishment): service available in nn minutes.


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
-12    : timeout during connect
-13    : timeout during accept
-14    : timeout during reading
-15    : timeout sending data




CHANGELOG

until 29.10.2000
  first working version. Started writing documentation

31.10.2000
  system errors too are given to the error_func.

13.12.2002
  changed comments and documentation to english, documentation from html
  to ascii format. error-messages are now returned in a string (err_msg).

29.12.2002
  added reentrant version of gethostbyname.
  added timeouts.
  version 1.2

4.7.2004
  active ftp left data data sockets open. bug found and fixed by
  Daniel Haensse <haensse@swissembedded.com>

  server responses with more than two lines weren't read in ftp_get_response.
  version 1.3

*/

