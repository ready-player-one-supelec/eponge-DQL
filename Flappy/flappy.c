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

int main (int argc, char *argv[]) {

    // Pipes pipes;
    // pipes.imagesPipe = open("images", O_WRONLY);
    // pipes.actionsPipe = open("actions", O_RDONLY);
    //
    // write(pipes.imagesPipe, "10", SIZE_WRITING_BUFFER_PIPE);
    //
    // read(pipes.actionsPipe, pipes.readingBuffer, SIZE_READING_BUFFER_PIPE);
    // printf("%s\n", pipes.readingBuffer);
    // read(pipes.actionsPipe, pipes.readingBuffer, SIZE_READING_BUFFER_PIPE);
    // printf("%s\n", pipes.readingBuffer);
    // read(pipes.actionsPipe, pipes.readingBuffer, SIZE_READING_BUFFER_PIPE);
    // printf("%s\n", pipes.readingBuffer);
    SDL_Init(SDL_INIT_VIDEO);
    TTF_Init();
    Font font;
    initFont(&font);
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
    game(ecran, background, &boule, &font);
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
                        game(ecran, background, &boule, &font);
                        break;
                }
        }
    }
    SDL_FreeSurface(background);
    SDL_FreeSurface(boule.image);
    TTF_CloseFont(font.font);
    TTF_Quit();

    // sprintf(pipes.writingBuffer, "11");
    // write(pipes.imagesPipe, pipes.writingBuffer, SIZE_WRITING_BUFFER_PIPE);
    // close(pipes.imagesPipe);
    // do {
    //     read(pipes.actionsPipe, pipes.readingBuffer, SIZE_READING_BUFFER_PIPE);
    // } while (!strstr(pipes.readingBuffer, "11"));
    // close(pipes.actionsPipe);
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
