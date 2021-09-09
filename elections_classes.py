import numpy as np 
import pandas as pd 
import math
import random
from elections_maps import *

class Area:
    def __init__(self, name, population, turnout=1):
        self.name = name
        self.population = population            # todo: investigate to add population from file - may want to input as a series or tuples
        self.turnout = turnout
        self.voters = []
        self.historical_vote_shares = []

    def __str__(self):
        return 'Area: {name}, Population: {population}, Voters: {voters}'.format(name=self.name, population=self.population, voters=len(self.voters))

    def __repr__(self):
        return 'Area(\'{name}\', {population}, {turnout})'.format(name=self.name, population=self.population, turnout=self.turnout)

    @property
    def population(self):
        return self._population
    
    @population.setter
    def population(self, population):
        if population >= 0:
            self._population = population
        else:
            raise ValueError("population cannot be negative!")

    @property
    def turnout(self):
        return self._turnout

    @turnout.setter
    def turnout(self, turnout):   
        if turnout >=0 and turnout <=1:         # todo: add fuzz around a national turnout input
            self._turnout = turnout
        else:
            raise ValueError("turnout must be between 0 and 1 inclusive!")

    def input_hist_shares(self, list_parties, list_shares):
        self.historical_vote_shares = []
        for i in len(list_parties):
            self.historical_vote_shares.append([list_parties[i].name, list_shares[i]])

    def create_voters(self):
        self.voters = []                        # clear any existing list of voters
        for i in math.ceil(self.population * self.turnout):
            self.voters.append(
                Voter(name=str(i),
                      lib_auth=random.uniform(-10,10),
                      left_right=random.uniform(-10,10),
                      priority_axis=random.choices([-1,0,1],[1,4,1],k=1)[0]))         # todo: make voters not purely random

    def print_voters(self):
        print(self.voters)

    def gen_voter_prefs(self, list_parties):
        for i in self.voters:
            i.gen_parties_dist(list_parties)
            i.order_parties()

    # todo: allow areas to hold historical vote shares for parties

class Constituency(Area):
    def __init__(self, name, population, turnout=1):
        Area.__init__(self, name, population, turnout)

    def __str__(self):
        return 'Area: {name}, Population: {population}, Turnout: {turnout}, Voters: {voters}'.format(name=self.name, population=self.population, turnout=self.turnout, voters=len(self.voters))

    def __repr__(self):
        return 'Constituency(\'{name}\', {population}, {turnout})'.format(name=self.name, population=self.population, turnout=self.turnout)

class LocalAuthority(Area):
    def __init__(self, name, population, turnout=1):
        Area.__init__(self, name, population, turnout)

    def __str__(self):
        return 'Area: {name}, Population: {population}, Turnout: {turnout}, Voters: {voters}'.format(name=self.name, population=self.population, turnout=self.turnout, voters=len(self.voters))

    def __repr__(self):
        return 'Constituency(\'{name}\', {population}, {turnout})'.format(name=self.name, population=self.population, turnout=self.turnout)


class Actor:
    def __init__(self, name, lib_auth=0, left_right=0):
        self.lib_auth = lib_auth
        self.left_right = left_right
        self.name = name

    def __str__(self):
        return """Name: {name}, Lib-Auth: {lib_auth}, Left-Right: {left_right}""".format(name=self.name, lib_auth=self.lib_auth, left_right=self.left_right)

    def __repr__(self):
        return 'Actor(\'{name}\', {lib_auth}, {left_right})'.format(name=self.name, lib_auth=self.lib_auth, left_right=self.left_right)

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
    def __init__(self, name, lib_auth=0, left_right=0, voteshare=0):
        Actor.__init__(self, name, lib_auth, left_right)
        self.voteshare = voteshare

    def __str__(self):
        return """Name: {name}, Lib-Auth: {lib_auth}, Left-Right: {left_right}, Vote share: {voteshare}%""".format(name=self.name, lib_auth=self.lib_auth, left_right=self.left_right, voteshare=self.voteshare*100)

    def __repr__(self):
        return 'Party(\'{name}\', {lib_auth}, {left_right}, {voteshare})'.format(name=self.name, lib_auth=self.lib_auth, left_right=self.left_right, voteshare=self.voteshare)

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
    """
        priority_axis will force voter to only care about one axis, not both.
        -1 for lib_auth, 1 for left_right, 0 for both
    """
    def __init__(self, name, lib_auth=0, left_right=0, priority_axis=0):
        Actor.__init__(self, name, lib_auth, left_right)
        self.priority_axis = priority_axis
        self.parties_dist = []

    def __str__(self):
        return """Name: {name}, Lib-Auth: {lib_auth}, Left-Right: {left_right}, Priority: {priority_axis}""".format(name=self.name, lib_auth=self.lib_auth, left_right=self.left_right, priority_axis=map_priority_axes[self.priority_axis])

    def __repr__(self):
        return 'Actor(\'{name}\', {lib_auth}, {left_right}, {priority_axis})'.format(name=self.name, lib_auth=self.lib_auth, left_right=self.left_right, priority_axis=self.priority_axis)

    @property
    def priority_axis(self):
        return self._priority_axis

    @priority_axis.setter
    def priority_axis(self, priority_axis):
        if priority_axis == -1 or priority_axis == 0 or priority_axis == 1:
            self._priority_axis = priority_axis
            self.priority_axis_readable = map_priority_axes[priority_axis]
        else:
            raise ValueError("priority_axis can only be -1, 0 or 1")

    def gen_parties_dist(self, list_parties):
        self.parties_dist = []            # Empty existing list
        for party in list_parties:
            if self.priority_axis == 0:
                self.parties_dist.append( \
                    ((party).name, \
                    math.sqrt( \
                        (self.lib_auth - (party).lib_auth)**2 + 
                        (self.left_right - (party).left_right)**2)))
            elif self.priority_axis == -1:
                self.parties_dist.append( \
                    ((party).name, \
                    abs(self.lib_auth - (party).lib_auth)))
            elif self.priority_axis == 1:
                self.parties_dist.append( \
                    ((party).name, \
                    abs(self.left_right - (party).left_right)))

    def order_parties(self):
        self.parties_dist.sort(key=lambda tup: tup[1])