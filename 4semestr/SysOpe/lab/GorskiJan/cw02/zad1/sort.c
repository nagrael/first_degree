#include "sort.h"


int main(int argc, char *argv[])
{
    if (argc < 4) {
        puts("usage: ./sort file_path record_size {lib|sys}");
        return EXIT_FAILURE;
    }

    char *file_path = argv[1];
    size_t record_size = (size_t) atoi(argv[2]);
    char *func_type = argv[3];

    struct tms start, end;

    times(&start);

    if (strcmp(func_type, "lib") == 0) {
        puts("Sort using library functions");
        sort_lib(file_path, record_size);
    } else if (strcmp(func_type, "sys") == 0) {
        puts("Sort using system functions");
        sort_sys(file_path, record_size);
    } else {
        throw_error("Invalid 3rd parameter of input");
    }

    times(&end);

    printf("User Time:\t%fs\n" " System Tiem:\t%fs\n",(double)(end.tms_utime-start.tms_utime)/CLOCKS_PER_SEC, (double)(end.tms_stime-start.tms_stime)/CLOCKS_PER_SEC);

    return EXIT_SUCCESS;
}

void sort_lib(const char *file_path, size_t record_size)
{
    FILE *file;
    if (!(file = fopen(file_path, "r+"))) {
        throw_error("cannot open file");
    }

    struct stat my_stat;
    int records_number;
    unsigned char *chars, *key;

    stat(file_path, &my_stat);
    records_number = (int) (my_stat.st_size / record_size);

    chars = malloc(record_size);
    key = malloc(record_size);
    if (!chars || !key) {
        throw_error("malloc failed");
    }

    for (int i = 1; i< records_number; ++i) {

        if (fseek(file, i*record_size, SEEK_SET)) {
                    throw_error("fseek failed");
            }
        fread(key, sizeof(char), record_size, file);

        if (fseek(file, -record_size, SEEK_CUR)) {
            throw_error("fseek failed");
        }
        for (int j = i-1; j >=0; --j) {
            if (fseek(file, -record_size, SEEK_CUR)) {
                throw_error("fseek failed");
            }

            fread(chars, sizeof(char), record_size, file);

            if (fseek(file, -record_size, SEEK_CUR)) {
                throw_error("fseek failed");
            }
            if (chars[0] > key[0]) {
                fwrite(key, sizeof(char), record_size, file);
                fwrite(chars, sizeof(char), record_size, file);
                    if (fseek(file, -2*record_size, SEEK_CUR)) {
                    throw_error("fseek failed");
                    }
            }
            else{
                break;
            }



        }

    }

    free(chars);
    free(key);
    fclose(file);
}

void sort_sys(const char *file_path, size_t record_size)
{
    int file = open(file_path, O_RDWR);
    if (file < 0) {
        throw_error("cannot open file");
    }

    struct stat my_stat;
    int records_number;
    unsigned char *chars, *key;

    stat(file_path, &my_stat);
    records_number = (int) (my_stat.st_size / record_size);

    chars = malloc(record_size);
    key = malloc(record_size);
    if (!chars || !key) {
        throw_error("malloc failed");
    }


    for (int i = 1; i< records_number; ++i) {
        if (lseek(file, i* record_size, SEEK_SET) == -1) {
            throw_error("lseek failed");
        }
        if (read(file, key, record_size) == -1) {
            throw_error("read failed");
        }
        if (lseek(file, -record_size, SEEK_CUR) == -1) {
            throw_error("lseek failed");
        }

        for (int j = i-1; j >=0; --j) {
            if (lseek(file, -record_size, SEEK_CUR) == -1) {
                throw_error("lseek failed");
            }

            if (read(file, chars, record_size) == -1) {
                throw_error("read failed");
            }
            if (lseek(file, -record_size, SEEK_CUR) == -1) {
                throw_error("lseek failed");
            }

            if (chars[0] > key[0]) {

                if (write(file, key, record_size) == -1) {
                    throw_error("write failed");
                }

                if (write(file, chars, record_size) == -1) {
                    throw_error("write failed");
                }
                if (lseek(file, -2 * record_size, SEEK_CUR) == -1) {
                    throw_error("lseek failed");
                }
            }
            else{
                break;
            }
        }
    }

    free(chars);
    free(key);
    close(file);
}


void throw_error(const char message[])
{
    perror(message);
    exit(1);
}
