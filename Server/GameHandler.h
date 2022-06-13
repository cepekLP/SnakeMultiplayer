#ifndef GAMEHANDLER_H
#define GAMEHANDLER_H

#include "GameState.h"
#include <semaphore.h>

typedef struct{
    game_state_t* game_state;
    sem_t* mutex;
}game_handler_struct_t;

void init_player(game_state_t* game_state);

void start_game_counter(game_state_t* game_state, sem_t* mutex);

void game_handler(game_handler_struct_t* game_handler_struct);

void end_game();

#endif