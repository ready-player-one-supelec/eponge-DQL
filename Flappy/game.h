#ifndef DEF_GAME
#define DEF_GAME

void run_game(void);
void updateValues(Boule *boule, Tuyau tuyaux[]);
int death(SDL_Surface *ecran, Boule *boule, Tuyau tuyaux[]);
int randCenter(void);
void nextTuyau(Tuyau *tuyau, Tuyau *previousTuyau);
int collision(Boule boule, Tuyau tuyau);
void initBoule(Boule *boule);
int move(SDL_Surface *ecran, Boule *boule, Tuyau tuyaux[], int *score);

#endif
