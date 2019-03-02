#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>

#include "tools.h"
#include "game.h"

void initFont(Font *font);
void init_flappy(void);
void exit_flappy(void);
extern Game game;

int main (int argc, char *argv[]) {

    init_flappy();
    run_flappy();
    exit_flappy();
    return EXIT_SUCCESS;
}

void init_flappy(void) {
    SDL_Init(SDL_INIT_VIDEO);
    TTF_Init();
    initFont(&game.font);
    game.ecran = SDL_SetVideoMode(LARGEUR_FENETRE, HAUTEUR_FENETRE, 32, SDL_HWSURFACE | SDL_DOUBLEBUF);
    SDL_WM_SetCaption("Flappy Bird", NULL);


    game.background = SDL_CreateRGBSurface(SDL_HWSURFACE, game.ecran->w, game.ecran->h, 32, 0, 0, 0, 0);
    SDL_FillRect(game.background, NULL, SDL_MapRGB(game.ecran->format, 135, 206, 235));
    game.boule.image = IMG_Load("Images/boule.png");
    game.boule.height = game.boule.image->w;
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
