CPP=gcc    #Commande du compilateur
CFLAGS=-O3 #Option d'optimisation du programme
# LDFLAGS=-lSDL2 -lSDL2_mixer #Linker
LDFLAGS=-lSDL -lSDL_mixer -lSDL_image -lSDL_ttf#Linker

OBJS=play.o test.o

all:
	cd lib_flappy; make; cd ..;
	make play test

-include $(OBJS:.o=.d)

play: play.o lib_flappy/lib_flappy.a
	$(CPP) $(CFLAGS) -o play play.o lib_flappy/lib_flappy.a $(LDFLAGS)

test: test.o lib_flappy/lib_flappy.a
	$(CPP) $(CFLAGS) -o test test.o lib_flappy/lib_flappy.a $(LDFLAGS) -lcurses

%.o: %.c
	$(CPP) $(CFLAGS) -c $*.c
	$(CPP) -MM $*.c > $*.d

clean:
	rm -fr *.o *.d play test

mrproper: clean
	rm -fr play test
