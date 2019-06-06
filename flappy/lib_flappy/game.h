#pragma once

void run_flappy(void);
void updateValues(Boule *boule, Tuyau tuyaux[], Cloud clouds[]);
int death(SDL_Surface *ecran, Boule *boule, Tuyau tuyaux[], int difficulty);
void nextTuyau(Tuyau *tuyau, Tuyau *previousTuyau);
void nextCloud(Cloud *cloud, Cloud *previousCloud);
int collision(Boule boule, Tuyau tuyau, int difficulty);
void initBoule(Boule *boule);
int move(SDL_Surface *ecran, Boule *boule, Tuyau tuyaux[], int *score, float *reward, int difficulty, Cloud clouds[]);
int step_flappy(int movement, float *reward);
