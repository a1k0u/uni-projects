//#pragma once

#ifndef POINT_H
#define POINT_H
typedef struct Point {
    int x, y;
    int num;
} POINT;

typedef struct Queue {
    POINT* memory;
    int pointer;
    int q_size;
} POINTS_QUEUE;

void push(POINTS_QUEUE* qu, const POINT point) {
    if (qu->pointer == qu->q_size) {
        qu->q_size *= 2;
        qu->memory = (POINT*)realloc(qu->memory, qu->q_size * sizeof(POINT));
    }
    qu->memory[qu->pointer++] = point;
}

POINT pop(POINTS_QUEUE* qu) {
    if (qu->pointer != 0) {
        POINT point = qu->memory[0];
        for (int i = 0; i < qu->q_size - 1; ++i)
            qu->memory[i] = qu->memory[i+1];
        qu->pointer--;

        return point;
    }
}

#endif
