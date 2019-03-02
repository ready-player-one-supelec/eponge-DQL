#include <stdio.h>
#include <stdlib.h>

#include "tools.h"
#include "game.h"
#include "graphique.h"

Game game;

void run_flappy(void) {
    int continuer = 1;
    SDL_Event event;
    initBoule(&game.boule);
    game.tuyaux[0].x = 700 ;
    game.tuyaux[0].y = randCenter();
    game.score = 0;

    for (int i = 1; i < NOMBRE_TUYAUX ; i++) {
        nextTuyau(&game.tuyaux[i], &game.tuyaux[(i-1) % NOMBRE_TUYAUX]);
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
                        game.boule.vy = -7.5;
                        break;
                }
                break;
        }
        continuer = move(game.ecran, &game.boule, game.tuyaux, &game.score);
        draw(game.ecran, game.background, &game.boule, game.tuyaux, &game.font, game.score);
        SDL_Delay(20);
    }
}

int move(SDL_Surface *ecran, Boule *boule, Tuyau tuyaux[], int *score) {
    updateValues(boule, tuyaux);
    if (death(ecran, boule, tuyaux)) {
        return 0;
    } else {
        int i, tmp;
        for (i = 0; i < NOMBRE_TUYAUX; i++) {
            if (tuyaux[i].x < -LARGEUR_TUYAU) {
                nextTuyau(&tuyaux[i], &tuyaux[(NOMBRE_TUYAUX + i-1) % NOMBRE_TUYAUX]);
            }
        }
        for (i = 0; i < NOMBRE_TUYAUX; i++) {
            tmp = tuyaux[i].x + LARGEUR_TUYAU;
            if (boule->x >= tmp && boule->x < tmp + boule->vx) {
                *score++;
                break;
            }
        }
        return 1;
    }
}

void initBoule(Boule *boule) {
    boule->y = 70;
    boule->vy = 0;
    boule->x = BOULE_XAXIS;
    boule->vx = 3;
}

int death(SDL_Surface *ecran, Boule *boule, Tuyau tuyaux[]) {
    if (boule->y < 0) {
        return 1;
    } else if (boule->y > ecran->h - boule->height) {
        return 1;
    }
    for (int i = 0; i < NOMBRE_TUYAUX; i ++) {
        if (collision(*boule, tuyaux[i])) {
            return 1;
        }
    }
    return 0;
}


int collision(Boule boule, Tuyau tuyau) {
    if (boule.x - TOLERANCE < tuyau.x - boule.height || boule.x + TOLERANCE > tuyau.x + LARGEUR_TUYAU) {
        return 0;
    }
    if (boule.x > tuyau.x - boule.height / 2 && boule.x < tuyau.x + LARGEUR_TUYAU - boule.height / 2) {
        if (boule.y + TOLERANCE < tuyau.y - HAUTEUR_TROU / 2) {
            return 1;
        } else if (boule.y + boule.height - TOLERANCE > tuyau.y + HAUTEUR_TROU / 2) {
            return 1;
        } else {
            return 0;
        }
    } else {
        int xCentre = boule.x + boule.height / 2;
        int yCentre = boule.y + boule.height / 2;
        if (boule.y < tuyau.y - HAUTEUR_TROU / 2 || boule.y > tuyau.y + HAUTEUR_TROU / 2) {
            return 1;
        }
        int xCoin[2] = {tuyau.x, tuyau.x + LARGEUR_TUYAU};
        int yCoin[2] = {tuyau.y - HAUTEUR_TROU / 2, tuyau.y + HAUTEUR_TROU / 2};
        int dx, dy;
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                dx = xCoin[i] - xCentre;
                dy = yCoin[j] - yCentre;
                if (dx * dx + dy * dy + TOLERANCE * TOLERANCE <= boule.height * boule.height / 4) {
                    return 1;
                }
            }
        }
        return 0;
    }
}

void updateValues(Boule *boule, Tuyau tuyaux[]) {
    boule->vy += GRAVITY;
    boule->y += boule->vy;
    for (int i = 0; i < NOMBRE_TUYAUX; i++) {
        tuyaux[i].x -= boule->vx;
    }
}


void nextTuyau(Tuyau *tuyau, Tuyau *previousTuyau) {
    tuyau->x = previousTuyau->x + PAS_ENTRE_TUYAU;
    tuyau->y = randCenter();
}
