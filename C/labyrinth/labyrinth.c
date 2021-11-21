#include <stdio.h>
#include <stdlib.h>
#include <conio.h>

#define QUEUE_SIZE 100

typedef struct cd {
    int x;
    int y;
} COORD;

typedef struct qu {
    COORD memory[QUEUE_SIZE];
    int pointer;
} QUEUE;

void push(QUEUE* queue, COORD cd) {
    if (queue->pointer != QUEUE_SIZE)
        queue->memory[queue->pointer++] = cd;
}

COORD pop(QUEUE* queue) {
    if (queue->pointer != 0) {
        COORD coordinates = queue->memory[0];
        for (int i = 0; i < QUEUE_SIZE - 1; ++i)
            queue->memory[i] = queue->memory[i+1];
        queue->pointer--;

        return coordinates;
    }
}

void bfs (COORD start, COORD end, int size) {
    int length = size*size, ar_pointer = 0;
    int** visited = (int**)calloc(length, sizeof(int*));
    for (int i = 0; i < length; ++i)
        visited[i] = (int*)calloc(3, sizeof(int));

    QUEUE queue;
    queue.pointer = 0;
    push(&queue, start);

    while (queue.pointer != 0) {
        COORD cur_xy = pop(&queue);
        if (cur_xy.x == end.x && cur_xy.y == end.y)
            break;

        COORD next_xy[4];
    }
}

char** initMap(char** map, int SIZE) {
    map = (char**)calloc(SIZE, sizeof(char*));
    for (int i = 0; i < SIZE; ++i)
        map[i] = (char*)calloc(SIZE, sizeof(char));
    return map;
}


char** deleteMap(char** map, int size) {
    for (int i = 0; i < size; ++i)
        free(map[i]);
    free(map);
    return NULL;
}

void fillMap(char** map, int size) {
    for (int y = 0; y < size; ++y)
        for (int x = 0; x < size; ++x)
            if ((y == 0) || (x == 0) ||
                    (y == size-1) || (x == size-1))
                map[x][y] = '#';
            else
                map[x][y] = ' ';
}

void printMap(char** map, int size) {
    for (int y = 0; y < size; ++y) {
        for (int x = 0; x < size; ++x)
            printf("%2c", map[x][y]);
        printf("\n");
    }
}

void printInfo() {
    printf("\nUse SHIFT + < - to correct START position(@).\n");
    printf("Use SHIFT + > - to correct END position(&).\n");
    printf("\nUse WASD to move.");
    printf("\n\n");
}

int main() {
    int size = 4;

    char** map = initMap(map, size);
    char button;

    COORD start, end, tmp_coord;
    start.x = 1;
    start.y = 1;

    end.x = size - 2;
    end.y = size - 2;

    tmp_coord.x = start.x;
    tmp_coord.y = start.y;

    int choosen = 0;
    bfs(start, end, size);

    do {
        fillMap(map, size);
        map[start.x][start.y] = '@';
        map[end.x][end.y] = '&';

        printMap(map, size);
        printInfo();

        button = getch();
        if (button == 'w') tmp_coord.y--;
        if (button == 's') tmp_coord.y++;
        if (button == 'a') tmp_coord.x--;
        if (button == 'd') tmp_coord.x++;

        if (button == '>') {
            tmp_coord.x = end.x;
            tmp_coord.y = end.y;
            choosen = 1;
        } else if (button == '<') {
            tmp_coord.x = start.x;
            tmp_coord.y = start.y;
            choosen = 0;
        }

        if (!choosen) {
            start.x = tmp_coord.x;
            start.y = tmp_coord.y;
        } else if (choosen) {
            end.x = tmp_coord.x;
            end.y = tmp_coord.y;
        }

        system("cls");
    } while (button != 'e');

    map = deleteMap(map, size);
    return 0;
}
