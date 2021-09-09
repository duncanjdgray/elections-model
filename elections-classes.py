import numpy as np 
import pandas as pd 
import math

class Area:
    def __init__(self, population):
        self.population = population            # todo: investigate to add population from file - may want to input as a series or tuples
        self.voters = None

    @property
    def population(self):
        return self._population
    
    @population.setter
    def population(self, population):
        if population >= 0:
            self._population = population
        else:
            raise ValueError("population cannot be negative!")

    def create_voters(self):
        self.voters = None                      # clear any existing list of voters
        for i in math.ceil(self.population * self.turnout):
            self.voters.append(Voter())         # todo: add specifics of the voters I am adding here

    def print_voters(self):
        print(self.voters)


class Constituency(Area):
    def __init__(self, population, turnout=1):
        Area.__init__(self, population)         # call Parent init
        self.turnout = turnout

    @property
    def turnout(self):
        return self._turnout

    @turnout.setter
    def turnout(self, turnout):   
        if turnout >=0 and turnout <=1:         # todo: add fuzz around a national turnout input
            self.turnout = turnout
        else:
            raise ValueError("turnout must be between 0 and 1 inclusive!")

class Actor:
    def __init__(self, lib_auth=0, left_right=0):
        self.lib_auth = lib_auth
        self.left_right = left_right
        
    @property
    def lib_auth(self):
        return self._lib_auth
    
    @lib_auth.setter
    def lib_auth(self, lib_auth):
        if lib_auth >= -10 and lib_auth <= 10:
            self._lib_auth = lib_auth
        else:
            raise ValueError("lib_auth must be between -10 and 10 inclusive!")

    @property
    def left_right(self):
        return self._left_right

    @left_right.setter
    def left_right(self, left_right):
        if left_right >= -10 and left_right <= 10:
            self._left_right = left_right
        else:
            raise ValueError("left_right must be between -10 and 10 inclusive!")

class Party(Actor):
    def __init__(self, lib_auth=0, left_right=0, voteshare=0):
        Actor.__init__(lib_auth, left_right)
        self.voteshare = voteshare

    @property
    def voteshare(self):
        return self._voteshare

    @voteshare.setter
    def voteshare(self, voteshare):
        if voteshare >= 0 and voteshare <= 1:
            self._voteshare = voteshare
        else:
            raise ValueError("voteshare must be between 0 and 1 inclusive!")

class Voter(Actor):
    def __init__(self, lib_auth=0, left_right=0):
        Actor.__init__(lib_auth, left_right)
