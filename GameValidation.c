#include "GameValidation.h"

void collision_check(player_data_t* player, player_data_t players[], game_state_t* game_state)
{
    if(wall_hit(player) == 1)
    {
        player->flags &= ~IS_ALIVE; 
    }
    else
    {
        for(int i =0;i < game_state->player_number; i++)
        {
            if(players[i].flags & IS_ALIVE == IS_ALIVE)
            {
                for(int j = 0 ;j < players[i].length; j++)
                {
                    if( do_overlap( players[i].position[j], 
                                    (point_t) {players[i].position[j].x +SNAKE_BLOCK_SIZE, players[i].position[j].y +SNAKE_BLOCK_SIZE},
                                    player->position[0],
                                    (point_t) {player->position[0].x +SNAKE_BLOCK_SIZE, player->position[0].y +SNAKE_BLOCK_SIZE} ) == 1)
                    {
                        player->flags &= ~IS_ALIVE; 
                    }
                }
*-
            }
        }
    }
}

int wall_hit(player_data_t* player)
{
    if( 
        player->position[0].x + SNAKE_BLOCK_SIZE <= MAP_WIDHT &&
        player->position[0].x >= 0 && 
        player->position[0].y + SNAKE_BLOCK_SIZE <= MAP_HEIGHT &&
        player->position[0].y >= 0 
        )
    {
        return 0;
    }
    else {
        return 1;
    }
}

int do_overlap(point_t l1, point_t l2, point_t r1, point_t r2)
{
    // If one rectangle is on left side of other
    if (l1.x > r2.x || l2.x > r1.x)
    {
           return 0;
    }

    // If one rectangle is above other
    if (r1.y > l2.y || r2.y > l1.y)
    {
        return 0;
    }

    return 1;
}