#include <malloc.h>
#include "lists.h"
#include "hasht.h"

/* legt eine neue hashtable an */
hashtable_t *new_hashtable (int (*cmp_func)(void*, void*),
    long (*hash_func)(void*), long hash_min, long hash_max)
{
  hashtable_t *res;
  long i, size=hash_max-hash_min+1;

  if (!hash_func || !cmp_func || (hash_max<hash_min)) return NULL;
  res=(hashtable_t*)malloc(sizeof(hashtable_t));
  res->hash_min  =hash_min;
  res->hash_max = hash_max;
  res->hash_func =hash_func;
  res->cmp_func  =cmp_func;
  res->val=(list_t**)malloc(sizeof(list_t*)*size);

  for (i=0; i<size; i++)
    res->val[i]=new_list();

  return res;
}


/* gibt den durch eine hashtable belegten Speicherplatz wieder frei. 
   Fuer jeden Wert wird die Funktion free_func aufgerufen (sofern !=NULL) */
void clear_hashtable (hashtable_t *h, void (*free_func)(void*))
{
  long i, size=h->hash_max-h->hash_min+1;
  for (i=0; i<size; i++)
    clear_list (h->val[i], free_func);
  free (h->val);
  free (h);
  return;
}


/* fuegt val in die hashtable ein. Gibt -1 bei einem Fehler zurueck,
   ansonsten 0 */
int insert_hash_element (hashtable_t *h, void *val)
{
  long pos, hash=h->hash_func(val);
  pos = hash-h->hash_min;
  if ((hash<h->hash_min)||(hash>h->hash_max)) return -1;
  insert_sorted_element (h->val[pos], val, h->cmp_func);
  return 0;
}


/* sucht, ob in der hashtable ein Wert ist, so dass die cmp_func sagt,
   dass er gleich dem uebergebenen val ist. Falls ja, wird ein Zeiger
   darauf zurueckgegeben. Falls nein, wird NULL zurueckgegeben. */
void *find_hash_element (hashtable_t *h, void *val)
{
  list_t *ltmp;
  long pos, hash=h->hash_func(val);
  pos = hash-h->hash_min;
  if ((hash<h->hash_min)||(hash>h->hash_max)) return NULL;
  ltmp=find_sorted_value (h->val[pos], val, h->cmp_func);
  if (ltmp) return ltmp->val;
  else return NULL;
}


/* sucht den uebergebenen Zeiger (nicht dessen Wert) in der hashtable
   und entfernt ihn. Ruft free_func auf, falls !=NULL.
   Gibt im Erfolgsfall 0, ansonsten -1 zurueck. */
int remove_hash_entry (hashtable_t *h, void *val, void (*free_func)(void*))
{
  list_t *head, *p;
  long pos, hash=h->hash_func(val);
  pos = hash-h->hash_min;
  if ((hash<h->hash_min)||(hash>h->hash_max)) return -1;
  p=head=h->val[pos];
  while ((p=p->next))
    if (p->val==val)
      {
        if (erase_list_element (head, p, free_func)) return -1;
	return 0;
      }
  return -1;
}


/* sucht den angegebenen Wert in der Hashtable und entfernt den entsprechenden
   Eintrag. Gibt im Erfolgsfall 0 zurueck, und -1, falls der Wert nicht
   gefunden wurde. Ruft vor dem Entfernen free_func auf, sofern dies !=NULL
   ist. */
int remove_hash_value (hashtable_t *h, void *val, void (*free_func)(void*))
{
  void *tmp=find_hash_element (h,val);
  long hash=h->hash_func(val);

  if (!tmp) return -1;
  erase_list_element (h->val[hash],tmp,free_func);
  return 0;
}


/* ordnet alle Values der uebergebenen Liste in die hashtable ein */
void insert_list_into_hashtable (hashtable_t *h, list_t *l, 
   void* (*copy_func)(void*))
{
  list_t *p=l;
  if (!l) return;
  while ((p=p->next))
    insert_hash_element (h, copy_func ? copy_func(p->val) : p->val);
  return;
}



/* schreibt alle Values in die uebergebene Liste ein. Ist sort!=0, so werden
   sie sortiert eingeordnet. Ansonsten werden wie einfach nur
   hintenangefuegt */
void insert_hashtable_into_list (list_t *l, hashtable_t *h, 
    void* (*copy_func)(void*), int sort)
{
  long i, size=h->hash_max-h->hash_min;
  list_t *p;
  void * nen;

  for (i=0; i<=size; i++)
    {
      p=h->val[i];
      while ((p=p->next))
	{
	  if (copy_func) nen=copy_func(p->val);
	  else nen=p->val;
	  if (sort) insert_sorted_element(l,nen,h->cmp_func);
          else insert_list_element(l,l->prev,nen);
	}
    }
  return;
}


/* fuegt alle Elemente von src in dst ein */
void insert_hashtable_into_hashtable (hashtable_t *dst, hashtable_t *src,
   void* (*copy_func)(void*))
{
  long i, srcsize=src->hash_max-src->hash_min;
  list_t *p;

  for (i=0; i<=srcsize; i++)
    {
      p=src->val[i];
      while ((p=p->next))
	insert_hash_element (dst,copy_func ? copy_func(p->val) : p->val);
    }
  return;
}


/* gibt die totale Anzahl an Eintraegen in der hashtable zurueck */
long hashtable_size (hashtable_t *h)
{
  long nr=0, i, size=h->hash_max-h->hash_min;
  list_t *p;

  for (i=0; i<=size; i++)
    {
      p=h->val[i];
      while ((p=p->next)) nr++;
    }
  return nr;
}
