// Compare - Recursive binary file comparison.
// Copyright (C) 2011, Ted Felix
// License: GPLv3+
// Started: 6/12/2011

#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <glob.h>

// Largest size for a path name string
#define PATH_LENGTH 4096

// globals
unsigned int destdoesnotexist = 0;
unsigned int different = 0;
unsigned int same = 0;
unsigned int unexpected = 0;
int srclen_original = 0;

// ---------------------------------------------------------------------
// Open a memory mapped file for read.
void *openmm(const char *filename)
{
	int fd = 0;
	struct stat st;
	void *pdata = 0;
	
	fd = open(filename, O_RDONLY);
	if (fd == -1) {
		perror("open");
		return 0;
	}

	if (fstat(fd, &st) == -1) {
		perror("fstat");
		return 0;
	}

	if (!S_ISREG(st.st_mode)) {
		printf("%s is not a file\n", filename);
		return 0;
	}

	pdata = mmap(0, st.st_size, PROT_READ, MAP_SHARED, fd, 0);
	if (pdata == MAP_FAILED) {
		perror("mmap");
		return 0;
	}

	if (close(fd) == -1) {
		perror("close");
	}

	return pdata;
}

// ---------------------------------------------------------------------
// Close a memory mapped file.
void closemm(void *pdata, size_t size)
{
	if (pdata != NULL)
	{
		if (munmap(pdata, size) == -1) {
			perror("munmap");
			return;
		}
	}
}

// ---------------------------------------------------------------------
// Compare two files using memory mapped I/O for speed.  name2 is the name
// that will be used in messages.  Generally it has the original source 
// directory removed so that it is reduced to just what is needed for the 
// user to identify the file.
void compare_files(const char *src, const char *dest, const char *name2)
{
	struct stat src_st;
	struct stat dest_st;
	void *psrc = 0;
	void *pdest = 0;
	int rc = 0;
	
//	printf("compare_files(%s, %s)\n", src, dest);

	// ??? Performance: We've already done this in compare_dirs().  Passing 
	//   these in would save time.
	stat(src, &src_st);
	stat(dest, &dest_st);

	// if they are of different lengths
	if (src_st.st_size != dest_st.st_size)
	{
		++different;
		printf("Different lengths: %s\n", name2 + 1);
		return;
	}
	
	// if src is zero length
	if (src_st.st_size == 0)
	{
		++same;
		return;
	}

	// Open both files for memory mapped i/o
	psrc = openmm(src);
	pdest = openmm(dest);

	rc = memcmp(psrc, pdest, src_st.st_size);

	if (rc == 0)
	{
		++same;
	}
	else
	{
		++different;
		printf("Files are different: %s\n", name2 + 1);
	}

	closemm(psrc, src_st.st_size);
	closemm(pdest, dest_st.st_size);
}

// ---------------------------------------------------------------------
// Compares two directories by going through every file and directory it
// contains and comparing them.
void compare_dirs(const char *src, const char *dest)
{
	char *srcname = 0;
	char *destname = 0;
	char *name2 = 0;
	glob_t globbuf;
	unsigned int i;
	size_t srclen = 0;
	struct stat src_st;
	struct stat dest_st;

//	printf("compare_dirs(%s, %s)\n", src, dest);

	// Tack on a "/*" to the end of the directory name
	srcname = malloc(PATH_LENGTH+1);
	strncpy(srcname, src, PATH_LENGTH);
	strncat(srcname, "/*", PATH_LENGTH);
	
	// Get the list of files in this directory.
	glob(srcname, 0, NULL, &globbuf);

	destname = malloc(PATH_LENGTH+1);

	// Length of the source directory so we can skip it and add the rest
	// to the destination directory and get the dest filename.
	srclen = strlen(src);
	
	// for each entry
	for (i = 0; i < globbuf.gl_pathc; ++i)
	{
//		printf("%s\n", globbuf.gl_pathv[i]);

		// Create the filename for the dest file by concatenating the dest dir
		// and the rest of the source name after the source directory.
		strncpy(destname, dest, PATH_LENGTH);
		strncat(destname, &(globbuf.gl_pathv[i][srclen]), PATH_LENGTH);

//		printf("    %s\n", destname);

		if (stat(destname, &dest_st) < 0)
		{
			++destdoesnotexist;
			printf("Destination does not exist: %s\n", destname);
			continue;
		}	

		stat(globbuf.gl_pathv[i], &src_st);
		
		// if both are directories
		if (S_ISDIR(src_st.st_mode)  &&  S_ISDIR(dest_st.st_mode))
		{
			compare_dirs(globbuf.gl_pathv[i], destname);
			continue;
		}
		
		// Strip off the original source dir so that messages are shorter.
		name2 = &(globbuf.gl_pathv[i][srclen_original]);
		
		// if both are files
		if (S_ISREG(src_st.st_mode)  &&  S_ISREG(dest_st.st_mode))
		{
			compare_files(globbuf.gl_pathv[i], destname, name2);
			continue;
		}

		// Something strange was being compared.
		// ??? Might want to at least make sure they are both the same mode.
		++unexpected;
		printf("Unexpected comparison: %s\n", name2 + 1);
	}
	
	// Free up the memory used by glob
	globfree(&globbuf);

	free(srcname);
	free(destname);
}

// ---------------------------------------------------------------------
// entry point
int main(int argc, char *argv[])
{
	struct stat st;

	// Allow only two args
	if (argc != 3)
	{
		printf("usage: compare dir1 dir2\n");
		return -1;
	}

	// Verify src is a valid directory
	if (stat(argv[1], &st) < 0)
	{
		printf("Source stat failed\n");
		return -1;
	}
	if (!S_ISDIR(st.st_mode))
	{
		printf("Source is not a directory.\n");
		return -1;
	}

	// Verify dest is a valid directory
	if (stat(argv[2], &st) < 0)
	{
		printf("Dest stat failed\n");
		return -1;
	}
	if (!S_ISDIR(st.st_mode))
	{
		printf("Dest is not a directory.\n");
		return -1;
	}
	
	// Save this so we can strip the original source dir off the front of
	// filenames and reduce the output in messages.
	srclen_original = strlen(argv[1]);
	
	// Send the two args to the compare routine
	compare_dirs(argv[1], argv[2]);

	printf("Destination is Identical: %u\n", same);
	printf("Destination is Different: %u\n", different);
	printf("Destination Does Not Exist: %u\n", destdoesnotexist);
	if (unexpected)
		printf("Unexpected file type (e.g. link or socket): %u\n", unexpected);
	
	return 0;
}
