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

    int nombreTuyaux = 3;
    Tuyau tuyaux[3];
    tuyaux[0].x = 700;
    tuyaux[0].y = 200;
    tuyaux[1].x = 1000;
    tuyaux[1].y = 300;
    tuyaux[2].x = 1300;
    tuyaux[2].y = 250;

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
        updateValues(boule, tuyaux, nombreTuyaux);
        if (death(ecran, boule)) {
            continuer = 0;
        }
        draw(ecran, background, boule, tuyaux, nombreTuyaux);
        SDL_Delay(20);
    }
}

int death(SDL_Surface *ecran, Boule *boule) {
    return (boule->y > (ecran->h - boule->height)) ||
            boule->y < 0;
}

void updateValues(Boule *boule, Tuyau tuyaux[], int nombreTuyaux) {
    boule->vy += GRAVITY;
    boule->y += boule->vy;
    for (int i = 0; i < nombreTuyaux; i++) {
        tuyaux[i].x -= boule->vx;
    }
}
