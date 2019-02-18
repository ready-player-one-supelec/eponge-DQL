#ifndef DEF_FLAPPY
#define DEF_FLAPPY

typedef struct Boule Boule;
struct Boule {
    SDL_Surface *image;
    float x;
    float vx;
    float y;
    float vy;
    int height;
};

#endif
