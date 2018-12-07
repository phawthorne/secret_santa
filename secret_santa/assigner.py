import os
import pandas as pd
import numpy as np
from itertools import combinations, permutations
from gurobipy import *


def generate_solutions(names, excluded_sets, number):
    assignments = []
    for i in range(number):
        result = generate_assignment(names, excluded_sets, excluded_assignments=assignments)
        assignments.append(result)

    return assignments


def generate_assignment(names, excluded_sets, excluded_assignments=None):
    m = Model('secret-santa')
    gives_to = {}
    for n in names:
        for k in names:
            gives_to[(n, k)] = m.addVar(vtype=GRB.BINARY)

    weight = {}
    for n in names:
        weight[(n, n)] = np.random.rand()

    for n, k in permutations(names, 2):
        weight[(n, k)] = np.random.rand()

    for n in names:
        m.addConstr(gives_to[(n, n)], GRB.EQUAL, 0)
        m.addConstr(quicksum([gives_to[(n, k)] for k in names]), GRB.EQUAL, 1)
        m.addConstr(quicksum([gives_to[(k, n)] for k in names]), GRB.EQUAL, 1)

    for es in excluded_sets:
        for pair in combinations(es, 2):
            m.addConstr(gives_to[(pair[0], pair[1])], GRB.EQUAL, 0)
            m.addConstr(gives_to[(pair[1], pair[0])], GRB.EQUAL, 0)

    if excluded_assignments is not None:
        for ea in excluded_assignments:
            m.addConstr(quicksum((gives_to[(n, k)] for n, k in ea)), GRB.LESS_EQUAL, len(ea) - 1)

    m.setObjective(quicksum((gives_to[(n, k)] * weight[(n, k)] for n in names for k in names)), GRB.MAXIMIZE)
    m.update()
    m.optimize()
    assignment = []
    for n in names:
        for k in names:
            if gives_to[(n, k)].x == 1:
                assignment.append((n, k))

    return assignment
