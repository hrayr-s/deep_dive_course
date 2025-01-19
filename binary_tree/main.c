#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>
#include <stdarg.h>

#include "bst.h"

/**
 * Assertion for specific condition and print the error message from formatted string.
 * The function accepts formatting arguments as if it would be done for `printf` function.
 *
 * @param condition boolean, if false prints formatted message
 * @param message the formatted message
 * @param ... formatting arguments
 */
void assertf(bool condition, char *message, ...)
{
    if (!condition)
    {
        va_list args;

        // Initialize va_list with the ellipsis
        va_start(args, message);
        char *formatted_message = (char*)malloc(strlen(message) + 1);
        vsprintf(formatted_message, message, args);
        fprintf(stderr, "%s\n", formatted_message);
        perror("\n");
        exit(EXIT_FAILURE);
        // Clean up the va_list
        va_end(args);
    }
}

int main()
{
    Hash nodes_list[] = {72, 44, 60, 62, 83, 63, 56, 46, 80, 25, 15, 54, 92, 84, 96, 28, 58, 8, 7};
    size_t node_list_len = sizeof(nodes_list) / sizeof(nodes_list[0]);
    Node* root_node = new_node(72, NULL);
    for (int i = 1; i < node_list_len; i++)
    {
        root_node->add(root_node, nodes_list[i]);
    }

    // Test the code
    assertf(validate(root_node, NULL, NULL), "Invalid tree");
    delete(root_node, 83);

    assertf(validate(root_node, NULL, NULL), "The tree is invalid");
    assertf(root_node->right->value == 84, "Expected 84 on right side got %llu", root_node->right->value);
    assertf(root_node->right->parent == root_node, "Expected replaced parent to be %llu, got %llu", root_node->value, root_node->right->parent->value);
    assertf(root_node->right->left != NULL, "Expected 80 for root_node->right->left, got NULL");
    assertf(root_node->right->left->parent == root_node->right, "Expected %llu for root_node->right->left->parent, got %llu", root_node->right->value, root_node->right->left->parent->value);
    assertf(root_node->right->right != NULL && root_node->right->right->parent == root_node->right, "Expected %llu for root_node->right->right->parent, got %llu", root_node->right->value, root_node->right->right->parent->value);
    assertf(root_node->left->parent == root_node, "Expected %llu parent to be the root node, got %llu", root_node->left->value, root_node->left->parent->value);

    // Check before mirroring
    assertf(root_node->left->value == 44, "Expect 44 on left node, got %llu", root_node->left->value);
    mirror_recursively(root_node);
    assertf(root_node->right->value == 44,  "Expected 44 on right node, got %llu", root_node->right->value);
    assertf(root_node->left->value == 84,  "Expected 84 on left node, got %llu", root_node->left->value);
    assertf(!root_node->ordering, "Expected root node ordering to be false - means Descending ordering");

    // revert mirroring
    mirror_recursively(root_node);
    assertf(root_node->ordering, "Expected root node ordering to be true - means ascending");

    delete(root_node, 80);
    assertf(validate(root_node, NULL, NULL), "Invalid tree");
    assertf(root_node->right->value==84,  "Expected 94 on right side, got %llu", root_node->right->value);
    assertf(root_node->right->left == NULL, "Expected %llu to be NULL", root_node->right->value);

    delete(root_node, 92);
    assertf(validate(root_node, NULL, NULL), "Invalid tree");
    assertf(root_node->right->right->value == 96,  "Expected 96 on right side, got %llu", root_node->right->value);

    delete(root_node, 15);
    assertf(validate(root_node, NULL, NULL), "Invalid tree");
    assertf(root_node->left->left->left->value == 8, "Expected 8 on left node, got %llu", root_node->left->left->left->value);

    delete(root_node, 46);
    assertf(validate(root_node, NULL, NULL), "Invalid tree");
    assertf(look_for(root_node, 56)->left->value == 54, "Expected 54 on left side of node '56', got %llu", look_for(root_node, 56)->left->value);

    root_node->add(root_node, 46);
    assertf(validate(root_node, NULL, NULL), "Invalid tree");
    assertf(look_for(root_node, 54)->left->value == 46, "Expected 46 to be added on 54 left side, got %llu", look_for(root_node, 54)->left->value);
    return 0;
}
