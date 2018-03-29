#include "zad2.h"
#include "test_points.h"



int main(){
#ifdef DYNAMIC
  void *handle = dlopen("./liblist.so",RTLD_LAZY);
  List* (*create_simple_list)(void) = dlsym(handle,"create_simple_list");
  void (*sort_test)(List*) = dlsym(handle,"sort_test");
  void (*find_test)(List*) = dlsym(handle,"find_test");
  void (*end_test)(List*) = dlsym(handle,"end_test");

#endif

  List* list;
  struct tms t0,t1,t2,t3,t4;
  clock_t start_time,prev_time,curr_time;

  start_time=clock();
  prev_time=start_time;
  times(&t0);
  list=create_simple_list();
  curr_time=clock();
  times(&t1);
  print_time_diff_start(start_time,&t0,curr_time,&t1);
  sort_test(list);
  prev_time=curr_time;
  curr_time=clock();
  times(&t2);
  print_time_diff_start(start_time,&t0,curr_time,&t2);
  print_time_diff_prev(prev_time,&t1,curr_time,&t2);
  find_test(list);
  prev_time=curr_time;
  curr_time=clock();
  times(&t3);
  print_time_diff_start(start_time,&t0,curr_time,&t3);
  print_time_diff_prev(prev_time,&t2,curr_time,&t3);
  end_test(list);
  prev_time=curr_time;
  curr_time=clock();
  times(&t4);
  print_time_diff_start(start_time,&t0,curr_time,&t4);
  print_time_diff_prev(prev_time,&t3,curr_time,&t4);


  #ifdef DYNAMIC
  dlclose(handle);
  #endif

  return 0;
}

void print_time_diff(clock_t prev, struct tms* t0, clock_t curr,  struct tms* t1){
  printf("czas rzeczywisty: %lf\nczas uzytkownika: %lf\nczas systemowy %lf\n\n",(double)(curr-prev)/CLOCKS_PER_SEC,(double)(t1->tms_utime-t0->tms_utime)/CLOCKS_PER_SEC,(double)(t1->tms_stime-t0->tms_stime)/CLOCKS_PER_SEC);
}


void print_time_diff_start(clock_t prev, struct tms* t0, clock_t curr,  struct tms* t1){
  printf("\nCzas od poczatku do teraz:\n");
  print_time_diff(prev,t0,curr,t1);
}


void print_time_diff_prev(clock_t prev, struct tms* t0, clock_t curr,  struct tms* t1){
  printf("Czas od poprzedniego punktu kontrolnego:\n");
  print_time_diff(prev,t0,curr,t1);
}
