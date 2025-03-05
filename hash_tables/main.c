//
// Created by Hrayr Stepanyan on 20.01.25.
//
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>
#include <stdarg.h>
#include "open_address.h"

#define INITIAL_CAPACITY 16

int main()
{
    printf("HASHTABLES\n");
    HashTable* tb = createHashTable(16);

    char* command = NULL;
    char* exit_cmd = "exit";
    char* print_cmd = "print";

    size_t len = 0;
    while (1)
    {
        printf("\n> ");
        ssize_t read = getline(&command, &len, stdin);
        if (read != -1)
        {
            // Remove the trailing newline character if present
            if (read > 0 && command[read - 1] == '\n')
            {
                command[read - 1] = '\0';
            }

            if (strcmp(command, exit_cmd) == 0)
            {
                break;
            }

            if (strcmp(command, print_cmd) == 0) {
                for (int i=0; i < tb->size; i++) {
                    printf("Hash #%i has data with %lu bytes\n", i, tb->data[i].size);
                    printf("Hash #%i has data %s\n", i, (char*)tb->data[i].data);
                }
                continue;
            }

            if (command[0] == '\0') continue; // skip empty enters

            Hash new_hash = hasher(command, tb->size);
            addToHashTable(tb, new_hash, create_data(strlen(command), (void*)command));
            printf("Hash: %llu", new_hash);
        }
        else
        {
            perror("getline failed");
        }
    }
    free(command);
    printf("Exiting...\n");
    return 0;
}