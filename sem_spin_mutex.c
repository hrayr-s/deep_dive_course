#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <semaphore.h>

#define NUM_ITERATIONS 1000000

// Shared counter
volatile int counter = 0;

volatile int sem = 0;

sem_t mutex;

void* up() {
    while (sem > 0) {}
    sem++;
    return NULL;
}

void* down()
{
    sem--;
    return NULL;
}

// Function for incrementing the counter (Critical Section)
void *increment_counter(void *arg) {
    for (int i = 0; i < NUM_ITERATIONS; i++) {
        // Critical Section: Increment the shared counter
        // Use all 3 mechanisms to sync this section. Keep two of them commented out.

        sem_wait(&mutex);
        counter++;
        sem_post(&mutex);
    }
    return NULL;
}

int main() {
    sem_init(&mutex, 0, 1);
    pthread_t thread1, thread2;
    // Create two threads
    pthread_create(&thread1, NULL, increment_counter, NULL);
    pthread_create(&thread2, NULL, increment_counter, NULL);
    // Wait for threads to finish
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    // Print the final value of the counter
    sleep(2);
    printf("Final Counter: %d\n", counter);
    return 0;
}