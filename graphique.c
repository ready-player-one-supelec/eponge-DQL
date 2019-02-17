#include <stdio.h>
#include <stdlib.h>
#include <SDL/SDL.h>
#include <SDL/SDL_image.h>

#include "flappy.h"
#include "graphique.h"

void draw(SDL_Surface *ecran, SDL_Surface *background, Boule *boule) {
    SDL_Rect position;
    position.x = 0;
    position.y = 0;
    SDL_BlitSurface(background, NULL, ecran, &position);

    position.x = 100;
    position.y = boule->y;
    SDL_BlitSurface(boule->image, NULL, ecran, &position);

    SDL_Flip(ecran);
}
