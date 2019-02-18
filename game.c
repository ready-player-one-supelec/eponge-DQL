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
    tuyaux[0].y = randCenter();
    for (int i = 1; i < nombreTuyaux ; i++) {
        nextTuyau(&tuyaux[i], &tuyaux[(i-1) % nombreTuyaux]);
    }

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
        for (int i = 0; i < nombreTuyaux; i++) {
            if (tuyaux[i].x < -LARGEUR_TUYAU) {
                nextTuyau(&tuyaux[i], &tuyaux[(nombreTuyaux + i-1) % nombreTuyaux]);
            }
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

int randCenter() {
    return random() % (TROU_CENTRE_YMAX - TROU_CENTRE_YMIN) + TROU_CENTRE_YMIN;
}

void nextTuyau(Tuyau *tuyau, Tuyau *previousTuyau) {
    tuyau->x = previousTuyau->x + PAS_ENTRE_TUYAU;
    tuyau->y = randCenter();
}
