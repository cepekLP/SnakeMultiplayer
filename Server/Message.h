#ifndef MESSAGE_H
#define MESSAGE_H


#include <stdint.h>
#include "Statics.h"
#define PLAYER_STRUCT_SIZE 2 * 2 * MAX_SNAKE_LENGTH + 4 + 2 + 2 + 2 + 2

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
    uint32_t timestamp;
    uint16_t length;
    uint16_t direction;
    uint16_t points;
    uint16_t flags;
    int16_t positionX[MAX_SNAKE_LENGTH];
    int16_t positionY[MAX_SNAKE_LENGTH];   
}player_state_t;

#endif