#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <string.h>

/*
 * Function recurse_dir
 *
 * reads path and all its sub-directories recursively. For every found
 * file the pre_call_func and the post_call_func are called with the 
 * following parameters: The filename, the status of the file, and some
 * user data. The status of the file may be NULL, if it couldn't be read. 
 * The first two variables are static and must not be freed or changed.
 * - If path is NULL, the working directory is used.
 * - The pre_call_func is called, before the function goes down into the
 *   subdirectories, the post_call_func after it. (E.g. if one wants to
 *   remove files recursively, the post_call_func must be used.)
 * - For the directory path itself the two call_func are called too.
 * - Both call_func may be NULL.
 * - The pre_dat and post_data are user-data, which is passed to the
 *   pre_call_func res. post_call_func without change.
 *
 * Return values of the call_funcs:
 *   LIBFIND_USER_BREAK  : signals the recurse_dir-function to stop
 *                         immediately. Remaining post_call_funcs are not
 *                         called any more.
 *   LIBFIND_USER_RETURN : signals the recurse_dir-function to stop
 *                         immediately. But remaining post_call_functions 
 *                         are called.
 *   LIBFIND_USER_SKIP   : if it is a directory, recurse_dir doesn't go
 *                         go down into this directory. But both call_func
 *                         are called.
 *
 * Error codes: 
 *   LIBFIND_OPENDIR_ERR : at least one directory couldn't be read.
 *   LIBFIND_STAT_ERR    : attributes of at least one file couldn't be got.
 *   LIBFIND_USER_BREAK  : user stopped recursing.
 *   LIBFIND_USER_RETURN : user stopped recursing.
 * The return code may be a bitwise combination of these. Or zero.
 *
 * This function is under the BSD licence. It can be used for free for
 * free or for commercial programs. It may be changed arbitrily.
 *
 * Changelog:
 *  07/2002 created
 *  12/2002 totally rewritten to use post_ and pre_call_func and pass
 *          user data.
 *  08/203  bugfix: call_func_result wasn't initialized.
 */

#include "libfind.h"

int recurse_dir (const char *path, 
   int pre_call_func  (char *filename, struct stat *filestat, void  *pre_data),
   int post_call_func (char *filename, struct stat *filestat, void *post_data),
   void *pre_data, void *post_data)
{
  int recurse_dir_intern (char *pname)
    {
      DIR *d;
      struct dirent *de;
      struct stat sbuf;
      int call_func_result=0, recurse_dir_result=0, stat_err;
      char *pname_end=pname+strlen(pname);

      if ((stat_err = stat (pname, &sbuf)))
        recurse_dir_result |= LIBFIND_STAT_ERR;

      if (pre_call_func) 
        recurse_dir_result |= 
          (call_func_result = pre_call_func(pname, stat_err ? NULL : &sbuf,
                                            pre_data));

      if (!(call_func_result & LIBFIND_USER_BREAK)) {
        if (!(call_func_result & (LIBFIND_USER_RETURN | LIBFIND_USER_SKIP))) {
          /* if it is a directory we go down the subdirectories */
          if (!stat_err && (sbuf.st_mode & S_IFDIR)) {
            if (!(d=opendir(pname)))
              recurse_dir_result |= LIBFIND_OPENDIR_ERR;
            else {
              while ((de=readdir(d))) {
                if (strcmp(de->d_name, ".") && strcmp (de->d_name, "..")) {
                  sprintf (pname_end, "/%s", de->d_name);

                  recurse_dir_result |= recurse_dir_intern (pname);
                  *pname_end='\0';
                  if (recurse_dir_result & 
                      (LIBFIND_USER_BREAK | LIBFIND_USER_RETURN)) break;
                }
              } /* while */
              closedir (d);
            }
          } /* if (!stat_err... ) */
        } /* if not (USER_RETURN or USER_SKIP) */

        if (!(recurse_dir_result & LIBFIND_USER_BREAK) && (post_call_func))
          recurse_dir_result |= 
            (call_func_result = 
             post_call_func(pname, stat_err ? NULL : &sbuf, post_data));
      } /* if not USER_BREAK */

      /* USER_SKIP is no return value for this function */
      recurse_dir_result &= ~LIBFIND_USER_SKIP;
      return recurse_dir_result;
    } /* recurse_dir_intern */

  char pathname[1024];
  if (path) strcpy (pathname, path);
  else getcwd (pathname, 1024);

  return recurse_dir_intern (pathname);
}

