//
// Created by Hrayr Stepanyan on 20.01.25.
//
#include <stdio.h>
#include <stdlib.h>
#include "hash.h"

Hash hasher(char* value, Hash hashtable_size) {
    Hash hash = 0;
    Hash prime_pow = 89;
    for (int i=0; value[i] !='\0'; i++) {
        hash += prime_pow * value[i];
        prime_pow = prime_pow * prime_pow;
        if (i % 2 == 1) {
            prime_pow = prime_pow * 7;
        }
    }
    while(hash > hashtable_size) {
        hash = hash % hashtable_size;
    }
    hash = hash + 1;

    return hash;
}
