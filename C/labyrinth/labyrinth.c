#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <conio.h>

#define QUEUE_SIZE 1000

typedef struct cd {
    int num;
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

void bfs (char** map, COORD start, COORD end, int size) {
    COORD visited_points[5000];
    int visited_points_pointer = 0;

    QUEUE next_points;
    next_points.pointer = 0;
    start.num = 0;

    push(&next_points, start);
    while(next_points.pointer != 0) {
        COORD cur_coord = pop(&next_points);

        if (cur_coord.x == end.x && cur_coord.y == end.y) {
            visited_points[visited_points_pointer++] = cur_coord;
            break;
        }

        COORD steped_point[4];
        if (cur_coord.x + 1 < size - 1 && map[cur_coord.x + 1][cur_coord.y] != '#') {
            steped_point[0].x = cur_coord.x + 1;
            steped_point[0].y = cur_coord.y;
            steped_point[0].num = cur_coord.num + 1;
        } else {
            steped_point[0].x = -1;
        }
        if (cur_coord.y + 1 < size - 1 && map[cur_coord.x][cur_coord.y + 1] != '#') {
            steped_point[1].x = cur_coord.x;
            steped_point[1].y = cur_coord.y + 1;
            steped_point[1].num = cur_coord.num + 1;
        } else {
            steped_point[1].x = -1;
        }
        if (cur_coord.x - 1 > 1 && map[cur_coord.x - 1][cur_coord.y] != '#') {
            steped_point[2].x = cur_coord.x - 1;
            steped_point[2].y = cur_coord.y;
            steped_point[2].num = cur_coord.num + 1;
        } else {
            steped_point[2].x = -1;
        }
        if (cur_coord.y - 1 > 1 && map[cur_coord.x][cur_coord.y - 1] != '#') {
            steped_point[3].x = cur_coord.x;
            steped_point[3].y = cur_coord.y - 1;
            steped_point[3].num = cur_coord.num + 1;
        } else {
            steped_point[3].x = -1;
        }

        for (int i = 0; i < 4; i++) {
            int fg = 0;
            if (!(steped_point[i].x == -1)) {
                for (int j = 0; j < next_points.pointer; j++) {
                    if (next_points.memory[j].x == steped_point[i].x && next_points.memory[j].y == steped_point[i].y) {
                        fg = 1;
                        break;
                    }
                }
                if (!fg) {
                    push(&next_points, steped_point[i]);
                }
            }
        }

        int flag = 0;
        for (int i = 0; i < visited_points_pointer; i++) {
            if (visited_points[i].x == cur_coord.x && visited_points[i].y == cur_coord.y) {
                flag = 1;
                break;
            }
        }

        if (!flag) {
            visited_points[visited_points_pointer] = cur_coord;
            visited_points_pointer++;
        }
    }

    int index_end = 0;
    COORD xy_draw;
    for (int i = 0; i < visited_points_pointer; i++) {
        if (visited_points[i].x == end.x && visited_points[i].y == end.y) {
            index_end = visited_points[i].num;
            xy_draw.x = visited_points[i].x;
            xy_draw.y = visited_points[i].y;
            break;
        }
    }

    while (index_end >= 0) {
        for (int i = 0; i < visited_points_pointer; i++) {
            if (((abs(visited_points[i].x - xy_draw.x) == 1 && abs(visited_points[i].y - xy_draw.y) == 0)
                    || (abs(visited_points[i].x - xy_draw.x) == 0 && abs(visited_points[i].y - xy_draw.y) == 1))
                    && visited_points[i].num == index_end-1) {
                xy_draw.x = visited_points[i].x;
                xy_draw.y = visited_points[i].y;
                map[xy_draw.x][xy_draw.y] = '*';
            }
        }
        index_end--;
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
    int size = 10;

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

    do {
        fillMap(map, size);
        bfs(map, start, end, size);
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
