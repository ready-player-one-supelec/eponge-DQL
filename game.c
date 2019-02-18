#include <stdio.h>
#include <stdlib.h>

#include <SDL/SDL.h>
#include <SDL/SDL_image.h>

#include "tools.h"
#include "game.h"
#include "graphique.h"

void game(SDL_Surface *ecran, SDL_Surface *background, Boule *boule) {
    int continuer = 1;
    SDL_Event event;

    Tuyau tuyau;
    tuyau.x = 700;
    tuyau.y = 200;

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
        updateValues(boule, &tuyau);
        if (death(ecran, boule)) {
            continuer = 0;
        }
        draw(ecran, background, boule, &tuyau);
        SDL_Delay(20);
    }
}

int death(SDL_Surface *ecran, Boule *boule) {
    return (boule->y > (ecran->h - boule->height)) ||
            boule->y < 0;
}

void updateValues(Boule *boule, Tuyau *tuyau) {
    boule->vy += GRAVITY;
    boule->y += boule->vy;
    tuyau->x -= boule->vx;
}
