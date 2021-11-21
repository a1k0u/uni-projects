#include <stdio.h>
#include <stdlib.h>

char** initMap(char** map, int SIZE) {
    map = (char**)calloc(SIZE, sizeof(char*));
    for (int i = 0; i < SIZE; ++i)
        map[i] = (char*)calloc(SIZE, sizeof(char));
    return map;
}

void fillMap(char** map, int size) {
    for (int y = 0; y < size; ++y)
        for (int x = 0; x < size; ++x)
            if ((y == 0) || (x == 0) ||
                    (y == size-1) || (x == size-1))
                map[x][y] = '#';
            else
                map[x][y] = '*';

}

void printMap(char** map, int size) {
    for (int y = 0; y < size; ++y) {
        for (int x = 0; x < size; ++x)
            printf("%2c", map[x][y]);
        printf("\n");
    }
}

int main() {
    int size = 20;
    char** map = initMap(map, size);
    fillMap(map, size);
    printMap(map, size);
    return 0;
}
