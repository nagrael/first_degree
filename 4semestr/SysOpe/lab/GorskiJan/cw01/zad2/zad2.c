#include "zad2.h"
// TO DO
// Everything

bool less_or_equal_than(char* s1, char* s2){
  return strcmp(s1,s2)<=0;
}

bool equal(char* s1, char* s2){
  return strcmp(s1,s2)==0;
}

void print_contact(Elem* n){
  printf("Name: %s %s\nBirthdate: %s\nE-mail: %s\nAddress: %s, Phone: %s\n\n",n->name,n->surname,n->birthdate,n->email,n->address,n->phone);
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

List* create_simple_list(){
  List *list = create_list();

  Elem *element;
  element=elem_create("Jan","Kowalski","1-1-1998","eda.mail@mail.com","ul.cos","5098641");
  list_insert(list,element);
  element = elem_create("Katarzyna", "Nowak", "1.1.1999","email@com.pl","ul. kos","84886468");
  list_insert(list,element);
  element = elem_create("Aleksandra", "Zuzak", "6.2.1989","in_wow-mail@com.pl","ul.bos","926904620");
  list_insert(list,element);
  element = elem_create("Milosz", "Egerad", "1.9.1968","super_rus_mail@pl.com.pl","ul. nos","38948931");
  list_insert(list,element);
  printf("Dodalem 4  ludzi do listy\n");
  print_list(list);
  return list;
}

void sort_test(List* list){
  printf("Sortowanie merge-sortem")
  sort(list);
  printf("Po sortowaniu:\n");
  print_list(list);
}

void find_test(List* list){
  printf("Testy szukania\n");
  printf("Kowalki ma wezel pod adresem %p\n",find_contact(list,"Jan","Kowalski"));
  printf("Nowak ma wezel pod adresem %p\n",find_contact(list,"Jan","Nowak"));
  printf("Brzeczyk ma wezel pod adresem %p\n",find_contact(list,"Adam","Brzeczyk"));
}

void end_test(List* list){
  printf("Koncze test, usuwam liste\n");
  list_destroy(list);
}
