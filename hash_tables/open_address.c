#include "open_address.h"
#include <stdlib.h>
#include <string.h>

#include "hash.h"

Data* create_data(size_t size, void* data)
{
  Data* _data = malloc(sizeof(Data));
  _data->data = malloc(size);
  _data->size = size;
  memcpy(_data->data, data, size);
  return _data;
}

HashTable* createHashTable(Hash size)
{
    HashTable* hashTable = malloc(sizeof(HashTable));
    hashTable->size = size;
    hashTable->data = (Data*)malloc(sizeof(Data*) * size);
    return hashTable;
}

void addHashTableDataAt(HashTable* hashTable, Hash index, Data* data)
{
    hashTable->data[index].data = malloc(data->size * sizeof(data->data));
    memcpy(hashTable->data[index].data, data->data, data->size * sizeof(data->data));
    hashTable->data[index].size = data->size;
}

void addToHashTable(HashTable* hashTable, Hash hash, Data* data)
{
    if (hashTable->data[hash].data == NULL)
    {
        addHashTableDataAt(hashTable, hash, data);
        return;
    }
    for (Hash i = hash; i < hashTable->size; i++)
    {
        if (hashTable->data[i].data == NULL)
        {
            addHashTableDataAt(hashTable, i, data);
            return;
        }
    }

    for (Hash i = 0; i < hash; i++)
    {
        if (hashTable->data[i].data == NULL)
        {
            addHashTableDataAt(hashTable, i, data);
            return;
        }
    }
    // If we came so far it means hash table is full 100%
    // TODO implement HashTable resize here to extend the HashTable size
}

float getHashTableLoadFactor(HashTable* hashTable)
{
    size_t loadFactor = 0;
    for (Hash i = 0; i < hashTable->size; i++)
    {
        if (hashTable->data[i].data == NULL) continue;
        loadFactor++;
    }
    return loadFactor / hashTable->size;
}
