#ifndef DIR_H_INCLUDED
#define DIR_H_INCLUDED

#include <ftw.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <dirent.h>

    char *input_permissions;

    void list_dir(const char *path, const char* real_path);

    void print_file_info(const struct stat *stat, const char *file);

    void list_dir_using_nftw(const char *path);

    int print_path(const char *path, const struct stat *sb, int flag);

    void throw_error(const char message[]);

    int  main(int argc, char *argv[]);

#endif // DIR_H_INCLUDED
