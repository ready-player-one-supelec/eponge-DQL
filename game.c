#include <stdio.h>
#include <stdlib.h>

#include <SDL/SDL.h>
#include <SDL/SDL_image.h>

#include "flappy.h"
#include "game.h"
#include "graphique.h"

void game(SDL_Surface *ecran, SDL_Surface *background, Boule *boule) {
    int continuer = 1;
    SDL_Event event;

    while (continuer) {
        SDL_PollEvent(&event);
        switch (event.type) {
            case SDL_QUIT :
                continuer = 0;
                break;
            case SDL_KEYDOWN :
                switch (event.key.keysym.sym) {
                    case SDLK_ESCAPE :
                        continuer = 0;
                        break;
                    case SDLK_SPACE :
                        boule->vy = -7.5;
                        break;
                }
                break;
        }
        updateValues(boule);
        if (death(ecran, boule)) {
            continuer = 0;
        }
        draw(ecran, background, boule);
        SDL_Delay(20);
    }
}

int death(SDL_Surface *ecran, Boule *boule) {
    return (boule->y > (ecran->h - boule->height)) ||
            boule->y < 0;
}

void updateValues(Boule *boule) {
    boule->vy += GRAVITY;
    boule->y += boule->vy;
    boule->x += boule->vx;
}
