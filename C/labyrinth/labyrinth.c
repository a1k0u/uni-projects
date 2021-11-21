#include <stdio.h>
#include <stdlib.h>
#include <conio.h>

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

    int start_x = 1, start_y = 1;
    int end_x = size - 2, end_y = size - 2;

    int x = start_x, y = start_y;
    int choosen = 0;

    do {
        fillMap(map, size);
        map[start_x][start_y] = '@';
        map[end_x][end_y] = '&';

        printMap(map, size);
        printInfo();

        button = getch();
        if (button == 'w') y--;
        if (button == 's') y++;
        if (button == 'a') x--;
        if (button == 'd') x++;

        if (button == '>') {
            x = end_x;
            y = end_y;
            choosen = 1;
        } else if (button == '<') {
            x = start_x;
            y = start_y;
            choosen = 0;
        }

        if (!choosen) {
            start_x = x;
            start_y = y;
        } else if (choosen) {
            end_x = x;
            end_y = y;
        }

        system("cls");
    } while (button != 'e');

    map = deleteMap(map, size);
    return 0;
}
