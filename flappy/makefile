CPP=gcc    #Commande du compilateur
CFLAGS=-O3 #Option d'optimisation du programme
# LDFLAGS=-lSDL2 -lSDL2_mixer #Linker
LDFLAGS=-lSDL -lSDL_mixer -lSDL_image -lSDL_ttf#Linker
EXEC=play  #Nom du programme � modifier

OBJS=play.o

all: $(EXEC)

-include $(OBJS:.o=.d)

play: $(OBJS)
	$(CPP) $(CFLAGS) -o play $(OBJS) lib_flappy/lib_flappy.a $(LDFLAGS)

%.o: %.c
	$(CPP) $(CFLAGS) -c $*.c
	$(CPP) -MM $*.c > $*.d

clean:
	rm -fr *.o *.d $(EXEC)

mrproper: clean
	rm -fr $(EXEC)
