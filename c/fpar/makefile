CC=/usr/bin/gcc
OBJ = fpar.o basefunc.o
SRC = test.c
BIN = a.out

CFLAGS  = -Wall -g
LDFLAGS = -lm

all: $(OBJ) $(BIN)

a.out: $(OBJ) $(SRC)
	$(CC) $(CFLAGS) -o $(BIN) $(SRC) $(OBJ) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean::
	rm -rf $(OBJ) $(BIN)

