# project/tests/test_optimization.py

from app.optimizer.solver import Solver


def test_optimality(test_data_optimization):
    solver = Solver(**test_data_optimization)
    solver.build_model()
    parameters = {
        "setRealParam": {"limits/gap": 0.0},
        "setIntParam": {"conflict/minmaxvars": 0, "conflict/maxlploops": 2},
    }
    solver.set_solver_parameters(parameters)
    solver.solve_instance()
    solution = solver.get_solution_status()
    assert solution["status"] == "optimal"
    assert solution["objective_function_value"] == 5610.0


def test_no_solver_parameters(test_data_optimization):
    solver = Solver(**test_data_optimization)
    solver.build_model()
    solver.set_solver_parameters()
    solver.solve_instance()
    solution = solver.get_solution_status()
    assert solution["status"] == "optimal"
    assert solution["objective_function_value"] == 5610.0
