import numpy as np
import pandas as pd

import pyomo.environ as pyo


def solve(S, Rc, nc, nd, gc, gd):
    # definicja zmiennej
    model = pyo.ConcreteModel()
    model.Iset = pyo.RangeSet(1, 6)
    model.Jset = pyo.RangeSet(0, len(S) - 1)
    model.x = pyo.Var(model.Jset, model.Iset, domain=pyo.NonNegativeReals)

    # ograniczenia
    def rule1(m, j):
        return m.x[j, 4] + m.x[j, 5] <= Rc - (-1 * sum(m.x[k, 3] for k in m.Jset if k < j) +
                                              nc * (sum(m.x[k, 4] for k in m.Jset if k < j) +
                                                    sum(m.x[k, 5] for k in m.Jset if k < j)) - sum(
                    m.x[k, 6] for k in m.Jset if k < j))

    model.rule1 = pyo.Constraint(model.Jset, rule=rule1)

    def rule2(m, j):
        return m.x[j, 1] + nd * m.x[j, 3] + m.x[j, 2] == S.D[j]

    model.rule2 = pyo.Constraint(model.Jset, rule=rule2)

    def rule3(m, j):
        return m.x[j, 3] + m.x[j, 6] <= -1 * sum(m.x[k, 3] for k in m.Jset if k < j) + \
            nc * (sum(m.x[k, 4] for k in m.Jset if k < j) + sum(m.x[k, 5] for k in m.Jset if k < j)) - \
            sum(m.x[k, 6] for k in m.Jset if k < j)

    model.rule3 = pyo.Constraint(model.Jset, rule=rule3)

    def rule4(m, j):
        return m.x[j, 4] + m.x[j, 5] <= gc

    model.rule4 = pyo.Constraint(model.Jset, rule=rule4)

    def rule5(m, j):
        return m.x[j, 3] + m.x[j, 6] <= gd

    model.rule5 = pyo.Constraint(model.Jset, rule=rule5)

    def rule6(m, j):
        return m.x[j, 4] + m.x[j, 1] <= S.E[j]

    model.rule6 = pyo.Constraint(model.Jset, rule=rule6)

    # Funkcja

    def objective(m):
        return np.sum(S.P * S.D) - sum(S.P[k] * (m.x[k, 5] - nd * m.x[k, 6] + m.x[k, 2]) for k in m.Jset)

    model.objective = pyo.Objective(rule=objective, sense=pyo.maximize)

    # Rozwiązanie

    opt = pyo.SolverFactory('glpk', executable='C:\glpk-4.65\w64\glpsol.exe')
    _ = opt.solve(model)
    a = np.array([[model.x[j, i].value for i in model.Iset] for j in model.Jset])
    columns = ['WD', 'GD', 'RD', 'WR', 'GR', 'RG']
    return pd.DataFrame(a, columns=columns)
