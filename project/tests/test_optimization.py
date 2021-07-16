# project/tests/test_optimization.py

from app.optimizer.model import OptimizationModel
from app.optimizer.solver import Solver


def test_modelsize(test_data_optimization):
    instance = OptimizationModel(**test_data_optimization)
    model = instance.generate_model()
    assert model.getNVars() == len(instance.customers) * len(instance.facilities) + len(
        instance.facilities
    )
    assert model.getNConss() == len(instance.customers) + len(
        instance.facilities
    ) + len(instance.customers) * len(instance.facilities)


def test_optimality(test_data_optimization):
    instance = OptimizationModel(**test_data_optimization)
    model = instance.generate_model()
    solver = Solver(model)
    parameters = {
        "setRealParam": {"limits/gap": 0.0},
        "setIntParam": {"conflict/minmaxvars": 0, "conflict/maxlploops": 2},
    }
    solver.setParams(parameters)
    solver.run()
    assert solver.model.getStatus() == "optimal"
    assert solver.model.getObjVal() == 5610.0
