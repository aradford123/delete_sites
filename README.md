# delete_sites
This script will delete all of the sites in the hierachy you provide.  The challenge with deletion from the GUI, is you need to delete all of the children (floors/buildings) before you can delete a building or an area.

NOTE:  This has only been tested with python3 as python2 is End of Support.

## Getting stated
First (optional) step, create a vitualenv. This makes it less likely to clash with other python libraries in future.
Once the virtualenv is created, need to activate it.
```buildoutcfg
python3 -m venv env3
source env3/bin/activate
```

Next clone the code.

```buildoutcfg
git clone https://github.com/aradford123/delete_sites.git
```

Then install the  requirements (after upgrading pip). 
Older versions of pip may not install the requirements correctly.
```buildoutcfg
pip install -U pip
pip install -r requirements.txt
```

Edit the dnac_vars file to add your DNAC and credential.  You can also use environment variables.

## Credentials

You can either add environment variables, or edit the  dnac_config.py file
```
import os
DNAC= os.getenv("DNAC") or "sandboxdnac.cisco.com"
DNAC_USER= os.getenv("DNAC_USER") or "devnetuser"
DNAC_PORT=os.getenv("DNAC_PORT") or 8080
DNAC_PASSWORD= os.getenv("DNAC_PASSWORD") or "Cisco123!"
```
## Running the program
a site is required.  If you run the script without the --commit flag, it will just show the sites to be deleted..  Make sure you check this!

```
./delete_sites.py --site Global/test 
COUNT:54
Global/test/sydney/f1
Global/test/sydney
Global/test
```


To actually delete, you need the --commit flag

```
./delete_sites.py --site Global/test --commit
COUNT:54
Global/test/sydney/f1
Global/test/sydney
Global/test
Deleting: Global/test/sydney/f1 (80e81504-0deb-4bfd-8c0c-ea96bb958805/aaf83f3e-b6a2-4f31-84ac-b4f7be26e236/99bff809-a617-4f79-b9f3-6cbbe8d1c031/b998a2b9-8180-40e0-bc78-7c4370776c67)
delete:b998a2b9-8180-40e0-bc78-7c4370776c67
sleeping
{'bapiKey': 'f083-cb13-484a-8fae', 'bapiName': 'Delete Site', 'bapiExecutionId': 'a7e0fe4b-1390-4049-98bf-8506954b0730', 'startTime': 'Wed May 29 09:25:07 UTC 2024', 'startTimeEpoch': 1716974707121, 'endTime': 'Wed May 29 09:25:07 UTC 2024', 'endTimeEpoch': 1716974707865, 'timeDuration': 744, 'status': 'SUCCESS', 'bapiSyncResponse': '{"status":true,"message":"Floor deleted successfully."}', 'runtimeInstanceId': 'DNACP_Runtime_feb34543-5eaa-4b85-94d9-85d9d5277c91'}
Deleting: Global/test/sydney (80e81504-0deb-4bfd-8c0c-ea96bb958805/aaf83f3e-b6a2-4f31-84ac-b4f7be26e236/99bff809-a617-4f79-b9f3-6cbbe8d1c031)
delete:99bff809-a617-4f79-b9f3-6cbbe8d1c031
sleeping
{'bapiKey': 'f083-cb13-484a-8fae', 'bapiName': 'Delete Site', 'bapiExecutionId': '77677562-a5e6-4226-9a29-8ef6f1c53f8e', 'startTime': 'Wed May 29 09:25:09 UTC 2024', 'startTimeEpoch': 1716974709266, 'endTime': 'Wed May 29 09:25:09 UTC 2024', 'endTimeEpoch': 1716974709524, 'timeDuration': 258, 'status': 'SUCCESS', 'bapiSyncResponse': '{"status":true,"message":"Building deleted successfully."}', 'runtimeInstanceId': 'DNACP_Runtime_feb34543-5eaa-4b85-94d9-85d9d5277c91'}
Deleting: Global/test (80e81504-0deb-4bfd-8c0c-ea96bb958805/aaf83f3e-b6a2-4f31-84ac-b4f7be26e236)
delete:aaf83f3e-b6a2-4f31-84ac-b4f7be26e236
sleeping
{'bapiKey': 'f083-cb13-484a-8fae', 'bapiName': 'Delete Site', 'bapiExecutionId': '8fd15100-f14c-44bc-a849-b7a8d26977ee', 'startTime': 'Wed May 29 09:25:11 UTC 2024', 'startTimeEpoch': 1716974711408, 'endTime': 'Wed May 29 09:25:11 UTC 2024', 'endTimeEpoch': 1716974711668, 'timeDuration': 260, 'status': 'SUCCESS', 'bapiSyncResponse': '{"status":true,"message":"Area deleted successfully."}', 'runtimeInstanceId': 'DNACP_Runtime_feb34543-5eaa-4b85-94d9-85d9d5277c91'}
```
