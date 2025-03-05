#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include "hash.h"

typedef unsigned long long Hash;


struct LinkList {
    char* value;
    struct LinkList* next;
};

struct HashValue {
    Hash    hash;
    struct LinkList*   values;
};

struct HashTable {
    struct HashValue* map;
    size_t size;
};


// Global variable for HashTable map
struct HashTable* hash_table = NULL;

struct HashValue* getOrCreateHashMapForHash(Hash hash) {
    struct HashValue* mp = NULL;
    int i = 0;
    for(i=0; i < hash_table->size; i++) {
        if (hash_table->map[i].hash == hash) {
            mp = &hash_table->map[i];
            return &hash_table->map[i];
        }
    }
    if (mp == NULL) {
        for(i=0; i < hash_table->size; i++) {
            if ((&hash_table->map[i]) == NULL || hash_table->map[i].hash == 0) {
                hash_table->map[i] = (struct HashValue) {.hash = hash};
                return &hash_table->map[i];
            }
        }
    }
    return mp;
}

void addToHashMapValues(struct LinkList* next, Hash hash, char* value) {
    if (strcmp(next->value, value) == 0) {
        return;
    }
    if (next->next == NULL) {
        next->next = (struct LinkList*)malloc(sizeof(struct LinkList*));
        next->next->value = (char*)malloc(strlen(value) + 1);
        strcpy(next->next->value, value);
        return;
    }
    addToHashMapValues(next->next, hash, value);
}

void addToHashTable(Hash hash, char* value) {
    struct HashValue* hash_value = getOrCreateHashMapForHash(hash);
    if (hash_value->values == NULL) {
        hash_value->values = (struct LinkList*)malloc(sizeof(struct LinkList));
        hash_value->values->value = (char*)malloc(strlen(value) + 1);
        strcpy(hash_value->values->value, value);
        return;
    }
    addToHashMapValues(hash_value->values, hash, value);
}

void printNextVal(struct LinkList* next) {
    if (next == NULL) {
        return;
    }
    printf(" %s", next->value);
    if (next->next == NULL) {
        return;
    }
    printNextVal(next->next);
}

void printHashMap(struct HashValue* hash_value) {
    if (hash_value == NULL || hash_value->hash == 0) {
        printf(".");
        return;
    }
    printf("Hash %llu for ", hash_value->hash);
    printNextVal(hash_value->values);
    printf("\n");
}

int main()
{
    char* command = NULL;
    char* exit_cmd = "exit";
    char* print_cmd = "print";

    size_t hashtable_size = 40;
    hash_table = (struct HashTable*)malloc(sizeof(struct HashTable));
    hash_table->size = hashtable_size;

    hash_table->map = (struct HashValue*)malloc(sizeof(struct HashValue) * hashtable_size);

    for (int i = 0; i < hashtable_size; i++) {
      hash_table->map[i] = (struct HashValue ){.hash=0, .values=NULL};
    }

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
                for (int i=0; i<hashtable_size; i++) {
                    printHashMap(&hash_table->map[i]);
                }
                continue;
            }

            if (command[0] == '\0') continue; // skip empty enters

            Hash new_hash;
            new_hash = hasher(command, hashtable_size);
            addToHashTable(new_hash, command);


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
