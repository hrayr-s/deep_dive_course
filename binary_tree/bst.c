#include "bst.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void add(struct Node* node, Hash value)
{
    if (node->value == value)
    {
        printf("Value %llu is already present in the BST", value);
        return;
    }

    if ((node->ordering && value < node->value) || (!node->ordering && value > node->value))
    {
        if (node->left != NULL)
        {
            add(node->left, value);
            return;
        }
        else
        {
            node->left = new_node(value, node);
        }
    }
    else
    {
        if (node->right != NULL)
        {
            add(node->right, value);
            return;
        }
        else
        {
            node->right = new_node(value, node);
        }
    }
}

struct Node* lower(struct Node* node)
{
    if (node->ordering)
    {
        return node->left;
    }
    return node->right;
}

struct Node* higher(struct Node* node)
{
    if (node->ordering)
    {
        return node->right;
    }
    return node->left;
}

struct Node* look_for(struct Node* node, Hash value)
{
    if (node->value == value)
    {
        return node;
    }
    struct Node* low_node = lower(node);
    struct Node* high_node = higher(node);
    if (low_node != NULL && value < low_node->value)
    {
        return look_for(low_node, value);
    }
    if (high_node != NULL && value > high_node->value)
    {
        return look_for(high_node, value);
    }
    return NULL;
}

struct Node* minimum(struct Node* node)
{
    struct Node* low_node = lower(node);
    if (low_node == NULL)
    {
        return node;
    }
    return minimum(low_node);
}

struct Node* maximum(struct Node* node)
{
    struct Node* high_node = higher(node);
    if (high_node == NULL)
    {
        return node;
    }
    return maximum(high_node);
}


// Initialize the struct and assign function pointers
void init_node_struct(Node* node)
{
    node->add = add;
    node->lower = lower;
    node->higher = higher;
}


struct Node* new_node(Hash value, struct Node* parent)
{
    struct Node* node = (struct Node*)malloc(sizeof(struct Node));
    init_node_struct(node);
    if (!node)
    {
        perror("Failed to allocate memory");
        exit(EXIT_FAILURE);
    }
    node->value = value;
    node->parent = parent;
    if (parent != NULL)
    {
        node->ordering = node->parent->ordering;
    }
    else
    {
        node->ordering = true; // ascending
    }
    return node;
}
