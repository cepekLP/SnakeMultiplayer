#include "GameValidation.h"

void collision_check(player_state_t* player, player_state_t players[], game_state_t* game_state)
{
    if((player->flags & IS_ALIVE) == IS_ALIVE)
    {
        if(wall_hit(player) == 1)
        {
            player->flags &= ~IS_ALIVE; 
        }
        else if(self_collision(player) == 1)
        {
            player->flags &= ~IS_ALIVE; 
        }
        else if(others_players_hit(player, players, game_state->player_number) == 1)
        {
            player->flags &= ~IS_ALIVE;
        }
    }
    
}

int wall_hit(player_state_t* player)
{
    if( 
        player->positionX[0] + SNAKE_BLOCK_SIZE <= MAP_WIDTH &&
        player->positionX[0] >= 0 && 
        player->positionY[0] + SNAKE_BLOCK_SIZE <= MAP_HEIGHT &&
        player->positionY[0] >= 0 
        )
    {
        return 0;
    }
    else {
        return 1;
    }
}

int self_collision(player_state_t* player)
{
    for(int i = 1; i < player->length; i++)
    {
        if(do_overlap((point_t){player->positionX[0], player->positionY[0]}, (point_t){player->positionX[i], player->positionY[i]}))
        {
            return 1;
        }
    }

    return 0;
}

int do_overlap(point_t point1, point_t point2)
{
    if(point1.x == point2.x && point1.y == point2.y)
    {
        return 1;
    }

    return 0;
}

int others_players_hit(player_state_t* player, player_state_t players[], int players_nr)
{
    for(int i = 0; i < players_nr; i++)
    {
        if((players[i].flags & IS_ALIVE) == IS_ALIVE && player != &players[i])
        {
            for(int j = 0 ;j < players[i].length; j++)
            {
                if( do_overlap((point_t){player->positionX[0], player->positionY[0]}, (point_t){player->positionX[i], player->positionY[i]}) == 1)
                {
                    return 1;
                }
            }
        }
    }

    return 0;
}