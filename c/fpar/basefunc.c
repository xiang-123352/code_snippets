#include <math.h>
#include "basefunc.h"

void base_add (node_t *n)
{
  n->value = n->childs[0]->value + n->childs[1]->value;
  n->valid = 1;
  return;
}

void base_sub (node_t *n)
{
  n->value = n->childs[0]->value - n->childs[1]->value;
  n->valid = 1;
  return;
}

void base_mult (node_t *n)
{
  n->value = n->childs[0]->value * n->childs[1]->value;
  n->valid = 1;
  return;
}

void base_div (node_t *n)
{
  n->value = n->childs[0]->value / n->childs[1]->value;
  n->valid = 1;
  return;
}

void base_sqrt (node_t *n)
{
  n->value = sqrt(n->childs[0]->value);
  n->valid=1;
  return;
}

void base_sin (node_t *n)
{
  n->value = sin(n->childs[0]->value);
  n->valid = 1;
  return;
}

void base_cos (node_t *n)
{
  n->value = cos(n->childs[0]->value);
  n->valid = 1;
  return;
}

void base_tan (node_t *n)
{
  n->value = tan(n->childs[0]->value);
  n->valid = 1;
  return;
}

void base_exp (node_t *n)
{
  n->value = exp(n->childs[0]->value);
  n->valid = 1;
  return;
}

void base_ln (node_t *n)
{
  n->value = log(n->childs[0]->value);
  n->valid = 1;
  return;
}

void base_pow (node_t *n)
{
  n->value = pow(n->childs[0]->value,n->childs[1]->value);
  n->valid = 1;
  return;
}

void base_neg (node_t *n)
{
  n->value = -n->childs[0]->value;
  n->valid = 1;
  return;
}

void base_id (node_t *n)
{
  n->value = n->childs[0]->value;
  n->valid = 1;
  return;
}

void base_x (node_t *n)
{
  n->value = 3.1415; 
  /* here can stand something arbitrary, e.g. an own function, the value of
     a variable or something like this. */
  n->valid = 1;
  return;
}

