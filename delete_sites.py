#!/usr/bin/env python
from argparse import ArgumentParser
from dnacentersdk import api
from dnacentersdk.exceptions import ApiError
import logging
import json
from  time import sleep, time, strftime, localtime
from dnac_config import DNAC, DNAC_USER, DNAC_PASSWORD
logger = logging.getLogger(__name__)
timeout = 10

#LIMIT = 500
LIMIT = 10
class SiteCache:
    def __init__(self,dnac):
        self._cache = {}
        self.dnac = dnac
        response = dnac.sites.get_site_count()
        count = response.get('response',0)
        print ("COUNT:{}".format(count))
        # loop through pages
        for start in range(1, count+1, LIMIT):
            #response = get_url("group?groupType=SITE&offset={}&limit={}".format(start,LIMIT))
            response = dnac.sites.get_site(offset=start,limit=LIMIT)
            # add to cache
            sites = response['response']
            for s in sites:
                logging.debug("Caching {}".format(s['siteNameHierarchy']))
                self._cache[s['siteNameHierarchy']] =  s
        #done
        self._new_cache_site("Global","area")

    def _new_cache_site(self,name,type):
        self._cache[name] = {'siteNameHierarchy' : name, 'additionalInfo' : [{'attributes' : {'type' :type}}]}

    def lookup(self, fqSiteName):
        if fqSiteName in self._cache:
            return self._cache[fqSiteName]
        else:
            raise ValueError("Cannot find site:{}".format(fqSiteName))

    def find_children(self,name):
        site = self.lookup(name)
        site_id_path = site['siteHierarchy']
        result = []
        for site in self._cache.values():
            if site['siteNameHierarchy'] != 'Global' and site_id_path in site['siteHierarchy']:
                result.append({site['siteHierarchy']: site['siteNameHierarchy']})
        return sorted(result,reverse=True, key=lambda x: list(x.keys())[0])

    def wait_on_task(self,taskurl):
        while True:
            task = dnac.custom_caller.call_api(method="GET",resource_path=taskurl)
            if task.status != "IN_PROGRESS":
                break
            print("sleeping")
            sleep(1)
        return task
            
    def del_site(self, id_path):
        site_id = id_path.split("/")[-1]
        print(f'delete:{site_id}')
        response = dnac.sites.delete_site(site_id)
        excution = response.executionId
        task = self.wait_on_task(response.executionStatusUrl)
        #status': 'FAILURE', 'bapiError': '{"message":["The input site is not valid or site is not present."]
        sleep(1)
        if task.status == "FAILURE":
            failure = json.loads(task.bapiError)
            print(failure['message'], failure['response']['message'])
            print()
        else:
            print(task.bapiSyncResponse)

def main(dnac, sitename, commit):
    # build site cache
    cache = SiteCache(dnac)
    remove = cache.find_children(sitename)
    names =  "\n".join([value for d in remove for key, value in d.items()])
    print(f'{names}')
    if commit:
        id_paths = [(key,value) for d in remove for key, value in d.items()]
        for id_path,name in id_paths:
            print(f'Deleting: {name} ({id_path})')
            cache.del_site(id_path)
            

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    parser.add_argument('--password',  type=str, required=False,
                        help='new passowrd')
    parser.add_argument('--dnac',  type=str,default=DNAC,
                        help='dnac IP')
    parser.add_argument('--commit', action='store_true',
                        help="commit")

    parser.add_argument('--site',  type=str,required=True,
                        help='site name to delete (and all children)')
    parser.add_argument('arguments', nargs='*', help='Additional arguments as a list.')
    args = parser.parse_args()

    if args.v:
        root_logger=logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)
        logger.debug("logging enabled")

    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    DNAC = args.dnac
    dnac = api.DNACenterAPI(base_url='https://{}:443'.format(DNAC),
                                #username=DNAC_USER,password=DNAC_PASSWORD,verify=False,debug=True)
                                username=DNAC_USER,password=DNAC_PASSWORD,verify=False)
    main(dnac, args.site, args.commit)
