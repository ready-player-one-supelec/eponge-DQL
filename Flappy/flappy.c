#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>

#include <SDL/SDL.h>
#include <SDL/SDL_image.h>
#include <SDL/SDL_ttf.h>

#include "tools.h"
#include "game.h"

void initFont(Font *font);
extern Game game;

int main (int argc, char *argv[]) {

    SDL_Init(SDL_INIT_VIDEO);
    TTF_Init();
    initFont(&game.font);
    game.ecran = SDL_SetVideoMode(LARGEUR_FENETRE, HAUTEUR_FENETRE, 32, SDL_HWSURFACE | SDL_DOUBLEBUF);
    SDL_WM_SetCaption("Flappy Bird", NULL);


    game.background = SDL_CreateRGBSurface(SDL_HWSURFACE, game.ecran->w, game.ecran->h, 32, 0, 0, 0, 0);
    SDL_FillRect(game.background, NULL, SDL_MapRGB(game.ecran->format, 135, 206, 235));
    game.boule.image = IMG_Load("Images/boule.png");
    game.boule.height = game.boule.image->w;

    int continuer = 1;
    SDL_Event event;
    run_game();
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
                        run_game();
                        break;
                }
        }
    }
    SDL_FreeSurface(game.background);
    SDL_FreeSurface(game.boule.image);
    TTF_CloseFont(game.font.font);
    TTF_Quit();
    return EXIT_SUCCESS;
}

void initFont(Font *font) {
    font->font = NULL;
    font->font = TTF_OpenFont("Sugar Addiction - TTF.ttf", 30);
    font->color.r = 255;
    font->color.g = 0;
    font->color.b = 0;
    font->textSurface = NULL;
}
