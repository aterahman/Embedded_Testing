from time import time

import responses
import pytest
import requests
import json
from datetime import datetime


from responses.registries import OrderedRegistry

#first part of first request
@responses.activate
def sample_1_i():
    responses.add(responses.GET, 'https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions',
                  json={"api": "/api/v1.0/swupdate/sw-versions",
                      "status": "success",
                      "versions": {
                          "name": "Cruise 1.0",
                          "version": "1.0",
                      }})
    resp = requests.get('https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions')
    assert resp.json() == {"api": "/api/v1.0/swupdate/sw-versions",
                      "status": "success",
                      "versions": {
                          "name": "Cruise 1.0",
                          "version": "1.0",
                      }}
    assert resp.status_code == 200
    print("\n",resp.json())



#second part of first request
@responses.activate(registry=OrderedRegistry)
def sample_1_ii():
            responses.add(
                responses.GET,
                "https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions",
                json={"msg": "Success"},
                status=200,
            )
            responses.add(
                responses.GET,
                "https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions",
                json={"msg": "Internal Server Error"},status=500,
            )
            responses.add(
                responses.GET,
                "https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions",
                json={"msg": "Unauthorized"},status=401,
            )
            responses.add(
                responses.GET,
                "https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions",
                json={"msg": "Bad request"},status=400,
            )

            #checks for success message
            response1 = requests.get("https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions")
            assert response1.status_code == 200
            assert response1.json() =={"msg": "Success"}

            #checks for internal server error
            response2 = requests.get("https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions")
            assert response2.status_code == 500
            assert response2.json() =={"msg": "Internal Server Error"}
            response3 = requests.get("https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions")

            #checks for unauthorized error
            assert response3.status_code == 401
            assert response3.json() =={"msg": "Unauthorized"}

            #checks for bad request error
            response4 = requests.get("https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions")
            assert response4.status_code == 400
            assert response4.json() =={"msg": "Bad request"}

#second request
@responses.activate
def sample_2():
    responses.add(responses.GET, 'https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions',
                  json={"api": "/api/v1.0/swupdate/sw-versions",
                      "status": "success",
                      "versions": {
                          "name": "Cruise 1.0",
                          "version": "1.0",
                      }})
    resp = requests.get('https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions')
    ans=resp.json()["versions"]
    if ans["version"]!="2.0":
        responses.add(responses.GET,
                      'https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions',
                      json={"api": "/api/v1.0/swupdate/sw-versions",
                            "status": "success",
                            "versions": {
                                "name": "Cruise 1.0",
                                "version": "2.0",
                            }})
        response = requests.get('https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/sw-versions')
        print(response.json())

#third request
@responses.activate
def sample_3():
    responses.add(responses.GET, 'https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/hw-revison',
                  json={"api": "/api/v1.0/swupdate/hw-revision",
                      "status": "success",
                      "board": "Cruiseboardname",
                      "revision": "1.1", })
    response = requests.get('https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/hw-revison')
    #print(resp.json()["board"])
    try:
        assert response.json()["board"] == "Cruiseboardname" and response.json()["revision"] == "1.1"
    except AssertionError:
        print("boardname and revision did not matched")


#fourth request
@responses.activate
def sample_4():
     time=str(datetime.now())
     responses.add(responses.GET,'https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/system/clock/value',json={'current_time': time})
     response = requests.get('https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/system/clock/value')
     print(response.json())
     try:
         assert response.json()["current_time"] == time
         print("Pass")
     except AssertionError:
         print("fail")


#fifth request
@responses.activate
def sample_5():
    responses.add(responses.GET, 'https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/boot-status',
                  json={"api": "/api/v1.0/swupdate/boot-status",
                        "boot-status": "success",
                        "status": "fail"})
    response = requests.get('https://7facbdb5-b28c-46e1-a70f-a00b44f62626.mock.pstmn.io/api/v1.0/swupdate/boot-status')
    if response.json()["status"] == "fail":
        print("device should be reset")
    else:
        print("device is working properly")

