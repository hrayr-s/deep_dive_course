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

    void         (*add)(struct Node* node, Hash value);
    struct Node* (*lower)(struct Node* node);
    struct Node* (*higher)(struct Node* node);
} Node;

struct Node* new_node(Hash value, struct Node* parent);
struct Node* look_for(struct Node* node, Hash value);
struct Node* minimum(struct Node* node);
struct Node* maximum(struct Node* node);

#endif
