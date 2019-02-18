CPP=gcc    #Commande du compilateur
CFLAGS=-O3 #Option d'optimisation du programme
# LDFLAGS=-lSDL2 -lSDL2_mixer #Linker
LDFLAGS=-lSDL -lSDL_mixer -lSDL_image#Linker
EXEC=flappy  #Nom du programme � modifier

OBJS=flappy.o graphique.o game.o tools.o

all: $(EXEC)

flappy: $(OBJS)
	$(CPP) $(CFLAGS) -o flappy $(OBJS) $(LDFLAGS)

flappy.o: flappy.c tools.h game.h
	$(CPP) $(CFLAGS) -c flappy.c

graphique.o : graphique.c tools.h graphique.h
	$(CPP) $(CFLAGS) -c graphique.c

game.o : game.c tools.h game.h graphique.h
	$(CPP) $(CFLAGS) -c game.c

tools.o : tools.c tools.h
	$(CPP) $(CFLAGS) -c tools.c



clean:
	rm -fr *.o

mrproper: clean
	rm -fr $(EXEC)
