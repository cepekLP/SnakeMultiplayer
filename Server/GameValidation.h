#pragma once

#include "GameState.h"
#include "Message.h"

void collision_check(player_state_t* player, player_state_t players[], game_state_t* game_state);

int wall_hit(player_state_t* player);

int self_collision(player_state_t* player);

int do_overlap(point_t point1, point_t point2);

int others_players_hit(player_state_t* player, player_state_t players[], int players_nr);