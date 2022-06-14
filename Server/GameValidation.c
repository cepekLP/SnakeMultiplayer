#include "GameValidation.h"

void collision_check(player_state_t* player, player_state_t players[], game_state_t* game_state)
{

    apple_collision(player, game_state);
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
        //printf("%lld %lld", player, &players[i]);
        if((players[i].flags & IS_ALIVE) == IS_ALIVE && player != &players[i])
        {
            for(int j = 0 ;j < players[i].length; j++)
            {
                if( do_overlap((point_t){player->positionX[0], player->positionY[0]}, (point_t){players[i].positionX[j], players[i].positionY[j]}) == 1)
                {
                    return 1;
                }
            }
        }
    }

    return 0;
}

void apple_collision(player_state_t* player, game_state_t* game_state)
{
    // def apple_collision(self, apple_position):
	// 	self.body.insert(0, Point(self.position.x, self.position.y))
	// 	if (apple_position.x <= self.position.x < apple_position.x + APPLE_SIZE) and\
	// 		(apple_position.y <= self.position.y < apple_position.y + APPLE_SIZE):
	// 		return True
	// 	else:
	// 		self.body.pop()
	// 	return False

    if((game_state->apple_position.x <= player->positionX[0]) && (player->positionX[0] < game_state->apple_position.x + APPLE_SIZE) &&
        (game_state->apple_position.y <= player->positionY[0]) && (player->positionY[0] < game_state->apple_position.y + APPLE_SIZE))
    {
        player->positionX[player->length] = player->positionX[player->length-1];
        player->positionY[player->length] = player->positionY[player->length-1];
        player->length += 1;
        player->points += 10;
        spawn_apple(game_state);
    }
}

void spawn_apple(game_state_t* game_state)
{
    // for snake in self.snakes:
	// 			if snake.apple_collision(self.apple_position):
	// 				self.apple_spawned = False

	// 		if not self.apple_spawned:
	// 			self.apple_position = Point(
	// 				random.randrange(0, WINDOW_X - APPLE_SIZE, BLOCK_SIZE),
	// 				random.randrange(0, WINDOW_Y - APPLE_SIZE, BLOCK_SIZE))
	// 		self.apple_spawned = True

    game_state->apple_position.x = (rand() % (MAP_WIDTH / SNAKE_BLOCK_SIZE - APPLE_SIZE / SNAKE_BLOCK_SIZE + 1) * SNAKE_BLOCK_SIZE);
    game_state->apple_position.y = (rand() % (MAP_HEIGHT / SNAKE_BLOCK_SIZE - APPLE_SIZE / SNAKE_BLOCK_SIZE + 1) * SNAKE_BLOCK_SIZE);
}