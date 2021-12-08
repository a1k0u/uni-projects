#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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

void bfs (char** map, COORD st_point, COORD end_point, int size) {
    COORD visited_points[5000];
    COORD steped_point;
    QUEUE queue_points;
    queue_points.pointer = 0;

    int visited_points_pointer = 0;
    int flag = 0;

    st_point.num = 0;

    push(&queue_points, st_point);
    while(queue_points.pointer != 0) {
        COORD cur_coord = pop(&queue_points);

        flag = 0;
        for (int i = 0; i < visited_points_pointer; i++)
            if (visited_points[i].x == cur_coord.x &&
                        visited_points[i].y == cur_coord.y) {
                flag = 1;
                break;
            }

        if (!flag)
            visited_points[visited_points_pointer++] = cur_coord;

        if (cur_coord.x == end_point.x && cur_coord.y == end_point.y)
            break;

        int directions[8][2] = {1, 0, -1, 0, 0, 1, 0, -1, 1, 1, -1, -1, 1, -1, -1, 1};
        for (int i = 0; i < 8; i++) {
            flag = 0;

            steped_point.x = cur_coord.x + directions[i][0];
            steped_point.y = cur_coord.y + directions[i][1];
            steped_point.num = cur_coord.num + 1;
            if (map[steped_point.y][steped_point.x] != '#') {
                for (int j = 0; j < queue_points.pointer; j++) {
                    if (queue_points.memory[j].x == steped_point.x &&
                                queue_points.memory[j].y == steped_point.y) {
                        flag = 1;
                        break;
                    }
                }
                if (!flag)
                    push(&queue_points, steped_point);
            }
        }
    }

    int index_end = 0;
    COORD xy_draw;
    for (int i = 0; i < visited_points_pointer; i++) {
        if (visited_points[i].x == end_point.x && visited_points[i].y == end_point.y) {
            index_end = visited_points[i].num;
            xy_draw.x = visited_points[i].x;
            xy_draw.y = visited_points[i].y;
            break;
        }
    }

    while (index_end >= 0) {
        for (int i = 0; i < visited_points_pointer; i++) {
            if (((abs(visited_points[i].x - xy_draw.x) == 1 && abs(visited_points[i].y - xy_draw.y) == 0)
                    || (abs(visited_points[i].x - xy_draw.x) == 0 && abs(visited_points[i].y - xy_draw.y) == 1)
                    || (abs(visited_points[i].x - xy_draw.x) == 1 && abs(visited_points[i].y - xy_draw.y) == 1))
                    && visited_points[i].num == index_end-1) {
                xy_draw.x = visited_points[i].x;
                xy_draw.y = visited_points[i].y;
                map[xy_draw.y][xy_draw.x] = '`';
                break;
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
    FILE* f_read = fopen("input.txt", "r");

    int map_height = 0, map_width;

    char buffer[100] = {0};
    while (fgets(buffer, 100, f_read)) {
        map_width = strlen(buffer);
        for (int i = 0; i < map_width; ++i)
            map[map_height][i] = buffer[i];
        map_height++;
    }

    fclose(f_read);
}

void printMap(char** map, int size) {
    for (int y = 0; y < size; ++y)
        for (int x = 0; x < size; ++x)
            printf("%2c", map[y][x]);
}

void printInfo() {
    printf("\n\nUse UP-2, DOWN-4, LEFT-1, RIGHT-3 to move START POINT.");
    printf("\nUse UP-7, DOWN-9, LEFT-6, RIGHT-8 to move END POINT.");
    printf("\n\n");
}

int main() {
    int size = 23;

    char** map = initMap(map, size);
    char button;

    COORD st_point, end_point, tmp_coord;
    st_point.x = 1;
    st_point.y = 1;

    end_point.x = 2;
    end_point.y = 2;

    tmp_coord.x = st_point.x;
    tmp_coord.y = st_point.y;

    int choosen = 0;

    do {
        fillMap(map, size);
        bfs(map, st_point, end_point, size);
        map[st_point.y][st_point.x] = 'S';
        map[end_point.y][end_point.x] = 'F';

        printMap(map, size);
        printInfo();

        button = getch();
        if (map[st_point.y-1][st_point.x] != '#' && button == '2') st_point.y--;
        if (map[st_point.y+1][st_point.x] != '#' && button == '4') st_point.y++;
        if (map[st_point.y][st_point.x-1] != '#' && button == '1') st_point.x--;
        if (map[st_point.y][st_point.x+1] != '#' && button == '3') st_point.x++;

        if (map[end_point.y-1][end_point.x] != '#' && button == '7') end_point.y--;
        if (map[end_point.y+1][end_point.x] != '#' && button == '9') end_point.y++;
        if (map[end_point.y][end_point.x-1] != '#' && button == '6') end_point.x--;
        if (map[end_point.y][end_point.x+1] != '#' && button == '8') end_point.x++;

        system("cls");
    } while (button != 'e');

    map = deleteMap(map, size);
    return 0;
}
