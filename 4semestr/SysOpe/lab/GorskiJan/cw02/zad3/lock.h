#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>

void show_options();

int get_option();

int get_byte_index(int file_size);

void lock_read(int file, int byte_index);

void lock_write(int file, int byte_index);

char read_byte(int file, int byte_index);

void write_byte(int file, int byte_index, char *byte);

void remove_lock(int file, int byte_index);

void print_locked_bytes(int file, int file_size);

void throw_error(const char *message);

int main(int argc, char *argv[]);
