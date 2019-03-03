#include <stdio.h>
#include <stdlib.h>
#include <curses.h>
#include <unistd.h>
#include "lib_flappy/flappy.h"
#include <SDL/SDL.h>

int main (int argc, char *argv) {
    init_flappy(1);
    // WINDOW *w = initscr();
    // nodelay(w, 1);
    // keypad(w, 1);
    int continuer;
    do {
        continuer = step(random() % 2);
    } while (continuer);
    // endwin();
    // int continuer = 1;
    // SDL_Event event;
    // int movement;
    //
    // while (continuer) {
    //     movement = 0;
    //     SDL_PollEvent(&event);
    //     switch (event.type) {
    //         case SDL_QUIT :
    //             continuer = 0;
    //             break;
    //         case SDL_KEYDOWN :
    //             switch (event.key.keysym.sym) {
    //                 case SDLK_ESCAPE :
    //                     continuer = 0;
    //                     break;
    //                 case SDLK_SPACE :
    //                     movement = 1;
    //                     break;
    //             }
    //             break;
    //     }
    //     continuer = step(movement);
    // }
    exit_flappy();
    return 0;
}
