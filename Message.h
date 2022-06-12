#include "GameState.h"


typedef struct __attribute__((__packed__)){
    float x;
    float y;
    char message[256];
}Message;

typedef struct __attribute__((__packed__)){
    int ping;
}ping_crc;

