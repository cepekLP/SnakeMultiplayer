#define MAX_LENGTH 20

typedef struct __attribute__((__packed__)){
    float x;
    float y;
    char message[256];
}Message;

typedef struct __attribute__((__packed__)){
    int ping;
}ping_crc;

typedef struct{
	u_int16_t x;
	u_int16_t y;
}point_t;

typedef enum {
    UP,
    DOWN,
    LEFT,
    RIGHT
}direction_t;

typedef struct {
    int timestamp;
    point_t position[MAX_LENGTH];
    direction_t direction;
    int length;
}player_data_t;

