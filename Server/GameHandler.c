#include "GameHandler.h"

void init_player(game_state_t* game_state)
{
    game_state->players[game_state->active_players].length = 20;
    game_state->players[game_state->active_players].points = 0;
    game_state->players[game_state->active_players].flags = 0;
// losowanie startu
    uint16_t rand_pos_x = (rand() % (MAP_WIDTH / SNAKE_BLOCK_SIZE - 10)) * SNAKE_BLOCK_SIZE + 5 * SNAKE_BLOCK_SIZE;
    uint16_t rand_pos_y = (rand() % (MAP_HEIGHT / SNAKE_BLOCK_SIZE - 10)) * SNAKE_BLOCK_SIZE + 5 * SNAKE_BLOCK_SIZE;
    direction_t rand_dir = rand() % 4;
    

    game_state->active_players++;
}

void start_game_counter(game_state_t* game_state, sem_t* mutex)
{
    for(int i =15; i>0; i--)
    {
        sem_wait(mutex);
        game_state->start_counter = i;
        sem_post(mutex);
        sleep(1000);
    }
    sem_wait(mutex);
    game_state->start_counter = 0;
    sem_post(mutex);
}

void game_handler(game_handler_struct_t* game_handler_struct)
{
    printf("GameHandler started...\n");
    game_state_t* gs = game_handler_struct->game_state;
    sem_t* gs_mutex = game_handler_struct->mutex;
    while(1){
        sem_wait(gs_mutex);
        while(gs->active_players < gs->player_number/2)
        {
            sem_post(gs_mutex);
            sleep(250);
            sem_wait(gs_mutex);
        }
              for(int i=0;i < gs->active_players; i++)
        {
            gs->players[i].flags |= IS_GOING_TO_START;
        }  
        sem_post(gs_mutex);
        start_game_counter(gs, gs_mutex);


        sem_wait(gs_mutex);
        int player_alive = gs->active_players;
        
        for(int i=0;i < gs->active_players; i++)
        {
            gs->players[i].flags |= IS_STARTED;
        }
        sem_post(gs_mutex);

        while(player_alive>0){
            sleep(100);
            sem_wait(gs_mutex);
            player_alive = 0;
            
            for(int i=0;i < gs->active_players; i++)
            {
                if((gs->players[i].flags && IS_ALIVE)==IS_ALIVE)
                {
                    player_alive++;
                };
            }
            sem_post(gs_mutex);
        }

    }
}




