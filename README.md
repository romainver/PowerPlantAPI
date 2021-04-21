Powerplant Trading API Reference
===================

This document explain how to build and use the Powerplant Trading API.

API goal is to calculate how much power each of a multitude of different powerplants need to produce (a.k.a. the production-plan) when the load is given and taking into account the cost of the underlying energy sources (gas, kerosine) and the Pmin and Pmax of each powerplant.



----------


Building Powerplant Trading using Docker
-------------

**Prerequisites :** docker and docker-compose. 
Reference : https://github.com/docker/compose

**Step 1** : Extract the archive in a local repository.

**Step 2** Inside local repo, open a terminal prompt and run :

	docker-compose up -d

**Step 3** Access API endpoint by browsing to http://localhost:8888/productionplan

----------

POST Requests
-------------------

The API accept POST requests at /productionplan 
Body content of POST request must be of JSON type.
JSON example : https://github.com/gem-spaas/powerplant-coding-challenge/tree/master/example_payloads
API will return a JSON containing the payload response,  specifying for each powerplant how much power each powerplant should deliver. 