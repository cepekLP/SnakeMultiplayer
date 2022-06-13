#pragma once
#include "Statics.h"
#define GAME_STRUCT_SIZE 2 * 2 * MAX_SNAKE_LENGTH + 4 + 2 + 2 + 2 + 2

#define PING_STRUCT_SIZE 8

typedef struct __attribute__((__packed__)){
    float x;
    float y;
    char message[256];
}Message;

typedef struct __attribute__((__packed__)){
    int ping;
}ping_crc_t;

/*  -----------flags-----------  */
//  15 ......... 0
//  0 - acceleration
//  1 - isAlive
//  2

typedef struct __attribute__((__packed__)){
    u_int32_t timestamp;
    u_int16_t length;
    u_int16_t direction;
    u_int16_t points;
    u_int16_t flags;
    u_int16_t positionX[MAX_SNAKE_LENGTH];
    u_int16_t positionY[MAX_SNAKE_LENGTH];   
}player_state_t;
