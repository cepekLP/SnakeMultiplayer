#include <stdio.h>
#include <stdlib.h>
#include "Message.h"

char* point_serialize(point_t in_point)
{
    static char result[9];
    sprintf(result, "%04x%04x",in_point.x, in_point.y);
    return result;
}

char* serialize_player_data()
{
    char result[2000];
    int timestamp = 213742069;
    u_int8_t direction = 1;
    u_int8_t length = 255;
    sprintf(result, "%010x%01x%02x\n", timestamp, direction, length);
    for(int i=0; i < MAX_LENGTH; i++)
    {
        point_t point= {2,2};
        char* ret = point_serialize(point);
        printf("%s\n", ret);
    }
    
    printf("%s", result);
    return result;
}

player_data_t deserialize_player_data(char* in_data)
{
    player_data_t player_data;
    int timestamp = 0;
    u_int8_t direction = 0;
    u_int8_t length = 0;

    sscanf(in_data,"%010x%01x%02x", &player_data.timestamp, &player_data.direction, &player_data.length);

    printf("%d %d %d", player_data.timestamp, direction, length);
    return player_data;
}

int main()
{
    char* data = serialize_player_data();
    deserialize_player_data(data);
}