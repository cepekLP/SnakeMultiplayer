#pragma once

#include "GameState.h"

void collision_check(player_data_t* player, player_data_t players[], game_state_t* game_state);

int wall_hit(player_data_t* player);

int do_overlap(point_t l1, point_t l2, point_t r1, point_t r2);