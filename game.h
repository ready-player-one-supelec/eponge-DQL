#ifndef DEF_GAME
#define DEF_GAME

#define GRAVITY 0.4

void game(SDL_Surface *ecran, SDL_Surface *background, Boule *boule);
void updateValues(Boule *boule);
int death(SDL_Surface *ecran, Boule *boule);

#endif
