#include "lock.h"

int main(int argc, char *argv[])
{
    if (argc < 2) {
        puts("usage: ./lock file_path");
        return EXIT_FAILURE;
    }

    char *file_path;
    int file, file_size;
    struct stat my_stat;

    file_path = argv[1];

    if ((file = open(file_path, O_RDWR)) < 0) {
        throw_error("Cannot open file");
    }


    stat(file_path, &my_stat);
    file_size = (int) my_stat.st_size;

    int option = -1;

    while(option){
        show_options();
        option = get_option();
        switch (option) {
            case 1: // Lock byte reading

                lock_read(file, get_byte_index(file_size));
                break;

            case 2: // Lock byte writing

                lock_write(file, get_byte_index(file_size));
                break;

            case 3: // List locked bytes
                print_locked_bytes(file, file_size);
                break;

            case 4: // Remove lock
                remove_lock(file, get_byte_index(file_size));

                break;

            case 5: ; // Read byte
                char newest_byte = get_byte_index(file_size);
                printf("%d byte = %c\n", newest_byte, read_byte(file,newest_byte));
                break;

            case 6: // Write byte
                printf("Provide new byte to write:\n ");
                char new_byte;
                scanf("%c", &new_byte);
                write_byte(file, get_byte_index(file_size), &new_byte);

                break;

        }
    }

    close(file);

    return EXIT_SUCCESS;
}

void show_options()
{
    puts("1: Lock byte reading");
    puts("2: Lock byte writing");
    puts("3: List locked bytes");
    puts("4: Remove lock");
    puts("5: Read byte");
    puts("6: Write byte");
    puts("0: Exit");
}

int get_option()
{
    int option;

    printf("\nMy choice: ");
    scanf("%d", &option);
    while (0>option || option >6){
    printf("Wrong choice. Try again: ");
    scanf("%d", &option);
    }
    return option;
}

void lock_read(int file, int byte_index)
{
    struct flock lock;

    lock.l_type = F_RDLCK;
    lock.l_start = byte_index;
    lock.l_whence = SEEK_SET;
    lock.l_len = 1;
    lock.l_pid    = getpid();

    if (fcntl(file, F_SETLK, &lock) == -1) {
        throw_error("Cannot set read lock");
    } else {
        printf("Read lock for byte index: %d was set\n", byte_index);
    }
}

void lock_write(int file, int byte_index)
{
    struct flock lock;

    lock.l_type = F_WRLCK;
    lock.l_start = byte_index;
    lock.l_whence = SEEK_SET;
    lock.l_len = 1;
    lock.l_pid    = getpid();

    if (fcntl(file, F_SETLK, &lock) == -1) {
        throw_error("Cannot set write lock");
    } else {
        printf("Write lock for byte index: %d was set\n", byte_index);
    }
}

void remove_lock(int file, int byte_index)
{
    struct flock lock;

    lock.l_type = F_UNLCK;
    lock.l_start = byte_index;
    lock.l_whence = SEEK_SET;
    lock.l_len = 1;
    lock.l_pid    = getpid();

    if (fcntl(file, F_SETLK, &lock) == -1) {
        throw_error("Cannot release lock");
    } else {
        printf("Lock for byte index: %d was removed\n", byte_index);
    }
}

void print_locked_bytes(int file, int file_size)
{
    puts("Locked bytes:");
    struct flock lock;
    for (int i = 0; i < file_size; ++i) {


        lock.l_type = F_WRLCK;
        lock.l_start = i;
        lock.l_whence = SEEK_SET;
        lock.l_len = 1;
        if(fcntl(file, F_GETLK, &lock) == -1){
            throw_error("Cannot check locks");
        }

        if (lock.l_type != F_UNLCK) {
            printf("Byte index: %d locked by process: %d with lock: %s\n", i, lock.l_pid, (lock.l_type==F_WRLCK)? "Write block" : "Read block");
        }
    }
}

char read_byte(int file, int byte_index)
{
    char ret[1];

    lseek(file, byte_index, SEEK_SET);
    read(file, ret, 1);

    return ret[0];
}

void write_byte(int file, int byte_index, char *byte)
{
    lseek(file, byte_index, SEEK_SET);
    write(file, byte, 1);
}

int get_byte_index(int file_size)
{
    int byte;

    printf("Provide byte index.\n");
    scanf("%d", &byte);

    while (byte < 0 || file_size < byte) {
        printf("Size need to be between 0 and file size!\nProvide byte index:\n");
        scanf("%d", &byte);
    }
    return byte;
}

void throw_error(const char *message)
{
    perror(message);
    exit(1);
}
