#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <stdbool.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/times.h>
#include <time.h>


void sort_lib(const char *file_path, size_t record_size);

void sort_sys(const char *file_path, size_t record_size);

void throw_error(const char message[]);

int main(int argc, char *argv[]);
