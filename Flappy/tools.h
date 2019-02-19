#ifndef DEF_TOOLS
#define DEF_TOOLS

#define GRAVITY 0.4
#define LARGEUR_FENETRE 720//1080 // Il faut de préférence une largeur supérieure à 720
#define HAUTEUR_FENETRE 440//720 // Il faut de préférence une hauteur supérieure à 440
#define LARGEUR_TUYAU 100
#define HAUTEUR_TROU 150
#define TROU_CENTRE_YMIN 100
#define TROU_CENTRE_YMAX (HAUTEUR_FENETRE - (HAUTEUR_TROU/2) - 100)
#define PAS_ENTRE_TUYAU 300
#define TOLERANCE 2 //nombre de pixels de tolérance pour les collisions
#define ESPACE_INTER_TUYAU (PAS_ENTRE_TUYAU+LARGEUR_TUYAU)
#define NOMBRE_TUYAUX (2+(LARGEUR_FENETRE/ESPACE_INTER_TUYAU))
#define BOULE_XAXIS 100;

#define SIZE_READING_BUFFER_PIPE 2 //only reading an integer
#define SIZE_WRITING_BUFFER_PIPE 3 //will probably be a very large table (thousands of values)

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

typedef struct Font Font;
struct Font {
    SDL_Color color;
    TTF_Font *font;
    SDL_Surface *textSurface;
    char text[31];
};

typedef struct Pipes Pipes;
struct Pipes {
    int imagesPipe;
    int actionsPipe;
    char readingBuffer[SIZE_READING_BUFFER_PIPE];
    char writingBuffer[SIZE_WRITING_BUFFER_PIPE];
};

int min(int v1, int v2);
int max(int v1, int v2);

#endif
