//
// Created by Hrayr Stepanyan on 19.01.25.
//

#ifndef OPEN_ADDRESS_H
#define OPEN_ADDRESS_H

#include <stddef.h>
#include "hash.h"

typedef struct Data
{
    size_t size;
    void* data; // any kind of data
} Data;

typedef struct HashTable
{
    Hash size;
    Data* data;
} HashTable;

Data* create_data(size_t size, void* data);
HashTable* createHashTable(Hash size);
void addToHashTable(HashTable* hashTable, Hash hash, Data* value);
float getHashTableLoadFactor(HashTable* hashTable);
Data* searchByHash(HashTable* hashTable, Hash hash);

#endif //OPEN_ADDRESS_H
