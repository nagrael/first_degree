#include "generator.h"

int main(int argc, char *argv[])
{
    if (argc < 4) {
        puts("usage: ./generator file_name record_size number_of_records");
        return EXIT_FAILURE;
    }

    srand((unsigned int) time(NULL));
    generate(argv[1], atoi(argv[3]), (size_t) atoi(argv[2]));

    return EXIT_SUCCESS;
}

void generate(char *file_name, int records_number, size_t record_size)
{
    FILE *file;
    if (!(file = fopen(file_name, "w+"))) {
        throw_error("cannot open file");
    }

    for (int i = 0; i < records_number; ++i) {
        unsigned char *chars = malloc(record_size);

        for (int j = 0; j < record_size; ++j) {
            chars[j] = (unsigned char) (rand() % 10 + (int) '0');
        }

        fwrite(chars, sizeof(char), record_size, file);
        free(chars);
    }

    fclose(file);
}

void throw_error(const char message[])
{
    perror(message);
    exit(1);
}
