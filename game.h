#ifndef DEF_GAME
#define DEF_GAME

void game(SDL_Surface *ecran, SDL_Surface *background, Boule *boule);
void updateValues(Boule *boule, Tuyau tuyaux[], int nombreTuyaux);
int death(SDL_Surface *ecran, Boule *boule);

#endif
