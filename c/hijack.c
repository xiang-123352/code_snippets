/* hijack.c - force a process to load a library

    Usage: hijack PID LIBRARY
 
    PID is the pid of a running process.
    LIBRARY is the pathname of a dynamic library.
 
    hijack forces process PID to load the LIBRARY as if
    PID had called dlopen.  PID need only be a dynamic
    executable.  As usual, the LIBRARY's _init section
    is executed as it is loaded.
 
    hijack works on x86 Linux.
 
    Compile with no special options; e.g., "cc -o hijack hijack.c"
 
    Bugs:
 	PID exits if the LIBRARY does not exist.
 
    Copyright (C) 2002 Victor Zandy <zandy@cs.wisc.edu>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    Send mail regarding this file to zandy@cs.wisc.edu.  */
#define _XOPEN_SOURCE 500  /* include pread,pwrite */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <fcntl.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <dlfcn.h>
#include <elf.h>
#include <unistd.h>
#include <errno.h>

/* memory map for libraries */
#define MAX_NAME_LEN 256
#define MEMORY_ONLY  "[memory]"
struct mm {
	char name[MAX_NAME_LEN];
	unsigned long start, end;
};

typedef struct symtab *symtab_t;
struct symlist {
	Elf32_Sym *sym;       /* symbols */
	char *str;            /* symbol strings */
	unsigned num;         /* number of symbols */
};
struct symtab {
	struct symlist *st;    /* "static" symbols */
	struct symlist *dyn;   /* dynamic symbols */
};

static void * 
xmalloc(size_t size)
{
	void *p;
	p = malloc(size);
	if (!p) {
		fprintf(stderr, "Out of memory\n");
		exit(1);
	}
	return p;
}

static struct symlist *
get_syms(int fd, Elf32_Shdr *symh, Elf32_Shdr *strh)
{
	struct symlist *sl, *ret;
	int rv;

	ret = NULL;
	sl = (struct symlist *) xmalloc(sizeof(struct symlist));
	sl->str = NULL;
	sl->sym = NULL;

	/* sanity */
	if (symh->sh_size % sizeof(Elf32_Sym)) { 
		fprintf(stderr, "elf_error\n");
		goto out;
	}

	/* symbol table */
	sl->num = symh->sh_size / sizeof(Elf32_Sym);
	sl->sym = (Elf32_Sym *) xmalloc(symh->sh_size);
	rv = pread(fd, sl->sym, symh->sh_size, symh->sh_offset);
	if (0 > rv) {
		perror("read");
		goto out;
	}
	if (rv != symh->sh_size) {
		fprintf(stderr, "elf error\n");
		goto out;
	}

	/* string table */
	sl->str = (char *) xmalloc(strh->sh_size);
	rv = pread(fd, sl->str, strh->sh_size, strh->sh_offset);
	if (0 > rv) {
		perror("read");
		goto out;
	}
	if (rv != strh->sh_size) {
		fprintf(stderr, "elf error");
		goto out;
	}

	ret = sl;
out:
	return ret;
}

static int
do_load(int fd, symtab_t symtab)
{
	int rv;
	size_t size;
	Elf32_Ehdr ehdr;
	Elf32_Shdr *shdr = NULL, *p;
	Elf32_Shdr *dynsymh, *dynstrh;
	Elf32_Shdr *symh, *strh;
	char *shstrtab = NULL;
	int i;
	int ret = -1;
	
	/* elf header */
	rv = read(fd, &ehdr, sizeof(ehdr));
	if (0 > rv) {
		perror("read");
		goto out;
	}
	if (rv != sizeof(ehdr)) {
		fprintf(stderr, "elf error\n");
		goto out;
	}
	if (strncmp(ELFMAG, ehdr.e_ident, SELFMAG)) { /* sanity */
		fprintf(stderr, "not an elf\n");
		goto out;
	}
	if (sizeof(Elf32_Shdr) != ehdr.e_shentsize) { /* sanity */
		fprintf(stderr, "elf error\n");
		goto out;
	}

	/* section header table */
	size = ehdr.e_shentsize * ehdr.e_shnum;
	shdr = (Elf32_Shdr *) xmalloc(size);
	rv = pread(fd, shdr, size, ehdr.e_shoff);
	if (0 > rv) {
		perror("read");
		goto out;
	}
	if (rv != size) {
		fprintf(stderr, "elf error");
		goto out;
	}
	
	/* section header string table */
	size = shdr[ehdr.e_shstrndx].sh_size;
	shstrtab = (char *) xmalloc(size);
	rv = pread(fd, shstrtab, size, shdr[ehdr.e_shstrndx].sh_offset);
	if (0 > rv) {
		perror("read");
		goto out;
	}
	if (rv != size) {
		fprintf(stderr, "elf error\n");
		goto out;
	}

	/* symbol table headers */
	symh = dynsymh = NULL;
	strh = dynstrh = NULL;
	for (i = 0, p = shdr; i < ehdr.e_shnum; i++, p++)
		if (SHT_SYMTAB == p->sh_type) {
			if (symh) {
				fprintf(stderr, "too many symbol tables\n");
				goto out;
			}
			symh = p;
		} else if (SHT_DYNSYM == p->sh_type) {
			if (dynsymh) {
				fprintf(stderr, "too many symbol tables\n");
				goto out;
			}
			dynsymh = p;
		} else if (SHT_STRTAB == p->sh_type
			   && !strncmp(shstrtab+p->sh_name, ".strtab", 7)) {
			if (strh) {
				fprintf(stderr, "too many string tables\n");
				goto out;
			}
			strh = p;
		} else if (SHT_STRTAB == p->sh_type
			   && !strncmp(shstrtab+p->sh_name, ".dynstr", 7)) {
			if (dynstrh) {
				fprintf(stderr, "too many string tables\n");
				goto out;
			}
			dynstrh = p;
		}
	/* sanity checks */
	if ((!dynsymh && dynstrh) || (dynsymh && !dynstrh)) {
		fprintf(stderr, "bad dynamic symbol table");
		goto out;
	}
	if ((!symh && strh) || (symh && !strh)) {
		fprintf(stderr, "bad symbol table");
		goto out;
	}
	if (!dynsymh && !symh) {
		fprintf(stderr, "no symbol table");
		goto out;
	}

	/* symbol tables */
	if (dynsymh)
		symtab->dyn = get_syms(fd, dynsymh, dynstrh);
	if (symh)
		symtab->st = get_syms(fd, symh, strh);
	ret = 0;
out:
	free(shstrtab);
	free(shdr);
	return ret;
}

static symtab_t
load_symtab(char *filename)
{
	int fd;
	symtab_t symtab;

	symtab = (symtab_t) xmalloc(sizeof(*symtab));
	memset(symtab, 0, sizeof(*symtab));

	fd = open(filename, O_RDONLY);
	if (0 > fd) {
		perror("open");
		return NULL;
	}
	if (0 > do_load(fd, symtab)) {
		fprintf(stderr, "Error ELF parsing %s\n", filename);
		free(symtab);
		symtab = NULL;
	}
	close(fd);
	return symtab;
}


static int
load_memmap(pid_t pid, struct mm *mm, int *nmmp)
{
	char raw[10000];
	char name[MAX_NAME_LEN];
	char *p;
	unsigned long start, end;
	struct mm *m;
	int nmm = 0;
	int fd, rv;
	int i;

	sprintf(raw, "/proc/%d/maps", pid);
	fd = open(raw, O_RDONLY);
	if (0 > fd) {
		fprintf(stderr, "Can't open %s for reading\n", raw);
		return -1;
	}

	/* Zero to ensure data is null terminated */
	memset(raw, 0, sizeof(raw));

	p = raw;
	while (1) {
		rv = read(fd, p, sizeof(raw)-(p-raw));
		if (0 > rv) {
			perror("read");
			return -1;
		}
		if (0 == rv)
			break;
		p += rv;
		if (p-raw >= sizeof(raw)) {
			fprintf(stderr, "Too many memory mapping\n");
			return -1;
		}
	}
	close(fd);

	p = strtok(raw, "\n");
	m = mm;
	while (p) {
		/* parse current map line */
		rv = sscanf(p, "%08lx-%08lx %*s %*s %*s %*s %s\n",
			    &start, &end, name);
		p = strtok(NULL, "\n");

		if (rv == 2) {
			m = &mm[nmm++];
			m->start = start;
			m->end = end;
			strcpy(m->name, MEMORY_ONLY);
			continue;
		}

		/* search backward for other mapping with same name */
		for (i = nmm-1; i >= 0; i--) {
			m = &mm[i];
			if (!strcmp(m->name, name))
				break;
		}

		if (i >= 0) {
			if (start < m->start)
				m->start = start;
			if (end > m->end)
				m->end = end;
		} else {
			/* new entry */
			m = &mm[nmm++];
			m->start = start;
			m->end = end;
			strcpy(m->name, name);
		}
	}
	*nmmp = nmm;
	return 0;
}

/* Find libc in MM, storing no more than LEN-1 chars of
   its name in NAME and set START to its starting
   address.  If libc cannot be found return -1 and
   leave NAME and START untouched.  Otherwise return 0
   and null-terminated NAME. */
static int
find_libc(char *name, int len, unsigned long *start,
	  struct mm *mm, int nmm)
{
	int i;
	struct mm *m;
	char *p;
	for (i = 0, m = mm; i < nmm; i++, m++) {
		if (!strcmp(m->name, MEMORY_ONLY))
			continue;
		p = strrchr(m->name, '/');
		if (!p)
			continue;
		p++;
		if (strncmp("libc", p, 4))
			continue;
		p += 4;

		/* here comes our crude test -> 'libc.so' or 'libc-[0-9]' */
		if (!strncmp(".so", p, 3) || (p[0] == '-' && isdigit(p[1])))
			break;
	}
	if (i >= nmm)
		/* not found */
		return -1;

	*start = m->start;
	strncpy(name, m->name, len);
	if (strlen(m->name) >= len)
		name[len-1] = '\0';
	return 0;
}

static int
lookup2(struct symlist *sl, unsigned char type,
	char *name, unsigned long *val)
{
	Elf32_Sym *p;
	int len;
	int i;

	len = strlen(name);
	for (i = 0, p = sl->sym; i < sl->num; i++, p++)
		if (!strncmp(sl->str+p->st_name, name, len)
		    && ELF32_ST_TYPE(p->st_info) == type) {
			*val = p->st_value;
			return 0;
		}
	return -1;
}

static int
lookup_sym(symtab_t s, unsigned char type,
	   char *name, unsigned long *val)
{
	if (s->dyn && !lookup2(s->dyn, type, name, val))
		return 0;
	if (s->st && !lookup2(s->st, type, name, val))
		return 0;
	return -1;
}

static int
lookup_func_sym(symtab_t s, char *name, unsigned long *val)
{
	return lookup_sym(s, STT_FUNC, name, val);
}

static int
finddlopen(pid_t pid, unsigned long *dlopenaddr)
{
	struct mm mm[50];
	unsigned long libcaddr;
	int nmm;
	char libc[256];
	symtab_t s;

	if (0 > load_memmap(pid, mm, &nmm)) {
		fprintf(stderr, "cannot read memory map\n");
		return -1;
	}
	if (0 > find_libc(libc, sizeof(libc), &libcaddr, mm, nmm)) {
		fprintf(stderr, "cannot find libc\n");
		return -1;
	}
	s = load_symtab(libc);
	if (!s) {
		fprintf(stderr, "cannot read symbol table\n");
		return -1;
	}
	if (0 > lookup_func_sym(s, "_dl_open", dlopenaddr)) {
		fprintf(stderr, "cannot find _dl_open\n");
		return -1;
	}
	*dlopenaddr += libcaddr;
	return 0;
}

/* Write NLONG 4 byte words from BUF into PID starting
   at address POS.  Calling process must be attached to PID. */
static int
write_mem(pid_t pid, unsigned long *buf, int nlong, unsigned long pos)
{
	unsigned long *p;
	int i;

	for (p = buf, i = 0; i < nlong; p++, i++)
		if (0 > ptrace(PTRACE_POKEDATA, pid, pos+(i*4), *p))
			return -1;
	return 0;
}

/*
 Stack layout before we resume the process.
 The stack grows up. $OLDEIP is EIP when we attach.
 Args to _dl_open are passed in registers (EAX,EDX,ECX).

 $NEWESP, EIP  ->    pushad
                     mov $NEWESP, esp
                     call _dl_open
          ECX  ->    mov $OLDESP, esp
                     popad
                     ret
          EAX  ->    "libname.so"
      $OLDESP  ->    savedregs (32 bytes)
          ESP  ->    $OLDEIP
                     Top of user stack
*/
static char code[] = {
	0x60,                       /* pushad (0x60) */
	0xbc, 0x0, 0x0, 0x0, 0x0,   /* mov $0, %esp */
	0xe8, 0x0, 0x0, 0x0, 0x0,   /* call $0 */
	0xbc, 0x0, 0x0, 0x0, 0x0,   /* mov $0, %oldesp */
	0x61,                       /* popad */
	0xc3,                       /* ret */
	0x0, 0x0                    /* pad */
};

enum {
	OFF_NEWESP = 2,
	OFF_DLOPEN = 7,
	OFF_DLRET = 11,
	OFF_OLDESP = 12
};

int
main(int argc, char *argv[])
{
	pid_t pid;
	struct user_regs_struct regs;
	unsigned long dlopenaddr, codeaddr, libaddr;
	unsigned long *p;
	int fd, n;
	char buf[32];
	char *arg;

	if (argc != 3) {
		fprintf(stderr, "usage: %s PID LIBNAME\n", argv[0]);
		exit(1);
	}
	pid = strtol(argv[1], NULL, 0);
	n = strlen(argv[2])+1;
	n = n/4 + (n%4 ? 1 : 0);
	arg = xmalloc(n*sizeof(unsigned long));
	memcpy(arg, argv[2], n*4);

	if (0 > finddlopen(pid, &dlopenaddr)) {
		fprintf(stderr, "parse failed\n");
		exit(1);
	}

	/* Attach */
	if (0 > ptrace(PTRACE_ATTACH, pid, 0, 0)) {
		fprintf(stderr, "cannot attach to %d\n", pid);
		exit(1);
	}
	waitpid(pid, NULL, 0);
	sprintf(buf, "/proc/%d/mem", pid);
	fd = open(buf, O_WRONLY);
	if (0 > fd) {
		fprintf(stderr, "cannot open %s\n", buf);
		exit(1);
	}
	ptrace(PTRACE_GETREGS, pid, 0, &regs);

	/* push EIP */
	regs.esp -= 4;
	ptrace(PTRACE_POKEDATA, pid, regs.esp, regs.eip);

	/* push library name, leaving room for a pushad result */
	libaddr = regs.esp - n*4 - 32;
	if (0 > write_mem(pid, (unsigned long*)arg, n, libaddr)) {
		fprintf(stderr, "cannot write dlopen argument (%s)\n",
			strerror(errno));
		exit(1);
	}
		
	/* finish code and push it */
	codeaddr = libaddr - sizeof(code);
	p = (unsigned long*)&code[OFF_NEWESP];
	*p = codeaddr; /* stack begins after code */
	p = (unsigned long*)&code[OFF_DLOPEN];
	*p = dlopenaddr-(codeaddr+OFF_DLRET);
	p = (unsigned long*)&code[OFF_OLDESP];
	*p = regs.esp-32;
	if (0 > write_mem(pid, (unsigned long*)&code,
			  sizeof(code)/sizeof(long), codeaddr)) {
		fprintf(stderr, "cannot write code\n");
		exit(1);
	}
	regs.eip = codeaddr;

	/* Setup dlopen call; use internal register calling convention */
	regs.eax = libaddr;             /* library name */
	regs.edx = RTLD_NOW;            /* dlopen mode */
	regs.ecx = codeaddr+OFF_DLRET;  /* caller context used by dlopen */

	/* Detach and continue */
	ptrace(PTRACE_SETREGS, pid, 0, &regs);
	ptrace(PTRACE_DETACH, pid, 0, 0);

	return 0;
}
