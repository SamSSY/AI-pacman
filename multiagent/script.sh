#!/bin/sh

python pacman.py --frameTime 0 -p ReflexAgent -k 1 -q
python pacman.py --frameTime 0 -p ReflexAgent -k 2 -q
python pacman.py -p ReflexAgent -l openClassic -n 10 -q
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4 -q
python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3 -q
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic -q
python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
python pacman.py -l smallClassic -p ExpectimaxAgent -a evalFn=better -q -n 20


