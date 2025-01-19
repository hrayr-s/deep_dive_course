#include "bst.h"

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>

void add(Node* node, Hash value)
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

Node* lower(Node* node)
{
    if (node->ordering)
    {
        return node->left;
    }
    return node->right;
}

Node* higher(Node* node)
{
    if (node->ordering)
    {
        return node->right;
    }
    return node->left;
}

Node* look_for(Node* node, Hash value)
{
    if (node->value == value)
    {
        return node;
    }
    Node* low_node = lower(node);
    Node* high_node = higher(node);
    if (low_node != NULL && value < node->value)
    {
        return look_for(low_node, value);
    }
    if (high_node != NULL && value > node->value)
    {
        return look_for(high_node, value);
    }
    return NULL;
}

Node* minimum(Node* node)
{
    Node* low_node = lower(node);
    if (low_node == NULL)
    {
        return node;
    }
    return minimum(low_node);
}

Node* maximum(Node* node)
{
    Node* high_node = higher(node);
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


Node* new_node(Hash value, Node* parent)
{
    Node* node = (Node*)malloc(sizeof(struct Node));
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

bool validate(Node* node, Node* minimum, Node* maximum)
{
    if (
        (minimum != NULL && node->value < minimum->value)
        || (maximum != NULL && node->value > maximum->value)
    )
    {
        return false;
    }
    if (
        (node->left == NULL || validate(node->left, minimum, node))
        && (node->right == NULL || validate(node->right, node, maximum))
    )
        return true;
    return false;
}

/* Function: delete
 * ----------------
 *
 * deletes Node with given value from give node
 * node: Node to delete from
 * value: eq. Hash value to delete
 *
 */
void delete(Node* root_node, Hash value)
{
    Node* node = look_for(root_node, value);
    if (node == NULL)
    {
        printf("Value %llu is not present in the BST", value);
        return;
    }
    if (node->left == NULL && node->right == NULL)
    {
        // delete a node with no branches
        if (node->parent->left == node)
            node->parent->left = NULL;
        else
            node->parent->right = NULL;
        free(node);
        return;
    }

    // define replacement, we fill when find a replacement
    Node* replacement = NULL;

    if (node->left != NULL && node->right == NULL)
    {
        replacement = node->left;
    }
    else if (node->right != NULL && node->left == NULL)
    {
        replacement = node->right;
    }
    else if (node->left != NULL && node->right != NULL)
    {
        // We will always look for right node minimum for replacement
        // Not the optimized way for this kind of tree. Can be re-implemented
        replacement = minimum(node->right);
    }

    if (replacement != NULL)
    {
        // take care of sub-node
        attach_sub_node_to_parent(replacement);

        // attach replacement to node's parent
        if (node->parent->left == node)
        {
            node->parent->left = replacement;
        }
        else
        {
            node->parent->right = replacement;
        }
        replacement->parent = node->parent;

        set_parent(replacement, node->left, true);
        set_parent(replacement, node->right, false);

        // free the memory
        free(node);
    }
}

/**
 * Link node to parent on parent left or right branch
 *
 * @param parent parent node
 * @param node future child node
 * @param Left if true place on left, otherwise on right
 */
void set_parent(Node* parent, Node* node, bool Left)
{
    if (node->parent->left == node)
    {
        node->parent->left = NULL;
    } else
    {
        node->parent->right = NULL;
    }

    node->parent = parent;
    if (Left == true)
    {
        parent->left = node;
    } else
    {
        parent->right = node;
    }
}

/**
 * The function attaches the child node of given node to the parent node.
 * Assuming that the node has only one child.
 * @param node
 */
void attach_sub_node_to_parent(Node* node)
{
    if (node->parent == NULL)
    {
        printf("Parent is NULL for node %llu\n", node->value);
        return;
    }
    if (node->left != NULL && node->right != NULL)
    {
        printf("Node %llu has two children. Cannot make operation `attach_sub_node_to_parent` on this kind of node\n",
               node->value);
        return;
    }
    Node* attachment = NULL;
    if (node->left != NULL)
    {
        attachment = node->left;
    }
    else if (node->right != NULL)
    {
        attachment = node->right;
    }
    else
    {
        if (node->parent->left == node)
        {
            node->parent->left = NULL;
        }
        else
        {
            node->parent->right = NULL;
        }
        // nothing to attach
        return;
    }
    if (node->parent->right == node)
    {
        node->parent->right = attachment;
    }
    else if (node->parent->left == node)
    {
        node->parent->left = attachment;
    }
    else
    {
        printf("Node %llu is invalid!", node->value);
    }
    attachment->parent = node->parent;
}

void mirror_recursively(Node* node)
{

    Node* temp = node->left;
    node->left = node->right;
    node->right = temp;
    node->ordering = !node->ordering;
    if (node->left != NULL)
    {
        mirror_recursively(node->left);
    }
    if (node->right != NULL)
    {
        mirror_recursively(node->right);
    }
}

// void mirror_in_loop(Node* node)
// {
//
// }
