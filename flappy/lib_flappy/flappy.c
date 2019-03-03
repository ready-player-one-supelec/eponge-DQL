#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>

#define _LIB_FLAPPY
#include "tools.h"
#include "flappy.h"
#include "game.h"

unsigned char* init_flappy(int display) {
    SDL_Init(SDL_INIT_VIDEO);
    TTF_Init();
    initFont(&game.font);
    game.ecran = SDL_SetVideoMode(LARGEUR_FENETRE, HAUTEUR_FENETRE, 32, SDL_HWSURFACE | SDL_DOUBLEBUF);
    SDL_WM_SetCaption("Flappy Bird", NULL);

    game.display = display;

    game.background = SDL_CreateRGBSurface(SDL_HWSURFACE, game.ecran->w, game.ecran->h, 32, 0, 0, 0, 0);
    SDL_FillRect(game.background, NULL, SDL_MapRGB(game.ecran->format, 135, 206, 235));
    game.boule.image = IMG_Load("Images/boule.png");
    game.boule.height = game.boule.image->w;
    reset_flappy();

    unsigned char *pointeur = NULL;
    pointeur = (unsigned char *)malloc(X_SIZE * Y_SIZE);
    // treatingImage(ecran, image);
    printf("pointeur = %ld\n", (long int) pointeur);
    return pointeur;
}

void initBoule(Boule *boule) {
    boule->y = 70;
    boule->vy = 0;
    boule->x = BOULE_XAXIS;
    boule->vx = 3;
}

void reset_flappy(void) {
    initBoule(&game.boule);
    game.tuyaux[0].x = 700 ;
    game.tuyaux[0].y = randCenter();
    game.score = 0;

    for (int i = 1; i < NOMBRE_TUYAUX ; i++) {
        nextTuyau(&game.tuyaux[i], &game.tuyaux[(i-1) % NOMBRE_TUYAUX]);
    }
}

void changeDisplay(int display) {
    game.display = display;
}

void exit_flappy(void) {
    SDL_FreeSurface(game.background);
    SDL_FreeSurface(game.boule.image);
    TTF_CloseFont(game.font.font);
    TTF_Quit();
}

void initFont(Font *font) {
    font->font = NULL;
    font->font = TTF_OpenFont("Sugar Addiction - TTF.ttf", 30);
    font->color.r = 255;
    font->color.g = 0;
    font->color.b = 0;
    font->textSurface = NULL;
}

void getSize(int *x_size, int *y_size) {
    *x_size = X_SIZE;
    *y_size = Y_SIZE;
}
