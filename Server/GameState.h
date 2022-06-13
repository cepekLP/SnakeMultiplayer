#pragma once

#include "Statics.h"
#include "Message.h"


typedef enum {
    UP,
    LEFT,
    DOWN,
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
/*
typedef struct {
    uint32_t timestamp;
    point_t position[MAX_SNAKE_LENGTH];
    direction_t direction;
    uint8_t length;
    uint16_t points;
    uint16_t flags;
}player_data_t;*/

typedef struct{
	unsigned int player_number;
    u_int16_t active_players;
    int start_counter;
    player_state_t players[MAX_PLAYER_NUMBER];

}game_state_t;


