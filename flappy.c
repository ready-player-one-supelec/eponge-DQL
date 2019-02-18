#include <stdio.h>
#include <stdlib.h>

#include <SDL/SDL.h>
#include <SDL/SDL_image.h>

#include "tools.h"
#include "game.h"

int main (int argc, char *argv[]) {

    SDL_Init(SDL_INIT_VIDEO);
    SDL_Surface *ecran = NULL;
    ecran = SDL_SetVideoMode(LARGEUR_FENETRE, HAUTEUR_FENETRE, 32, SDL_HWSURFACE | SDL_DOUBLEBUF);
    SDL_WM_SetCaption("Flappy Bird", NULL);


    SDL_Surface *background = SDL_CreateRGBSurface(SDL_HWSURFACE, ecran->w, ecran->h, 32, 0, 0, 0, 0);
    SDL_FillRect(background, NULL, SDL_MapRGB(ecran->format, 135, 206, 235));
    Boule boule;
    boule.image = IMG_Load("Images/boule.png");
    boule.height = boule.image->w;

    int continuer = 1;
    SDL_Event event;
    game(ecran, background, &boule);
    while(continuer) {
        SDL_WaitEvent(&event);
        switch (event.type) {
            case SDL_QUIT :
                continuer = 0;
                break;
            case SDL_KEYDOWN :
                switch (event.key.keysym.sym) {
                    case SDLK_ESCAPE :
                        continuer = 0;
                        break;
                    case 13 :
                        game(ecran, background, &boule);
                        break;
                }
        }
    }

    return EXIT_SUCCESS;
}
