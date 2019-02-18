#ifndef DEF_GRAPHIQUE
#define DEF_GRAPHIQUE

void draw(SDL_Surface *ecran, SDL_Surface *background, Boule *boule, Tuyau tuyaux[], int nombreTuyaux);
void drawTuyau(SDL_Surface *ecran, Tuyau *tuyau);
void remplissage(SDL_Surface *ecran, SDL_Surface **upperPart, SDL_Surface **lowerPart, int largeur, int centre);

#endif
