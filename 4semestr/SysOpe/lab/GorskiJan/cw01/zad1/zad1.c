#include "zad1.h"
// TO DO
// Everything

bool less_or_equal_than(char* s1, char* s2){
  return strcmp(s1,s2)<=0;
}

bool equal(char* s1, char* s2){
  return strcmp(s1,s2)==0;
}

void print_contact(Elem* n){
  printf("Name: %s %s\nBirthdate: %s\nE-mail: %s\Address: %s, Phone: %s\n\n",n->name,n->surname,n->birthdate,n->email,n->address,n->phone);
}

void print_one(Node* node){
 print_contact(node->element);
}

void print_list(List *list){
 Node* node=list->first;
  while(node){
    print_one(node);
    node=node->next;
  }
  printf("---------\n");
}

Elem *elem_create(char *name, char *surname, char *birthdate, char *email, char *address, char *phone) {
	Elem *element = malloc(sizeof(Elem));

	element->name = name;
	element->surname = surname;
	element->birthdate = birthdate;
	element->email = email;
	element->address = address;
	element->phone = phone;
	return element;
}
Node* node_create(Elem *element){
    Node *node = malloc(sizeof(Node));
    node -> element = element;
    node ->prev = node -> next = NULL;
    return node;
}

void element_destroy(Elem *element){
    free(element->name);
	free(element->surname);
	free(element->birthdate);
	free(element->email);
	free(element->address);
	free(element->phone);
	free(element);
}
void *node_destroy(Node* node){
	if (node == NULL) {
		return;
	}
	element_destroy(node->element);
	free(node);

}

List *create_list(){
    List * list = malloc(sizeof(List));
    list->first = list->last = NULL;
    return list;
}

void *list_destroy(List *list){
    	if (list == NULL) {
		return;
	}

	Node *node = list->first;
	while (node != NULL) {
		Node *tmp = node;
		node = node->next;
		node_destroy(tmp);
	}

	free(list);
}


void list_insert(List *list, Elem *element)
{
	Node *last = list->last;
	Node *new_one = node_create(element);

	if (last == NULL) {
		list->first = list->last = new_one;
		return;
	}

	last->next = new_one;
	new_one->prev = last;
	list->last = new_one;
}

void list_remove(List *list, Node* node){

	if (node == list->first) {
		if (node == list->last) {
			list->first = list->last = NULL;
		} else {
			list->first = list->first->next;
			list->first->prev = NULL;
		}
	} else {
		if (node == list->last) {
			list->last = list->last->prev;
			list->last->next = NULL;
		} else {
			node->prev->next = node->next;
			node->next->prev = node->prev;
		}
	}
	node_destroy(node);
}

Node *find_contact(List *list, char*name, char*surname){
    Node *find = list->first;
    while(find){
       if(equal(name,find->element->name)&& equal(surname,find->element->surname))
            return find;
        find = find->next;
    }
    return NULL;

}

Node *split(Node *head)
{
    Node *fast = head,*slow = head;
    while (fast->next && fast->next->next)
    {
        fast = fast->next->next;
        slow = slow->next;
    }
    Node *temp = slow->next;
    slow->next = NULL;
    return temp;
}

Node *merge(Node *first, Node *second)
{
    // If first linked list is empty
    if (!first)
        return second;

    // If second linked list is empty
    if (!second)
        return first;

    // Pick the smaller value
    if (less_or_equal_than(first->element->surname,second->element->surname))
    {
        first->next = merge(first->next,second);
        first->next->prev = first;
        first->prev = NULL;
        return first;
    }
    else
    {
        second->next = merge(first,second->next);
        second->next->prev = second;
        second->prev = NULL;
        return second;
    }
}

// Function to do merge sort
Node *mergeSort(Node *head)
{
    if (!head || !head->next)
        return head;
    Node *second = split(head);

    // Recur for left and right halves
    head = mergeSort(head);
    second = mergeSort(second);

    // Merge the two sorted halves
    return merge(head,second);
}

List *sort(List *list){
    Node *first = mergeSort(list->first);
    list->first = first;
    while(first->next)
        first=first->next;
    list->last=first;
    return list;

}
