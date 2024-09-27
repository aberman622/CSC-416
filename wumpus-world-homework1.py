#Aidan Berman : CSC 416 Assignment 1

import itertools

class World:
    def __init__(self, size):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
    
    def add_wumpus(self, x, y):
        self.grid[x][y] = 'W'
    
    def add_pit(self, x, y):
        self.grid[x][y] = 'P'

class Player:
    def __init__(self, world):
        self.world = world
        self.knowledge_base = []

    def add_knowledge(self, fact):
        self.knowledge_base.append(fact)
    
    def inference_by_resolution(self, query):
        cnf_kb = [self.convert_to_cnf(clause) for clause in self.knowledge_base]
        cnf_query = self.convert_to_cnf(('NOT', query))
        clauses = cnf_kb + [cnf_query]

        while True:
            new_clauses = []
            for (ci, cj) in itertools.combinations(clauses, 2):
                resolvents = self.resolve(ci, cj)
                if resolvents == []:
                    return True
                new_clauses += resolvents
            if set(new_clauses).issubset(set(clauses)):
                return False
            clauses += new_clauses
    
    def resolve(self, ci, cj):
        resolvents = []
        for literal in ci:
            if ('NOT', literal) in cj:
                new_clause = set(ci) | set(cj)
                new_clause.remove(literal)
                new_clause.remove(('NOT', literal))
                resolvents.append(tuple(new_clause))
        return resolvents
    
    def convert_to_cnf(self, sentence):
        if isinstance(sentence, str):
            return [sentence]
        if sentence[0] == 'NOT':
            return [('NOT', sentence[1])]
        if sentence[0] == 'AND':
            return [self.convert_to_cnf(clause) for clause in sentence[1:]]
        if sentence[0] == 'OR':
            return [self.convert_to_cnf(literal) for literal in sentence[1:]]
        if sentence[0] == 'IMPLIES':
            return [('OR', ('NOT', sentence[1]), sentence[2])]
        if sentence[0] == 'IFF':
            p_to_q = ('IMPLIES', sentence[1], sentence[2])
            q_to_p = ('IMPLIES', sentence[2], sentence[1])
            return self.convert_to_cnf(('AND', p_to_q, q_to_p))
        return sentence

# Example 
world = World(4)
player = Player(world)

# Adding the knowledge to the KB
player.add_knowledge('P')  # P is True
player.add_knowledge(('IMPLIES', 'P', 'Q'))  # P => Q

# Query the KB
print("Q:", player.inference_by_resolution('Q'))  # print True
print("NOT Q:", player.inference_by_resolution(('NOT', 'Q')))  # print False