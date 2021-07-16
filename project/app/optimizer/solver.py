# project/optimizer/solver.py

from typing import Dict, Optional

from pydantic import BaseModel, constr


#####################################################################################
# Pydantic model for SCIP solver paramters
# list of paramters for scip solver: https://www.scipopt.org/doc/html/PARAMETERS.php
#####################################################################################
class SCIPParameters(BaseModel):
    setBoolParam: Optional[Dict[str, bool]] = None
    setIntParam: Optional[Dict[str, int]] = None
    setRealParam: Optional[Dict[str, float]] = None
    setCharParam: Optional[Dict[str, constr(min_length=1, max_length=1)]] = None
    setStringParam: Optional[Dict[str, str]] = None

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


###############################################
# SCIP solver
###############################################
class Solver:
    def __init__(self, model):
        self.model = model

    def setParams(self, parameters: SCIPParameters):
        if parameters:
            if "setBoolParam" in parameters:
                for key, value in parameters["setBoolParam"].items():
                    self.model.setBoolParam(key, value)
            if "setIntParam" in parameters:
                for key, value in parameters["setIntParam"].items():
                    self.model.setIntParam(key, value)
            if "setRealParam" in parameters:
                for key, value in parameters["setRealParam"].items():
                    self.model.setRealParam(key, value)
            if "setCharParam" in parameters:
                for key, value in parameters["setCharParam"].items():
                    self.model.setCharParam(key, value)
            if "setStringParam" in parameters:
                for key, value in parameters["setStringParam"].items():
                    self.model.setStringParam(key, value)

    def run(self):
        self.model.optimize()
