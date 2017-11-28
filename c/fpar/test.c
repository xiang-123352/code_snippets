#include <stdio.h>

#include "fpar.h"

int main ()
{
  char s[100];
  node_t *n;

  get_tokens();

  printf ("input numerical expression (e.g. 3+4^sin5). (x==Pi)\n");
  gets (s);
  printf ("\n\n");

  n=fpar_parserw (s);
  if (!n) {
    printf ("Error while parsing input. \n");
    exit (-1);
  }
  fprintf (stderr, "-----------\n");
  tree_output(n, 0);
  fprintf (stderr, "-----------\n");
  calc_value (n);
  printf ("Result: %f\n", n->value);
  free_node_tree (n);

  return 0;
}
