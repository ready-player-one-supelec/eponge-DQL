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
        }
        updateValues(boule);
        draw(ecran, background, boule);
        SDL_Delay(20);
    }
}

void updateValues(Boule *boule) {
    boule->vy += GRAVITY;
    boule->y += boule->vy;
}
