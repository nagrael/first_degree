#include "dir.h"




int  main(int argc, char *argv[])
{
	if (argc < 3) {
		puts("usage: ./dir path xxx");
		return EXIT_FAILURE;
	}

	input_permissions = argv[2];

	puts("List dir");
	list_dir(argv[1], "");

	puts("\nList dir using nftw");
	list_dir_using_nftw(argv[1]);

	return EXIT_SUCCESS;
}

void list_dir(const char *path, const char *real_path)
{

	DIR *dir;
	struct dirent *dirent;

	if (!(dir = opendir(path))) {
		throw_error("Cannot open directory");
	}

	while ((dirent = readdir(dir))) {
		char absolute_path[PATH_MAX], no_path[PATH_MAX], file_permissions[3];
		struct stat my_stat;

		snprintf(absolute_path, sizeof(absolute_path), "%s/%s", path, dirent->d_name);
		stat(absolute_path, &my_stat);

		if (sprintf(file_permissions, "%o", my_stat.st_mode & (S_IRWXU | S_IRWXG | S_IRWXO)) < 0) {
			throw_error("Cannot do sprintf");
		}

		if (dirent->d_type == DT_DIR) {
			if (strcmp(dirent->d_name, ".") != 0 && strcmp(dirent->d_name, "..") != 0) {
                snprintf(no_path, sizeof(no_path), "%s/%s", real_path, dirent->d_name);
				list_dir(absolute_path,  no_path);
			}
		} else if (dirent->d_type == DT_REG && strcmp(input_permissions, file_permissions) == 0) {
		    snprintf(no_path, sizeof(no_path), "%s/%s", real_path, dirent->d_name);
			print_file_info(&my_stat, no_path);
		}
	}

	closedir(dir);
}

void list_dir_using_nftw(const char *path)
{

	if (nftw(path, print_path,20, FTW_F) < 0) {
		throw_error("Error with nftw");
    }

}

int print_path(const char *path, const struct stat *my_stat, int flag)
{
	char file_permissions[3];
	if (sprintf(file_permissions, "%o", my_stat->st_mode & (S_IRWXU | S_IRWXG | S_IRWXO)) < 0) {
		throw_error("Cannot sprintf");
	}

	if (flag == FTW_F && strcmp(file_permissions, input_permissions) == 0) {
		char absolute_path[PATH_MAX];

		if (! realpath(path, absolute_path)) {
			throw_error("Cannot find real path");
		}

		print_file_info(my_stat,absolute_path);
	}

	return 0;
}

void print_file_info(const struct stat *stat, const char *file)
{
	struct tm lt;
	char lm_time[128];
	int size;

	size = (int)stat->st_size;
	localtime_r(&stat->st_atime, &lt);
	strftime(lm_time, sizeof(lm_time), "%c", &lt);

	printf("%s\t%d bytes\tLast access: %s\n", file, size, lm_time);
}

void throw_error(const char message[])
{
	perror(message);
	exit(1);
}
