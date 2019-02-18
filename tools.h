#ifndef DEF_TOOLS
#define DEF_TOOLS

#define GRAVITY 0.4
#define LARGEUR_FENETRE 640
#define HAUTEUR_FENETRE 480
#define LARGEUR_TUYAU 100
#define HAUTEUR_TROU 150
#define TROU_CENTRE_YMIN 100
#define TROU_CENTRE_YMAX 380

typedef struct Boule Boule;
struct Boule {
    SDL_Surface *image;
    float x;
    float vx;
    float y;
    float vy;
    int height;
};

typedef struct Tuyau Tuyau;
struct Tuyau {
    float x;
    float y;
};

int min(int v1, int v2);
int max(int v1, int v2);

#endif
