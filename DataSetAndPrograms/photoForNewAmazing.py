#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# http://dcimg.travel.net.tw
def photoDownload(photoUri,photoFolder,plan_id,tripPlanCodeName):
    global headers
    resImg = requests.get(photoUri,headers = headers)
    timeSleepRandom()
    deputyFileName = photoUri.split('/')[-1].split('.')[1]
    with open('./{0}/{1}_{2}.{3}'.format(photoFolder,plan_id,tripPlanCodeName,deputyFileName),'wb')as f:
        f.write(resImg.content)
    timeSleep()
    print('順利寫出第 '+ str(plan_id)+ '張。')
    
with open('./newAmazing_199_SET.json')as f:
    innn = json.load(f)

photoFolder = "photoForNewamazing"

for key in innn:
    if "http://dcimg.travel.net.tw" in innn[key]['imgUrn']:
        photoUri = innn[key]['imgUrn']
        plan_id = key
        tripPlanCodeName = innn[key]['tripPlanCodeName']
        photoDownload(photoUri,photoFolder,plan_id,tripPlanCodeName)       
    else:
        photoUri = innn[key]['domainUrl']+innn[key]['imgUrn']
        plan_id = key
        tripPlanCodeName = innn[key]['tripPlanCodeName']
        photoDownload(photoUri,photoFolder,plan_id,tripPlanCodeName)

