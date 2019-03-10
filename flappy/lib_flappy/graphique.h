#pragma once

void draw(SDL_Surface *ecran, SDL_Surface *background, Boule *boule, Tuyau tuyaux[], Font *font, int score, int display);
void drawTuyau(SDL_Surface *ecran, Tuyau *tuyau, SDL_Rect *position, SDL_Rect *pipePart);
Uint32 getpixel(SDL_Surface *surface, int x, int y);
void setPixel(SDL_Surface *surface, int x, int y, Uint32 pixel);
void showImage(SDL_Surface *ecran, char *image);
void treatingImage(char *image);
extern Game game;
