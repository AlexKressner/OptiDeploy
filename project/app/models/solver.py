# project/app/models/solver.py

from abc import ABC, abstractmethod
from typing import Dict, Optional
from app.optimizer.solver_parameters import SolverParameters


# definition of a solver interface which must be followed when implementing custom solvers
class SolverInterface(ABC):
    @abstractmethod
    def set_solver_parameters(self, parameters: Optional[SolverParameters]=None):
        """
        Set parameters (e.g. run time, gap, etc.) to control the behavior of the solver. 
        """
        pass

    @abstractmethod
    def build_model(self):
        """
        Given the problem data, build a formal model instance. If you are not using a classical MIP/
        LP solver this methode might be passed in the subclass.
        """
        pass

    @abstractmethod
    def solve_instance(self):
        """
        Given the problem data, solve the instance. This is where the acutal optimization happens!
        """
        pass

    @abstractmethod
    def get_solution_status(self) -> Dict:
        """
        Return a dictionary which contains relevant statistics about the solution of a problem instance.
        """
        pass