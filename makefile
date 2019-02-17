CPP=gcc    #Commande du compilateur
CFLAGS=-O3 #Option d'optimisation du programme
# LDFLAGS=-lSDL2 -lSDL2_mixer #Linker
LDFLAGS=-lSDL -lSDL_mixer -lSDL_image#Linker
EXEC=flappy  #Nom du programme � modifier

OBJS=flappy.o

all: $(EXEC)

ms: $(OBJS)
	$(CPP) $(CFLAGS) -o ms $(OBJS) $(LDFLAGS)

flappy.o: flappy.c
	$(CPP) $(CFLAGS) -c flappy.c



clean:
	rm -fr *.o

mrproper: clean
	rm -fr $(EXEC)
