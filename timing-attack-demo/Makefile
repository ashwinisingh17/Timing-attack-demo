
# Makefile for timing-attack-demo
CC ?= gcc
CFLAGS ?= -O2 -Wall -Wextra

all: leaky fixed

leaky: src/leaky.c
	$(CC) $(CFLAGS) -o leaky src/leaky.c

fixed: src/fixed.c
	$(CC) $(CFLAGS) -o fixed src/fixed.c

clean:
	rm -f leaky fixed
