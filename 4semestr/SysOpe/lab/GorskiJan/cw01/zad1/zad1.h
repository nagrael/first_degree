#ifndef ZAD1_H
#define ZAD1_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
// TO DO
// Everything

typedef struct Elem{
    char* name;
    char* surname;
    char* birthdate;
    char* email;
    char* address;
    char* phone;
} Elem;

typedef struct Node Node;
struct Node{
    Elem* element;
    struct Node* next;
    struct Node* prev;
};

typedef struct List{
    Node* first;
    Node* last;
} List;

bool less_or_equal_than(char* s1, char* s2);

bool equal(char* s1, char* s2);

void print_contact(Elem* n);

void print_one(Node* node);

void print_list(List *list);

Elem *elem_create(char *name, char *surname, char *birthdate, char *email, char *address, char *phone);

Node* node_create(Elem *element);

void element_destroy(Elem *element);

void *node_destroy(Node* node);

List *create_list();

void *list_destroy(List *list);

void list_insert(List *list, Elem *element);

void list_remove(List *list, Node* node);

Node *find_contact(List *list, char*name, char*surname);

Node *split(Node *head);

Node *merge(Node *first, Node *second);

Node *mergeSort(Node *head);

List *sort(List *list);

#endif // ZAD1_H
