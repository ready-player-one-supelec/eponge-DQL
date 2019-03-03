#pragma once

void reset_flappy(void);
void init_flappy(int display);
void exit_flappy(void);
void run_flappy(void);
int step_flappy(int movement);

#ifdef _LIB_FLAPPY
void initFont(Font *font);
void initBoule(Boule *boule);
void changeDisplay(int display);
extern Game game;
#endif
