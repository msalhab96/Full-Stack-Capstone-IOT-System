# Full-Stack-Capstone-IOT-System

##  Full Stack Developer Nanodegree Capstone Project
To access the API use the following Link: https://devicespro.herokuapp.com/

## Setting Up you Machine
- install the dependencies 
  - python3.x
  - install the requirements in reuirements.txt file using " pip install -r requirements"


## Getting Started with the API

the project is hosted [HERE](https://devicespro.herokuapp.com/), please make sure to use the 'Bearer' as Authentication in the header

the application contains 2 main roles:
- Admin role: can do all the following:
  - list all devices or certain device  
  - delete a certain device 
  - change the status of a certain device 
  - adding a measure 
- User Role: can list all the devices onle

## Endpoints
the API has the following endpoints:
  - GET /devices/<int:id> endpoint
    - returns a descrition about the given device by its id 
    - available for all users and admins and public
    - Example: https://devicespro.herokuapp.com/devices/5
    
    the result: 
    
    {"DeviceData":{"CreationDate":"Wed, 24 Feb 2021 19:57:31 GMT","DeviceName":"TEST DEVICE 1","ID":5,"LatestUpdate":"Wed, 24 Feb 2021 19:57:31 GMT","Status":true},"Success":true}
  - GET /devices/list endpoint 
    - list all the devices in the database
    - available for admin and users only (authentication should be passed)
    - Example: https://devicespro.herokuapp.com/devices/list
    
  - DELETE device/<int:id> endpoint
    - used to delete a certain devce by it's id 
    - used by admins only
    
  - PATCH /status/change endpoint
    - used to change the status of a device by sending the json in the request's body 
    - the request should enclude the following json {"id": int, "status": bool}, where the id is the id of the targeted device and status is boolean 
    - used by admin only

  - POST /add/measure endpoint
    - used to add new device by sending it's details in json in the request's body 
    - the json should look like {"value": float, "rank": int, "time" datetime, "device": int} device represent the id of the device the measures are taken from
    - used by admins only
    
