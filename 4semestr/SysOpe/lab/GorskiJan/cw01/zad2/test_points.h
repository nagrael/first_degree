#ifndef TEST_POINTS_H
#define TEST_POINTS_H

#include <dlfcn.h>
#include <stdio.h>
#include <sys/times.h>
#include <time.h>


void print_time_diff(clock_t prev, struct tms* t0, clock_t curr,  struct tms* t1);
void print_time_diff_start(clock_t prev, struct tms* t0, clock_t curr,  struct tms* t1);
void print_time_diff_prev(clock_t prev, struct tms* t0, clock_t curr,  struct tms* t1);



#endif // TEST_POINTS_H
