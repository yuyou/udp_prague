# run this like this:
# GNU make utility (make/gmake in Linux/FreeBSD)

SRC=prague_cc.cpp
HEADERS=prague_cc.h
CPPFLAGS=-std=c++11 -O3 -c -fPIC
WARN=-Wall -Wextra
LDFLAGS = -shared -o libprague.so

ifeq ($(OS),Windows_NT)
	CPP=g++
else
	UNAME=$(shell uname -s)
	ifeq ($(UNAME),Linux)
		CPP=g++
	else ifeq ($(UNAME),FreeBSD)
		CPP=clang++
	else ifeq ($(UNAME),Darwin)
		CPP=clang++
	endif
endif
AR=ar

all: udp_prague_receiver udp_prague_sender libprague.so

# Target: Build the library
libprague.so: prague_wrapper.o
	$(CPP) $(LDFLAGS) prague_wrapper.o

prague_wrapper.o: prague_wrapper.c
	$(CPP) $(CPPFLAGS) prague_wrapper.c
	
lib_prague: $(SRC) $(HEADERS) Makefile
	$(CPP) $(CPPFLAGS) $(WARN) -c $(SRC) -o libprague.o
	$(AR) rcs libprague.a libprague.o

udp_prague_receiver: udp_prague_receiver.cpp $(HEADERS) Makefile lib_prague
	$(CPP) udp_prague_receiver.cpp -L. -lprague --std=c++11 -pthread -O3 -Wall -Wextra -o $@

udp_prague_sender: udp_prague_sender.cpp $(HEADERS) Makefile lib_prague
	$(CPP) udp_prague_sender.cpp -L. -lprague --std=c++11 -pthread -O3 -Wall -Wextra -o $@

clean:
	rm -rf udp_prague_receiver udp_prague_sender *.a *.o
