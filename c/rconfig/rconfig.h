#ifndef __rconfig_h_
#define __rconfig_h_


#ifdef __rconfig_const_chars_
const char *file_error_msg="could not open file ";
const char *unknown_option_msg="unknown option ";
const char *illegal_format_msg="line without '='.\n";
#endif

char *read_config_file (const char *fname, char **opt_name, char **opt_val);
char *write_config_file (const char *fname, char **opt_name, char **opt_val,
			 const char *starttext);
char *make_conf_filename (const char *name, const char *default_name, 
                          const char *default_path);

#endif
