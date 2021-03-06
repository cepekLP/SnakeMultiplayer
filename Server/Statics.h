#ifndef STATICS_H
#define STATICS_H


#define MAP_WIDTH 800
#define MAP_HEIGHT 600
#define SPAWN_MARGIN 15
#define APPLE_SIZE 15

#define START_SNAKE_LENGTH 20
#define MAX_SNAKE_LENGTH 50

#define SNAKE_BLOCK_SIZE 5
#define PLAYER_NUMBER 3

#define MAX_PLAYER_NUMBER 6
/*  -----------flags-----------  */

#define ACCELERATION        0x0001
#define IS_ALIVE            0x0002
#define IS_FINISHED         0x0004
#define IS_STARTED          0x0008
#define IS_GOING_TO_START   0x000C
#define IS_ENDED            0x0010

#endif