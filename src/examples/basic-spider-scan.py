#!/usr/bin/env python
# A basic ZAP Python API example which spiders and scans a target URL

import time
from pprint import pprint
from zapv2 import ZAPv2


apikey = None # Change to match the API key set in ZAP, or use None if the API key is disabled
#
# By default ZAP API client will connect to port 8080
zap = ZAPv2(apikey=apikey)
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
# zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

zap._request(zap.base + 'openapi/action/importUrl/',{'url':'http://petstore.swagger.io/v2/swagger.json'})
target = 'http://127.0.0.1'

# Proxy a request to the target so that ZAP has something to deal with
print 'Accessing target %s' % target
zap.urlopen(target)
# Give the sites tree a chance to get updated
time.sleep(2)

print 'Spidering target %s' % target
scanid = zap.spider.scan(target)
# Give the Spider a chance to start
time.sleep(2)
while (int(zap.spider.status(scanid)) < 100):
    # Loop until the spider has finished
    print 'Spider progress %: ' + zap.spider.status(scanid)
    time.sleep(2)

print 'Spider completed'

while (int(zap.pscan.records_to_scan) > 0):
      print ('Records to passive scan : ' + zap.pscan.records_to_scan)
      time.sleep(2)

print 'Passive Scan completed'

print 'Active Scanning target %s' % target
scanid = zap.ascan.scan(target)
while (int(zap.ascan.status(scanid)) < 100):
    # Loop until the scanner has finished
    print 'Scan progress %: ' + zap.ascan.status(scanid)
    time.sleep(5)

print 'Active Scan completed'

# Report the results

print 'Hosts: ' + ', '.join(zap.core.hosts)
print 'Alerts: '
pprint (zap.core.alerts())
