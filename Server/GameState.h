#ifndef GAMESTATE_H
#define GAMESTATE_H

#include <stdint.h>
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

typedef struct{
	unsigned int player_number;
    uint16_t active_players;
    int start_counter;
    player_state_t players[MAX_PLAYER_NUMBER];
    point_t apple_position;
}game_state_t;


#endif