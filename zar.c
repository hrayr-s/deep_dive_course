#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>
#include <sys/time.h>


volatile int* state;
volatile int count;
pthread_barrier_t barrier;
pthread_barrier_t calc_barrier;

//void* incrementor() {
//    while(1) {
//        state++;
//        sleep(1);
//    }
//    return NULL;
//}


//void* handler() {
//    int current_state = 0, new_state = 0;
//    int wait_time;
//
//    while(1) {
//        new_state = state;
//        for (; current_state <= new_state; current_state++) {
//            if (current_state % 2 == 0) {  // state A
//                printf("State -- A --\n");
//                continue;
//            }
//            if (current_state % 2 == 1) {
//                printf("State -- B --\n");
//                continue;
//            }
//        }
//        wait_time = rand() % 3 + 1;
//        printf("waiting for %d seconds\n", wait_time);
//        sleep(wait_time);
//    }
//}


void* rand_zar(void* arg) {
    int id = *(int*)arg;
    while(1) {
        pthread_barrier_wait(&calc_barrier);
        state[id] = rand() % 1000000;
        pthread_barrier_wait(&barrier);
    }
    return NULL;
}

void* get_max()
{
    int max = 0;
    while(1)
    {
        pthread_barrier_wait(&barrier);
        max = state[0];
        printf("%d ", state[0]);
        for (int i = 1; i < count; i++)
        {
            if (max < state[i])
            {
                max = state[i];
            }
            printf("%d ", state[i]);
        }
        printf("max = %d\n", max);
        sleep(1);
        pthread_barrier_wait(&calc_barrier);
    }
}

int main() {
    srand(time(NULL));
    count = 10;
    pthread_t th[count+1];
    pthread_barrier_init(&barrier, NULL, count);
    pthread_barrier_init(&calc_barrier, NULL, count + 1);

    state = malloc(count * sizeof(int));
    int thread_ids[count];

    for (int i = 0; i < count; i++) {  // one more thread for max calculator
        thread_ids[i] = i; // Assign a unique ID to each thread
        pthread_create(&th[i], NULL, rand_zar, (void*)&thread_ids[i]);
    }

    pthread_create(&th[count], NULL, get_max, NULL);

    for (int i = 0; i <= count; i++)
    {
        pthread_join(th[i], NULL);
    }
    printf("Done\n");
}