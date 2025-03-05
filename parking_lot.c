#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>
#include <sys/time.h>

#define MAX_INPUTS 2
#define MAX_OUTPUTS 2
#define PARKING_LOT_SIZE 20


volatile int counter = 0;
volatile int sem_up = 0;

void* up() {
  while (sem_up>=PARKING_LOT_SIZE);
  sem_up++;
  return NULL;
}

void* down() {
  while (sem_up<=0);
  sem_up--;
  return NULL;
}


//volatile int* lots[PARKING_LOT_SIZE];


void* park_car() {
//  int park_at;
  int wait_time = 0;

  while(1) {
//    park_at = rand() % (PARKING_LOT_SIZE + 1);
    up();
    wait_time = rand() % 5 + 1;
    printf("Parking lot filled #%d\n", sem_up);
    // printf("Parked: waiting %d seconds for another car\n", wait_time);
    sleep(wait_time);
  }
}

void* cars_leaving() {
  int wait_time = 0;
  while(1) {
    wait_time = rand() % 10 + 1;
    sleep(wait_time);
    down();
    printf("Parking lot filled #%d\nParked: waited %d seconds a car to leave!\n", sem_up, wait_time);
  }
}


int main() {
  srand(time(NULL));
  pthread_t* parking_threads = (pthread_t*)malloc(sizeof(pthread_t) * MAX_INPUTS);
  pthread_t* leaving_threads = (pthread_t*)malloc(sizeof(pthread_t) * MAX_INPUTS);

  for (int i = 0; i < MAX_INPUTS; i++) {
    pthread_create(&parking_threads[i], NULL, park_car, NULL);
  }

  for (int i = 0; i < MAX_OUTPUTS; i++) {
    pthread_create(&leaving_threads[i], NULL, cars_leaving, NULL);
  }

  // JOIN Threads
  for (int i = 0; i < MAX_INPUTS; i++) {
    pthread_join(parking_threads[i], NULL);
  }
  for (int i = 0; i < MAX_OUTPUTS; i++) {
    pthread_join(leaving_threads[i], NULL);
  }

}