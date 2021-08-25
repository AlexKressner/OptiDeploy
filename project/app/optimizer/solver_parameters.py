# project/app/optimizer/solver_parameters.py

from pydantic import BaseModel, constr
from typing import Dict, Optional


class SolverParameters(BaseModel):
    """
    Definition of parameters to control the behavior of the solver (e.g. run time, gap, etc.).
    Example with SCIP solver parameters which can be found at https://www.scipopt.org/doc/html/PARAMETERS.php
    """

    setBoolParam: Optional[Dict[str, bool]] = None
    setIntParam: Optional[Dict[str, int]] = None
    setRealParam: Optional[Dict[str, float]] = None
    setCharParam: Optional[Dict[str, constr(min_length=1, max_length=1)]] = None
    setStringParam: Optional[Dict[str, str]] = None

    # example for solver settings to show in openapi doc
    class Config:
        schema_extra = {
            "example": {
                "setBoolParam": {
                    "branching/preferbinary": False,
                    "branching/delaypscostupdate": True,
                },
                "setIntParam": {"conflict/minmaxvars": 0, "conflict/maxlploops": 2},
                "setRealParam": {"branching/scorefac": 0.167, "branching/clamp": 0.2},
                "setCharParam": {
                    "branching/scorefunc": "p",
                    "branching/lpgainnormalize": "s",
                },
                "setStringParam": {
                    "visual/bakfilename": "-",
                    "heuristics/undercover/fixingalts": "li",
                },
            }
        }