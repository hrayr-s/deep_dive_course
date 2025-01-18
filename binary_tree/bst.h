#ifndef BST_DEFINED_H
#define BST_DEFINED_H

typedef struct {
    unsigned long long value;
    struct Node* left;
    struct Node* right;
    struct Node* parent;
    bool ordering; // true -> ascending, false -> descending

    void         (*add)(struct Node* node, unsigned long long value);
    struct Node* (*lower)(struct Node* node);
    struct Node* (*higher)(struct Node* node);
} Node;

struct Node* (*new_node)(unsigned long long value, struct Node* parent);
struct Node* look_for(struct Node* node, unsigned long long value);
struct Node* minimum(struct Node* node);
struct Node* maximum(struct Node* node);

##endif
