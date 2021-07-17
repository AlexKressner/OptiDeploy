# project/tests/test_instances.py

import json


def test_create_instance(test_app, test_data_post):
    response = test_app.post("/instances/", data=json.dumps(test_data_post))
    assert response.status_code == 201


def test_get_instance(test_app, test_data_post):
    response = test_app.post("/instances/", data=json.dumps(test_data_post))
    instance_id = response.json()["_id"]
    response = test_app.get(f"/instances/{instance_id}/")
    response_dict = response.json()
    assert response_dict["_id"] == instance_id
    assert response.status_code == 200
    assert response_dict["customers"] == test_data_post["customers"]
    assert response_dict["facilities"] == test_data_post["facilities"]
    assert response_dict["transportation_cost"] == test_data_post["transportation_cost"]
    assert response_dict["facility_capacity"] == test_data_post["facility_capacity"]
    assert response_dict["facility_installation_cost"] == test_data_post["facility_installation_cost"]
    assert response_dict["demand"] == test_data_post["demand"]
    assert response_dict["created_at"]


def test_delete_instance(test_app, test_data_post):
    response = test_app.post("/instances/", data=json.dumps(test_data_post))
    instance_id = response.json()["_id"]
    response = test_app.delete(f"/instances/{instance_id}/")
    assert response.status_code == 200
    assert response.json()["_id"] == instance_id
    response = test_app.get(f"/instances/{instance_id}/")
    assert response.status_code == 404
