CPP=gcc    #Commande du compilateur
CFLAGS=-O3 #Option d'optimisation du programme
# LDFLAGS=-lSDL2 -lSDL2_mixer #Linker
LDFLAGS=-lSDL -lSDL_mixer -lSDL_image#Linker
EXEC=flappy  #Nom du programme � modifier

OBJS=flappy.o graphique.o game.o

all: $(EXEC)

flappy: $(OBJS)
	$(CPP) $(CFLAGS) -o flappy $(OBJS) $(LDFLAGS)

flappy.o: flappy.c flappy.h graphique.h game.h
	$(CPP) $(CFLAGS) -c flappy.c

graphique.o : graphique.c flappy.h graphique.h
	$(CPP) $(CFLAGS) -c graphique.c

game.o : game.c flappy.h game.h graphique.h
	$(CPP) $(CFLAGS) -c game.c


clean:
	rm -fr *.o

mrproper: clean
	rm -fr $(EXEC)
