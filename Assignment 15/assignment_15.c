#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_THREADS 4
#define INCREMENTS 1000000

int unsynced_counter = 0;
int synced_counter = 0;
pthread_mutex_t mutex;

void* increment_unsync(void* arg) {
    for (int i = 0; i < INCREMENTS; i++) {
        unsynced_counter++;
    }
    return NULL;
}

void* increment_sync(void* arg) {
    for (int i = 0; i < INCREMENTS; i++) {
        pthread_mutex_lock(&mutex);
        synced_counter++;
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];          //unsync

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, increment_unsync, NULL);
    }
    
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_init(&mutex, NULL);             //sync

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, increment_sync, NULL);
    }
    
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&mutex);            // result display

    printf("Expected Counter Value: %d\n", NUM_THREADS * INCREMENTS);
    printf("Unsynchronized Counter Value: %d\n", unsynced_counter);
    printf("Synchronized Counter Value: %d\n", synced_counter);

    return 0;
}