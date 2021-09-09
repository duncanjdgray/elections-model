import numpy as np 
import pandas as pd 
import math

class Area:
    def __init__(self, population):
        self.population = population    # todo: investigate to add population from file - may want to input as a series or tuples
        self.voters = None

    def create_voters(self):
        self.voters = None              # clear any existing list of voters
        for i in math.ceil(self.population * self.turnout):
            self.voters.append(Voter()) # todo: add specifics of the voters I am adding here

    def print_voters(self):
        print(self.voters)


class Constituency(Area):
    def __init__(self, population, turnout=1):
        Area.__init__(self, population) # call Parent init

        if turnout >=0 and turnout <=1: # todo: add setter function for turnout (to add fuzz around a national turnout input)
            self.turnout = turnout
        else:
            raise ValueError("turnout must be between 0 and 1 inclusive!")

class Party:
    def __init__(self, voteshare):
        if voteshare >=0 and voteshare <=1:
            self.voteshare = voteshare
        else:
            raise ValueError("voteshare must be between 0 and 1 inclusive!")

class Voter:
    def __init__(self, parties):
        

