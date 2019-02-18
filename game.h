#ifndef DEF_GAME
#define DEF_GAME

void game(SDL_Surface *ecran, SDL_Surface *background, Boule *boule, Font *font);
void updateValues(Boule *boule, Tuyau tuyaux[]);
int death(SDL_Surface *ecran, Boule *boule, Tuyau tuyaux[]);
int randCenter();
void nextTuyau(Tuyau *tuyau, Tuyau *previousTuyau);
int collision(Boule boule, Tuyau tuyau);
void initBoule(Boule *boule);

#endif
