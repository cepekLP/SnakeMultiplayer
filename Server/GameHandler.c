#include "GameHandler.h"

void init_player(game_state_t* game_state)
{
    game_state->players[game_state->active_players].length = 20;
    game_state->players[game_state->active_players].points = 0;
    game_state->players[game_state->active_players].flags = 0;
// losowanie startu
    

    game_state->active_players++;
}

void start_game_counter(game_state_t* game_state)
{
    for(int i =15; i>0; i--)
    {
        game_state->start_counter = i;
        sleep(1000);
    }
    game_state->start_counter = 0;
}

void start_game()
{

}




