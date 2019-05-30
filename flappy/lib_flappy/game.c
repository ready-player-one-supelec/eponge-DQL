#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "tools.h"
#include "game.h"
#include "graphique.h"

Game game;

void run_flappy(void) {
    int continuer = 1;
    SDL_Event event;
    int movement;
    float garbage;

    while (continuer) {
        movement = WAIT;
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
                        movement = JUMP;
                        break;
                }
                break;
        }

        continuer = step_flappy(movement, &garbage);
    }
}


int step_flappy(int movement, float *reward) {
    if (movement == JUMP) {
        game.boule.vy = IMPULSE;
    }

    int continuer = move(game.ecran, &game.boule, game.tuyaux, &game.score, reward, game.difficulty);
    draw(game.ecran, game.background, &game.boule, game.tuyaux, &game.font, game.score, game.display, game.difficulty);
    if (game.display){
        SDL_Delay(20);
    }
    return continuer;
}

int move(SDL_Surface *ecran, Boule *boule, Tuyau tuyaux[], int *score, float *reward, int difficulty) {
    updateValues(boule, tuyaux);
    *reward = 0;
    if (death(ecran, boule, tuyaux, difficulty)) {
        *reward = -1.0;
        return 0;
    } else {
        *reward = 0.1;
        game.stepsSurvived++;
        int i, tmp;
        for (i = 0; i < NOMBRE_TUYAUX; i++) {
            if (tuyaux[i].x < -LARGEUR_TUYAU) {
                nextTuyau(&tuyaux[i], &tuyaux[(NOMBRE_TUYAUX + i-1) % NOMBRE_TUYAUX]);
            }
        }
        for (i = 0; i < NOMBRE_TUYAUX; i++) {
            tmp = tuyaux[i].x + LARGEUR_TUYAU;
            if (boule->x >= tmp && boule->x < tmp + boule->vx) {
                (*score)++;
                game.updatedScore = 1;
                *reward = 1.0;
                break;
            }
        }
        return 1;
    }
}

int death(SDL_Surface *ecran, Boule *boule, Tuyau tuyaux[], int difficulty) {
    if (boule->y < 0) {
        return 1;
    } else if (boule->y > ecran->h - boule->height) {
        return 1;
    }
    if (difficulty == NO_PIPE) {
        return 0;
    }
    for (int i = 0; i < NOMBRE_TUYAUX; i ++) {
        if (collision(*boule, tuyaux[i], difficulty)) {
            return 1;
        }
    }
    return 0;
}


int collision(Boule boule, Tuyau tuyau, int difficulty) {
    if (boule.x - TOLERANCE < tuyau.x - boule.height || boule.x + TOLERANCE > tuyau.x + LARGEUR_TUYAU) {
        return 0;
    }
    if (boule.x > tuyau.x - boule.height / 2 && boule.x < tuyau.x + LARGEUR_TUYAU - boule.height / 2) {
        if (boule.y + TOLERANCE < tuyau.y - HAUTEUR_TROU / 2) {
            return difficulty == WHOLE_PIPE ? 1 : 0;
        } else if (boule.y + boule.height - TOLERANCE > tuyau.y + HAUTEUR_TROU / 2) {
            return 1;
        } else {
            return 0;
        }
    } else {
        int xCentre = boule.x + boule.height / 2;
        int yCentre = boule.y + boule.height / 2;
        if (((boule.y < tuyau.y - HAUTEUR_TROU / 2) && (difficulty == WHOLE_PIPE)) || boule.y > tuyau.y + HAUTEUR_TROU / 2) {
            return 1;
        }
        int xCoin[2] = {tuyau.x, tuyau.x + LARGEUR_TUYAU};
        int yCoin[2] = {tuyau.y - HAUTEUR_TROU / 2, tuyau.y + HAUTEUR_TROU / 2};
        int dx, dy;
        for (int i = 0; i < 2; i++) {
            for (int j = (difficulty == WHOLE_PIPE ? 0 : 1); j < 2; j++) {
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
    tuyau->number = random() % game.n_pipes;
}
