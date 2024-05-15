##
## This file builds assignment 1
##

CFLAGS = -g -Wall -std=c99 -pedantic -fPIC

## uncomment/change this next line if you need to use a non-default compiler
CC = clang
PYTHON_INCLUDE = /usr/include/python3.10
PYTHON_INCLUDE_LIB = /usr/lib/python3.10

##
## We can define variables for values we will use repeatedly below
##

## define the executables we want to build
A1LIB = libphylib.so
A2LIB = _phylib.so

## define the set of object files we need to build each executable
A1OBJS = phylib.o
A2OBJS = phylib_wrap.o

##
## TARGETS: below here we describe the target dependencies and rules
##
all: $(A1LIB) $(A2LIB)

$(A1LIB): $(A1OBJS)
	$(CC) $(CFLAGS) -shared -o $(A1LIB) $(A1OBJS) -lm

phylib_wrap.c: phylib.i
	swig -python phylib.i

$(A2OBJS): phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I$(PYTHON_INCLUDE) -o $(A2OBJS)

$(A2LIB): $(A2OBJS) $(A1LIB)
	$(CC) $(CFLAGS) -shared -o $(A2LIB) $(A2OBJS) -L. -L$(PYTHON_INCLUDE_LIB) -lpython3.10 -lphylib -lm

## convenience target to remove the results of a build
clean :
	- rm -f -I $(A1OBJS) $(A1LIB) $(A2OBJS) $(A2LIB)