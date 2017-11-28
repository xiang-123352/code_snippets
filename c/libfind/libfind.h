#ifndef __libfind_h_
#define __libfind_h_

#include <sys/stat.h>

#define LIBFIND_OPENDIR_ERR  1
#define LIBFIND_STAT_ERR     2
#define LIBFIND_USER_BREAK   4
#define LIBFIND_USER_SKIP    8
#define LIBFIND_USER_RETURN 16

int recurse_dir (const char *path, 
   int pre_call_func  (char *filename, struct stat *filestat, void  *pre_data),
   int post_call_func (char *filename, struct stat *filestat, void *post_data),
   void *pre_data, void *post_data);

#endif
