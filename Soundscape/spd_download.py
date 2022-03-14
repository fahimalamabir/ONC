# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:07:13 2022

@author: abir29793
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 07:15:57 2022

@author: abir29793
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 20:00:11 2022

@author: aBr
"""

from datetime import timedelta
from dateutil.parser import parse
from onc.onc import ONC
# https://wiki.oceannetworks.ca/display/DP/51
 
token = ' '
onc = ONC(token=token)

 
# start and end date
dateFrom = parse('2020-03-05T00:00:00.000Z')
dateTo = parse('2022-03-04T00:00:00.000Z')
 
# time to add to dateFrom
step = timedelta(hours=1)
 
# use a loop to download 1 hour at a time
while dateFrom < dateTo:
    txtDate = dateFrom.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    print("\nDownloading data from: {:s}\n".format(txtDate))
 
    filters = {
        'dataProductCode' : 'HSPD',
        'locationCode' : 'ECHO3.H4',
        'deviceCategoryCode': 'HYDROPHONE',
        'dateFrom' : txtDate,
        'dateTo' : 'PT1H',
      #  'dpo_hydrophoneChannel':'All', # return results for all available hydrophone channels
      #  'dpo_hydrophoneAcquisitionMode':'All',        
        'dpo_filePlotBreaks': '2', # Weekly
        'dpo_hydrophoneDataDiversionMode':'OD',
        'extension' : 'mat'
    }
    result = onc.orderDataProduct(filters,includeMetadataFile	= False)
    dateFrom += step
 
print("\nFinished!")