#pragma once

#include "Statics.h"


typedef enum {
    UP,
    DOWN,
    LEFT,
    RIGHT
}direction_t;

typedef struct{
	uint16_t x;
	uint16_t y;
}point_t;

/*  -----------flags-----------  */
//  15 ......... 0
//  0 - acceleration
//  1 - isAlive
//  2

typedef struct {
    uint32_t timestamp;
    point_t position[MAX_SNAKE_LENGTH];
    direction_t direction;
    uint8_t length;
    uint16_t points;
    uint16_t flags;
}player_data_t;

typedef struct{
	unsigned int player_number;
    int active_players;
    player_data_t* players;

}game_state_t;


