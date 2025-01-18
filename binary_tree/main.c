#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "bst.h"

int main() {
    unsigned long long nodes_list[] = {72, 44, 60, 62, 83, 63, 56, 46, 80, 25, 15, 54, 92, 84, 96, 28, 58, 8, 7};
    size_t node_list_len = sizeof(nodes_list) / sizeof(nodes_list[0])
    struct Node* root_node = new_node(72, NULL);
    for (int i = 1; i < node_list_len; i++) {
        root_node->add(root_node, value);
    }
    return 0;
}