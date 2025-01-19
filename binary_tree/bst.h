#ifndef BST_DEFINED_H
#define BST_DEFINED_H
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

typedef unsigned long long Hash;

typedef struct Node
{
    Hash value;
    struct Node* left;
    struct Node* right;
    struct Node* parent;
    bool ordering; // true -> ascending, false -> descending

    void (*add)(struct Node* node, Hash value);
    struct Node* (*lower)(struct Node* node);
    struct Node* (*higher)(struct Node* node);
} Node;

Node* new_node(Hash value, Node* parent);
Node* look_for(Node* node, Hash value);
Node* minimum(Node* node);
Node* maximum(Node* node);
bool validate(Node* node, Node* minimum, Node* maximum);
void delete(Node* node, Hash value);
void attach_sub_node_to_parent(Node* node);
void set_parent(Node* node, Node* parent, bool Left);
void mirror_recursively(Node* node);

Node* prev_or_next(Node* node, bool prev_next);

Node* next_node(Node* node);
Node* prev_node(Node* node);

#endif
