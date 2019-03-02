CPP=gcc    #Commande du compilateur
CFLAGS=-O3 #Option d'optimisation du programme
# LDFLAGS=-lSDL2 -lSDL2_mixer #Linker
LDFLAGS=-lSDL -lSDL_mixer -lSDL_image -lSDL_ttf#Linker
EXEC=flappy  #Nom du programme � modifier

OBJS=flappy.o graphique.o game.o tools.o

all: $(EXEC)

-include $(OBJS:.o=.d)

flappy: $(OBJS)
	$(CPP) $(CFLAGS) -o flappy $(OBJS) $(LDFLAGS)

%.o: %.c
	$(CPP) $(CFLAGS) -c $*.c
	$(CPP) -MM $*.c > $*.d

clean:
	rm -fr *.o

mrproper: clean
	rm -fr $(EXEC)
