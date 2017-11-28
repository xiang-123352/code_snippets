#ifndef __hasht_h_
#define __hasht_h_

#include "lists.h"

typedef struct {
  list_t **val;
  int (*cmp_func)(void*, void*);
  long (*hash_func)(void*);
  long hash_min, hash_max; /* minimaler und maximaler hash-Wert */
} hashtable_t;

hashtable_t *new_hashtable (int (*cmp_func)(void*, void*),
    long (*hash_func)(void*), long hash_min, long hash_max);
void clear_hashtable (hashtable_t *h, void (*free_func)(void*));
int  insert_hash_element (hashtable_t *h, void *val);
void *find_hash_element (hashtable_t *h, void *val);
int remove_hash_entry (hashtable_t *h, void *val, void (*free_func)(void*));
int remove_hash_value (hashtable_t *h, void *val, void (*free_func)(void*));
void insert_list_into_hashtable (hashtable_t *h, list_t *l,
     void* (*copy_func)(void*));
void insert_hashtable_into_list (list_t *l, hashtable_t *h,
     void* (*copy_func)(void*), int sort);
void insert_hashtable_into_hashtable (hashtable_t *dst, hashtable_t *src,
     void* (*copy_func)(void*));
long hashtable_size (hashtable_t *h);

#endif
