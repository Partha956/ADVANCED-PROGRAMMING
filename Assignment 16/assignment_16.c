#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define BUFFER_SIZE 5
#define ITEMS_PER_THREAD 8
#define NUM_PRODUCERS 2
#define NUM_CONSUMERS 2

int buffer[BUFFER_SIZE];
int count = 0;

pthread_mutex_t mutex;
pthread_cond_t cond_not_full;
pthread_cond_t cond_not_empty;

void* producer(void* arg) {
    int id = *((int*)arg);
    for (int i = 0; i < ITEMS_PER_THREAD; i++) {
        pthread_mutex_lock(&mutex);
        
        while (count == BUFFER_SIZE) {
            printf("[Producer %d] Buffer FULL. Waiting for signal...\n", id);
            pthread_cond_wait(&cond_not_full, &mutex);
        }
        
        buffer[count] = i;
        count++;
        printf("[Producer %d] Produced item %d. (Buffer count: %d)\n", id, i, count);
        
        pthread_cond_signal(&cond_not_empty);
        pthread_mutex_unlock(&mutex);
        
        usleep(100000);
    }
    return NULL;
}

void* consumer(void* arg) {
    int id = *((int*)arg);
    for (int i = 0; i < ITEMS_PER_THREAD; i++) {
        pthread_mutex_lock(&mutex);
        
        while (count == 0) {
            printf("[Consumer %d] Buffer EMPTY. Waiting for signal...\n", id);
            pthread_cond_wait(&cond_not_empty, &mutex);
        }
        
        int item = buffer[count - 1];
        count--;
        printf("[Consumer %d] Consumed item %d. (Buffer count: %d)\n", id, item, count);
        
        pthread_cond_signal(&cond_not_full);
        pthread_mutex_unlock(&mutex);
        
        usleep(150000);
    }
    return NULL;
}

int main() {
    pthread_t producers[NUM_PRODUCERS];
    pthread_t consumers[NUM_CONSUMERS];
    int prod_ids[NUM_PRODUCERS];
    int cons_ids[NUM_CONSUMERS];

    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&cond_not_full, NULL);
    pthread_cond_init(&cond_not_empty, NULL);

    for (int i = 0; i < NUM_PRODUCERS; i++) {
        prod_ids[i] = i + 1;
        pthread_create(&producers[i], NULL, producer, &prod_ids[i]);
    }

    for (int i = 0; i < NUM_CONSUMERS; i++) {
        cons_ids[i] = i + 1;
        pthread_create(&consumers[i], NULL, consumer, &cons_ids[i]);
    }

    for (int i = 0; i < NUM_PRODUCERS; i++) {
        pthread_join(producers[i], NULL);
    }

    for (int i = 0; i < NUM_CONSUMERS; i++) {
        pthread_join(consumers[i], NULL);
    }

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond_not_full);
    pthread_cond_destroy(&cond_not_empty);

    printf("All production and consumption completed successfully.\n");
    return 0;
}