#include <stdio.h>
#include <stdlib.h>
#include <SDL/SDL.h>
#include <SDL/SDL_image.h>
#include <SDL/SDL_ttf.h>

#include "tools.h"
#include "graphique.h"

void draw(SDL_Surface *ecran, SDL_Surface *background, Boule *boule, Tuyau tuyaux[], Font *font, int score) {
    SDL_Rect position;
    position.x = 0;
    position.y = 0;
    SDL_BlitSurface(background, NULL, ecran, &position);

    position.x = boule->x;
    position.y = boule->y;
    SDL_BlitSurface(boule->image, NULL, ecran, &position);

    for (int i = 0; i < NOMBRE_TUYAUX; i++) {
        drawTuyau(ecran, &tuyaux[i]);
    }

    position.x = 10;
    position.y = 10;
    sprintf(font->text, "Score : %d", score);
    font->textSurface = TTF_RenderText_Blended(font->font, font->text, font->color);
    SDL_BlitSurface(font->textSurface, NULL, ecran, &position);

    SDL_Flip(ecran);
}

void drawTuyau(SDL_Surface *ecran, Tuyau *tuyau) {
    SDL_Surface *upperPart = NULL;
    SDL_Surface *lowerPart = NULL;
    SDL_Rect position;
    int largeur;
    if (tuyau->x < LARGEUR_FENETRE) {
        if (tuyau->x >= 0 && tuyau->x < LARGEUR_FENETRE - LARGEUR_TUYAU) {
            largeur = LARGEUR_TUYAU;;
            position.x = tuyau->x;
        } else if (tuyau->x < 0) {
            largeur = LARGEUR_TUYAU + tuyau->x;
            position.x = 0;
        } else {
            largeur = LARGEUR_FENETRE - tuyau->x;
            position.x = LARGEUR_FENETRE - largeur;
        }
        remplissage(ecran, &upperPart, &lowerPart, largeur, tuyau->y);
        position.y = 0;
        SDL_BlitSurface(upperPart, NULL, ecran, &position);
        position.y = tuyau->y + HAUTEUR_TROU / 2;
        SDL_BlitSurface(lowerPart, NULL, ecran, &position);
    }
}

void remplissage(SDL_Surface *ecran, SDL_Surface **upperPart, SDL_Surface **lowerPart, int largeur, int centre) {
    *upperPart = SDL_CreateRGBSurface(SDL_HWSURFACE, largeur, centre - HAUTEUR_TROU / 2, 32, 0, 0, 0, 0);
    *lowerPart = SDL_CreateRGBSurface(SDL_HWSURFACE, largeur, HAUTEUR_FENETRE - centre - HAUTEUR_TROU / 2, 32, 0, 0, 0, 0);
    SDL_FillRect(*upperPart, NULL, SDL_MapRGB(ecran->format, 120, 255, 120));
    SDL_FillRect(*lowerPart, NULL, SDL_MapRGB(ecran->format, 120, 255, 120));
}
