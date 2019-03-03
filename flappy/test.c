#include <stdio.h>
#include <stdlib.h>
#include <curses.h>
#include <unistd.h>

int main (int argc, char *argv) {
    WINDOW *w = initscr();
    nodelay(w, 1);
    keypad(w, 1);
    int ret;
    do {
        ret = getch();
        switch (ret) {
            case 259 : // up
                printw("UP\n");
                break;
            case 258 :
                printw("DOWN\n");
                break;
        }
    } while (ret != 27);
    endwin();
    return 0;
}
