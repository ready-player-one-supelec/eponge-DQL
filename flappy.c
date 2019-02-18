#include <stdio.h>
#include <stdlib.h>

#include <SDL/SDL.h>
#include <SDL/SDL_image.h>

#include "flappy.h"
#include "graphique.h"
#include "game.h"

int main (int argc, char *argv[]) {

    SDL_Init(SDL_INIT_VIDEO);
    SDL_Surface *ecran = NULL;
    ecran = SDL_SetVideoMode(640, 480, 32, SDL_HWSURFACE | SDL_DOUBLEBUF);
    SDL_WM_SetCaption("Flappy Bird", NULL);


    SDL_Surface *background = SDL_CreateRGBSurface(SDL_HWSURFACE, ecran->w, ecran->h, 32, 0, 0, 0, 0);
    SDL_FillRect(background, NULL, SDL_MapRGB(ecran->format, 135, 206, 235));
    Boule boule;
    boule.image = IMG_Load("Images/boule.png");
    boule.y = 0;
    boule.vy = 0;
    boule.x = 100;
    boule.vx = 2;
    boule.height = boule.image->w;

    game(ecran, background, &boule);

    return EXIT_SUCCESS;
}
