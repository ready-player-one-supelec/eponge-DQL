#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>

#define _LIB_FLAPPY
#include "tools.h"
#include "flappy.h"
#include "game.h"

char* init_flappy(int display, int difficulty) {
    SDL_Init(SDL_INIT_VIDEO);
    TTF_Init();
    initFont(&game.font);
    game.ecran = SDL_SetVideoMode(LARGEUR_FENETRE, HAUTEUR_FENETRE, 32, SDL_HWSURFACE | SDL_DOUBLEBUF);
    SDL_WM_SetCaption("Flappy Bird", NULL);

    game.display = display;
    Uint32 pipeColor = SDL_MapRGB(game.ecran->format, 120, 255, 120);
    Uint32 skyColor = SDL_MapRGB(game.ecran->format, SKY_RED, SKY_GREEN, SKY_BLUE);
    game.skyColorGrayScale = (char)(0.2126 * SKY_RED + 0.7152 * SKY_GREEN + 0.0722 * SKY_BLUE);
    if (game.display) {
        game.background = SDL_CreateRGBSurface(SDL_HWSURFACE, game.ecran->w, game.ecran->h, 32, 0, 0, 0, 0);
    } else {
        game.background = SDL_CreateRGBSurface(SDL_HWSURFACE, (X_MAX - X_MIN), game.ecran->h, 32, 0, 0, 0, 0);
    }
    SDL_FillRect(game.background, NULL, skyColor);

    game.n_pipes = 3;
    game.pipe = (SDL_Surface **) malloc(game.n_pipes * sizeof(SDL_Surface *));
    char name[100];
    for (int i = 0; i < game.n_pipes; i++) {
        snprintf(name, sizeof(name), "Images/brick-wall-%d.png", i);
        game.pipe[i] = IMG_Load(name);
    }

    game.cloud = IMG_Load("Images/cloud-0.png");
    game.n_clouds = 1;

    game.boule.frame_counter = 0;
    game.boule.frame_step = 3;
    game.boule.n_images = 4;
    game.boule.currentImage = 0;
    game.boule.image = (SDL_Surface **) malloc(game.boule.n_images * sizeof(SDL_Surface *));
    for (int i = 0; i < game.boule.n_images; i++) {
        snprintf(name, sizeof(name), "Images/bird-%d.png", i);
        game.boule.image[i] = IMG_Load(name);
    }
    game.boule.height = game.boule.image[0]->w;
    reset_flappy(difficulty);

    char *pointeur = NULL;
    pointeur = (char *)malloc((X_SIZE * Y_SIZE + 1)* sizeof(char));
    return pointeur;
}

void initBoule(Boule *boule) {
    boule->y = 170;
    boule->vy = 0;
    boule->x = BOULE_XAXIS;
    boule->vx = 3;
}

void reset_flappy(int difficulty) {
    initBoule(&game.boule);
    game.tuyaux[0].x = 300 ;
    game.tuyaux[0].y = randCenter();
    game.tuyaux[0].number = random() % game.n_pipes;
    game.clouds[0].x = random() % (LARGEUR_FENETRE / 2);
    game.clouds[0].y = random() % (HAUTEUR_FENETRE);
    game.clouds[0].number = random() % game.n_clouds;
    game.clouds[0].vx = (random() % 20) / 10.0;
    game.clouds[0].width = game.cloud->w;
    game.score = 0;
    game.stepsSurvived = 0;
    game.updatedScore = 1;
    game.difficulty = difficulty;

    for (int i = 1; i < NOMBRE_TUYAUX ; i++) {
        nextTuyau(&game.tuyaux[i], &game.tuyaux[(i-1) % NOMBRE_TUYAUX]);
    }
    for (int i = 1; i < NOMBRE_NUAGES; i++) {
        nextCloud(&game.clouds[i], &game.clouds[(i-1) % NOMBRE_NUAGES]);
    }
}

void changeDisplay(int display) {
    game.display = display;
}

void exit_flappy(void) {
    SDL_FreeSurface(game.background);
    for (int i = 0; i < game.boule.n_images; i++) {
        SDL_FreeSurface(game.boule.image[i]);
    }
    for (int i = 0; i < game.n_pipes; i++) {
        SDL_FreeSurface(game.pipe[i]);
    }
    free(game.boule.image);
    free(game.pipe);
    TTF_CloseFont(game.font.font);
    TTF_Quit();
}

void initFont(Font *font) {
    font->font = NULL;
    font->font = TTF_OpenFont("Sugar Addiction - TTF.ttf", 30);
    font->color.r = 255;
    font->color.g = 255;
    font->color.b = 255;
    font->textSurface = NULL;
}

void getSize(int *x_size, int *y_size) {
    *x_size = X_SIZE;
    *y_size = Y_SIZE;
}

void updateFeatures(int *xToPipe, float *yToUpperPipe, float *yToLowerPipe, float *vy, float *yToTop, float *yToBottom) {
    Tuyau nextPipe = game.tuyaux[0];
    for (int i = 1; i < NOMBRE_TUYAUX; i++) {
        if (game.boule.x >= game.tuyaux[i].x - PAS_ENTRE_TUYAU + LARGEUR_TUYAU && game.boule.x < game.tuyaux[i].x + LARGEUR_TUYAU) {
            nextPipe = game.tuyaux[i];
            break;
        }
    }
    *xToPipe = max(0, (int) (nextPipe.x - game.boule.x - game.boule.height));
    *yToUpperPipe = game.boule.y + HAUTEUR_TROU / 2 - nextPipe.y;
    *yToLowerPipe = nextPipe.y + HAUTEUR_TROU / 2 - game.boule.y - game.boule.height;
    *vy = game.boule.vy;
    *yToTop = game.boule.y;
    *yToBottom = HAUTEUR_FENETRE - game.boule.y - game.boule.height;
}
