#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from datetime import datetime
from pytz import timezone
import pytz
import requests,json,os,time,random,re
from bs4 import BeautifulSoup
import base64

def getTime():
    """
    show the present time.
    """
    CN = pytz.timezone('Asia/Taipei')
    CN.zone
    CN_time =CN.localize(datetime.now())#+ timedelta(hours=8))
    fmt = "%Y年_%m月_%d日_%H時_%M分"
    now = CN_time.strftime(fmt)
    return now

def searchNums(url):
    """
    :type:url:string
    :rtype:number:string
    regular expression in one url string to find out number.
    """
    searchNum = re.compile('\d+')
    number = searchNum.search(url).group()
    return number

def str2dict(data_str):
    """
    :type:data_str:string
    :rtype:data:Dict
    """
    data = {}
    for row in data_str.split("\n"):
        kv_list = row.split(":")
        data[kv_list[0]] = kv_list[1].replace(' ','').replace('/','-')
    return data

def timeSleepRandom():
    """
    sleep randomly between 1s and 2s.
    """
    time.sleep(random.randrange(1,3))

def timeSleep():
    """
    sleep 4s
    """
    time.sleep(4)

def mkdir(folderName):
    """
    :type:folderName:string
    create a folder in present working directroy.
    """
    folder = "./{}/".format(folderName)
    if os.path.exists(folder):
        print('已經存在 '+folderName)
        pass
    else:
        os.mkdir(folder)
        print('創建 '+folderName+"！")   

def crawler(page,url):
    """
    :type:page:int
    :type:url:string
    web scraping from https://www.newamazing.com.tw/EW/GO/GroupList.asp 
    and having responses(txt format) into files in folder created by function mkdir.
    """
    global folderName
    global headers
    #不要將字串縮排＠＠
    form_data = """displayType: G
subCd: 
orderCd: 1
pageALL: {0}
pageGO: 1
pagePGO: 1
waitData: false
waitPage: false
mGrupCd: 
SrcCls: 
tabList:  """.format(page)

    reSession = requests.Session()

    res = reSession.post(url,data = str2dict(form_data),headers = headers)
    timeSleepRandom()
    soup = BeautifulSoup(res.text,'html.parser')
    
    with open('./{0}/{1}_{2}_html.txt'.format(folderName,page,'10'),'w',encoding='utf-8')as f:
        f.write(str(soup))
    print('成功寫出第 '+ str(page) + '頁。')
    timeSleep()


def initialFile(folderName):
    """
    :type:folderName:string
    :rtype:htmltxts:List[string]
    listing files orderly via file's name in the specific folder.
    """
    htmltxts = os.listdir('./{}/'.format(folderName))
    htmltxts.sort(key=lambda x: int(x.split('_')[0])) #列舉檔案排序
    htmltxts.sort(key=lambda x: int(x.split('_')[1])) 
    return htmltxts

def photoDownload(photoUri,photoFolder,plan_id,tripPlanCodeName):
    """
    :type:photoUri:string
    :type:photoFolder:string
    :type:plan_id:int
    :type:tripPlanCodeName:string
    downloading photos from photoUri into the specific folder.
    """
    global headers
    resImg = requests.get(photoUri,headers = headers)
    timeSleepRandom()
    deputyFileName = photoUri.split('/')[-1].split('.')[1]
    with open('./{0}/{1}_{2}.{3}'.format(photoFolder,plan_id,tripPlanCodeName,deputyFileName),'wb')as f:
        f.write(resImg.content)
    timeSleep()
    print('順利寫出第 '+ str(plan_id)+ '張。')
#     encoded_string = base64.b64encode(resImg.content)
#     return str(encoded_string,encoding='utf=8')

def dataProcessing(folderName,photoFolder,domainUrl):
    """
    :type:folderName:string
    :type:photoFolder:string
    :type:domainUrl:string
    data processing from the files(txt format) in "folderName" in order to generate json files we want.
    downloading photos from photoUri into the specific folder is alternative!
    """
    global htmltxts
    global headers
    plan_id = 1
    dataDict = {}
    for realtxt in htmltxts:
        with open('./{0}/{1}'.format(folderName,realtxt),encoding='utf-8')as f:
            inn = f.read()
        textSoup = BeautifulSoup(inn,'html.parser')
        textSoupGetItems = textSoup.select_one('#listDataAll').select('.thumbnail')
        for tripPlan in textSoupGetItems:
            print('開始處理第 '+str(plan_id)+'筆。')
            dataDictInner = {}

            dataDictInner['partner_id'] = "1" #新魅力
            dataDictInner['giveaway_id'] = "1" #假設都用第一組贈品資訊
            dataDictInner['continent_id'] = "1" #假設都指向第一個洲
            tripPlanCodeName = tripPlan.select_one('.product_name').text.split('\n')[1].strip()
            dataDictInner['tripPlanCodeName'] = tripPlanCodeName
            dataDictInner['tripPlan'] = tripPlan.select_one('.product_name').text.split('\n')[2].replace('\r\n','').strip()
            dataDictInner['days'] = searchNums(tripPlan.select_one('.product_days').text)
            dataDictInner['dateOfDeparture'] = tripPlan.select_one('.product_date').text.replace('/','-')
            dataDictInner['totalNumber'] = searchNums(tripPlan.select_one('.product_total').text)
            dataDictInner['availableNumber'] = searchNums(tripPlan.select_one('.product_available').text)
            
            dataDictInner['expense'] = searchNums(tripPlan.select_one('.product_price').text.split(',')[0])+            searchNums(tripPlan.select_one('.product_price').text.split(',')[1])
            
            imgUrn = tripPlan.select_one('a img').attrs.get('src')
#             若不要下載圖片，請在下面一組if else中註解掉photoUri and photoDownload。 圖片有部屬在不同的網域中。。。
            if "http://dcimg.travel.net.tw" in imgUrn:
                dataDictInner['domainUrl'] = domainUrl
                dataDictInner['imgUrn'] = imgUrn            
                photoUri = imgUrn
                photoDownload(photoUri,photoFolder,plan_id,tripPlanCodeName)
            else:
                dataDictInner['domainUrl'] = domainUrl
                dataDictInner['imgUrn'] = imgUrn                
                photoUri = domainUrl + imgUrn
                photoDownload(photoUri,photoFolder,plan_id,tripPlanCodeName)       
          
            dataDictInner['tripUrn'] = tripPlan.select_one('a').attrs.get('href')
            
            dataDict[str(plan_id)] = dataDictInner
            print('done '+str(plan_id)+'!')
            plan_id += 1
    with open('./newAmazing_{0}.json'.format(plan_id-1),'w',encoding='utf-8')as f:
        json.dump(dataDict,f,indent=2,ensure_ascii=False)
    with open('./newAmazing_{0}_noindent.json'.format(plan_id-1),'w',encoding='utf-8')as f:
        json.dump(dataDict,f,ensure_ascii=False)

if __name__ == '__main__':

    print('現在開始爬蟲，時間是 '+getTime())
    
    begin = time.time()
    
    folderName = "crawlerForNewamazing"
    photoFolder = "photoForNewamazing"
    url = 'https://www.newamazing.com.tw/EW/GO/GroupList.asp'
    domainUrl = 'https://www.newamazing.com.tw'
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
           "Chrome/72.0.3626.121 Safari/537.36",
          "Accept-Language":"en-US,en;q=0.9"}
    mkdir(folderName)
    
    for page in range(1,11):
        crawler(page,url)
        
    end = time.time()
    
    print("爬蟲執行完畢，共耗時 " +str(end-begin)+'秒。')
    print('現在開始清洗並下載圖片，時間是 '+getTime())
    begin = time.time()
    
    mkdir(photoFolder)
    htmltxts = initialFile(folderName)
    dataProcessing(folderName,photoFolder,domainUrl)
    
    end = time.time()
    print("清洗並下載圖片執行完畢，共耗時 " +str(end-begin)+'秒。')

