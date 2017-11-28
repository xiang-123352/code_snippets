#include <malloc.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define __rconfig_const_chars_
#include "rconfig.h"
#undef  __rconfig_const_chars_


/* eine Hilfsfunktion, die die drei chars (s2 und s3) duerfen NULL sein,
   zu einem char zusammensetzt und in einem neu allokierten Speicher
   zurueckgibt. */
char *rconfig_make_message (const char *s1, const char *s2, const char *s3)
  {
    char *tmp=(char*)malloc(sizeof(char)*
      (2+strlen(s1)+(s2 ? strlen(s2) : 0)+(s3 ? strlen(s3) :0)));
     strcpy (tmp,s1);
    if (s2) strcat (tmp,s2);
    if (s3) strcat (tmp,s3);
    return tmp;
  }




/* Diese Funktion liest einfach aufgebaute Konfigurationsdateien der Form

  OPTION_NAME = irgendein Text oder andere Zeichen

Die Funktionsweise ist ganz einfach:
 1. Alles, was hinter einem # kommt, wird ignoriert.
 2. In jeder Zeile wird ein = gesucht. Kommt kein = vor, wird die Zeile
    ignoriert
 3. Die Zeile wird in alles vor dem = und alles nach dem = aufgeteilt.
    Fuehrende und endende blanks und tabs dieser beiden Teilstrings werden
    entfernt.
 4. Es wird geschaut, ob eine Option mit dem angegebenen Namen vorhanden
    ist. Wenn ja, wird ihr Wert auf den zweiten string gesetzt. Wenn nein
    wird ein Fehlerstring generiert und weitergemacht.*/

/* Zeilen koennen nicht mit \ fortgesetzt werden.
   Zeilen duerfen nicht laenger als 1024 Zeichen sein. */


/* Uebergeben werden zwei nullterminierte arrays von char* im ersten stehen
   die Optionsnamen, in den zweiten werden die Werte der Optionen 
   geschrieben. Ist ein Wert schon gesetzt wird und wird in der Datei
   neu definiert, so wird der alte Speicherplatz freigegeben. */



char *read_config_file (const char *fname, char **opt_name, char **opt_val)
{
  FILE *f;
  char line[1024], *c, *msg=NULL;
  int i;

  void trim_blanks (char *s)
    {
      char *t=s, *u=s;
      while ((*t)&&((*t==' ')||(*t=='\t'))) t++;
      while (*t) *(u++)=*(t++);
      while ((u--!=s)&&((*u==' ')||(*u=='\t')||(*u=='\n')));
      *(++u)='\0';
      return;
    }

  if (!(f=fopen(fname,"r")))
    return rconfig_make_message (file_error_msg,fname,".");
  while (fgets(line, 1024, f))
    {
      if ((c=strchr(line,'#'))) *c='\0';
      if ((c=strchr(line,'=')))
	{
	  *(c++)='\0';
	  trim_blanks (line);
	  trim_blanks (c);
	  i=0;
	  while ((opt_name[i])&&(strcmp(opt_name[i],line))) i++;
	  if (opt_name[i]) opt_val[i]=strdup(c);
          else
	    {
	      if (!msg) msg=rconfig_make_message (unknown_option_msg,line,".");
	    }
	}
    }
  fclose(f);
  return msg;
}


/* schreibt die optionen in opt_name und opt_val in die Datei fname, die 
   von read_config_file gelesen werden kann. An den Anfang der Datei wird 
   der starttext geschrieben. Der Benutzer muss selber dafuer sorgen, dass 
   der Starttext mit # auskommentiert wird. (Oder auch nicht. Man kann den 
   starttext auch dazu verwenden, zusaetzliche Optionen hineinzuschreiben.*/

char *write_config_file (const char *fname, char **opt_name, char **opt_val,
			 const char *starttext)
{
  FILE *f;
  int i=-1;

  if (!(f=fopen(fname,"w"))) 
    return rconfig_make_message (file_error_msg,fname,".");
  if (starttext) fprintf (f,"%s\n",starttext);
  while (opt_name[++i])
    if (opt_val[i]) fprintf (f,"%s = %s\n",opt_name[i],opt_val[i]);
  fclose (f);
  return NULL;
}





/* Diese Funktion dient dazu, den Namen einer Konfigurationsdatei 
   zu bilden. 
   1. Ist name==NULL, so wird der default-name genommen.
   2. ~ am Anfang wird zum home-directory des Benutzers expandiert
   3. Ist es kein absoluter Pfad (beginnend mit /), so wird 
      default_path davorkopiert. default_path darf mit / aufhoeren oder
      nicht. 

  Beispiel: make_conf_filename (".config",".default","~") ergibt
    "/home/username/.config" */

char *make_conf_filename (const char *name, const char *default_name, 
                          const char *default_path)
{
  char *res1, *res2;

  char *expand_tilde (const char *c)
    {
      char *tmp, *res;
      if (!c) return NULL;
      if (*c!='~') return strdup(c);
      tmp=getenv("HOME");
      res=(char*)malloc(sizeof(char)*(strlen(tmp)+strlen(c)));
      strcpy (res,tmp);
      strcat (res,c+1);
      free (tmp);
      return res;
    }

  if (name) res1=strdup(name);
  else res1=strdup(default_name);

  res2=expand_tilde (res1);
  free (res1);

  if ((*res2=='/')||(!default_path)) res1=strdup(res2);
  else
    {
      char *dpath=expand_tilde(default_path);
      int dp_len=strlen(dpath);
      if ((dp_len)&&(dpath[dp_len-1]=='/')) dpath[dp_len-1]='\0';
      res1=(char*)malloc(sizeof(char)*(strlen(res2)+strlen(dpath)+2));
      strcpy (res1, dpath);
      strcat (res1, "/");
      strcat (res1, res2);
      free (dpath);
    }
  free(res2);
  return res1;
}
