#pragma once

void run_flappy(void);
void updateValues(Boule *boule, Tuyau tuyaux[]);
int death(SDL_Surface *ecran, Boule *boule, Tuyau tuyaux[], int difficulty);
void nextTuyau(Tuyau *tuyau, Tuyau *previousTuyau);
int collision(Boule boule, Tuyau tuyau, int difficulty);
void initBoule(Boule *boule);
int move(SDL_Surface *ecran, Boule *boule, Tuyau tuyaux[], int *score, float *reward, int difficulty);
int step_flappy(int movement, float *reward);
