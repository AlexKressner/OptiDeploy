# project/tests/test_solutions.py

import json


def test_create_solution(test_app, test_data_post):
    response = test_app.post("/instances/", data=json.dumps(test_data_post))
    instance_id = response.json()["_id"]
    response = test_app.post(f"/solutions/{instance_id}/")
    assert response.status_code == 202
    assert response.json()["linked_instance_id"] == instance_id


def test_get_solution_by_solution_id(test_app, test_data_post):
    response = test_app.post("/instances/", data=json.dumps(test_data_post))
    instance_id = response.json()["_id"]
    parameters = {
        "setRealParam": {"limits/gap": 0.0},
        "setIntParam": {"conflict/minmaxvars": 0, "conflict/maxlploops": 2},
    }
    response = test_app.post(f"/solutions/{instance_id}/", data=json.dumps(parameters))
    solution_id = response.json()["_id"]
    response = test_app.get(f"/solutions/by_solution_id/{solution_id}/")
    response_dict = response.json()
    assert response.status_code == 200
    assert response_dict["_id"] == solution_id
    assert response_dict["status"] == "optimal"
    assert response_dict["objective_function_value"] == 5610.0


def test_get_solution_by_instance_id(test_app, test_data_post):
    response = test_app.post("/instances/", data=json.dumps(test_data_post))
    instance_id = response.json()["_id"]
    response = test_app.post(f"/solutions/{instance_id}/")
    solution_id_1 = response.json()["_id"]
    response = test_app.post(f"/solutions/{instance_id}/")
    solution_id_2 = response.json()["_id"]
    response = test_app.get(f"/solutions/by_instance_id/{instance_id}/")
    response_list = response.json()
    assert response.status_code == 200
    assert len(response_list) == 2
    assert response_list[0]["_id"] == solution_id_1
    assert response_list[1]["_id"] == solution_id_2


def test_delete_solution(test_app, test_data_post):
    response = test_app.post("/instances/", data=json.dumps(test_data_post))
    instance_id = response.json()["_id"]
    response = test_app.post(f"/solutions/{instance_id}/")
    solution_id = response.json()["_id"]
    response = test_app.delete(f"/solutions/{solution_id}/")
    assert response.status_code == 200
    assert response.json()["_id"] == solution_id
    response = test_app.get(f"/solutions/by_solution_id/{solution_id}/")
    assert response.status_code == 404
