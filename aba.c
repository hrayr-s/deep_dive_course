#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>
#include <sys/time.h>


volatile int state = 0;


void* incrementor() {
    while(1) {
        state++;
        sleep(1);
    }
    return NULL;
}


void* handler() {
    int current_state = 0, new_state = 0;
    int wait_time;

    while(1) {
        new_state = state;
        for (; current_state <= new_state; current_state++) {
            if (current_state % 2 == 0) {  // state A
                printf("State -- A --\n");
                continue;
            }
            if (current_state % 2 == 1) {
                printf("State -- B --\n");
                continue;
            }
        }
        wait_time = rand() % 3 + 1;
        printf("waiting for %d seconds\n", wait_time);
        sleep(wait_time);
    }
}


int main() {
    srand(time(NULL));
    pthread_t thread1, thread2;
    pthread_create(&thread1, NULL, incrementor, NULL);
    pthread_create(&thread2, NULL, handler, NULL);
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    printf("Done\n");
}