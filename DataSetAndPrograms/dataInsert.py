#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*-

import pymysql
import base64
import json,time,os,re

def initialFile(folderName):
    """
    :type:folderName:string
    :rtype:htmltxts:List[string]
    listing files orderly via file's name in the specific folder.
    """
    photos = os.listdir('./{}/'.format(folderName))
    photos.sort(key=lambda x: int(x.split('_')[0])) #列舉檔案排序
    return photos

def searchNums(url):
    """
    :type:url:string
    :rtype:number:string
    regular expression in one url string to find out number.
    """
    searchNum = re.compile('\d+')
    number = searchNum.search(url).group()
    return number


def loadDataInfo(fileName):
    """
    :type:fileName:string
    :rtype:fileName:json
    reading data from local file.
    """    
    with open('./{0}.json'.format(fileName))as f:
        fileName = json.load(f)
    return fileName


def loadPhotoInBase64(key,photos,folderName):
    """
    :type:key:string
    :type:photos:list
    :type:folderName:string
    :rtype:encoded_string:string
    reading photos from local folders and transfroming photos into string encoded by base64 and utf-8.
    """ 
    photoComparePool = [photo.split('_')[0] for photo in photos]
    if key in photoComparePool:
        index = photoComparePool.index(key)
        photoFile = photos[index]
        with open('./{0}/{1}'.format(folderName,photoFile),'rb')as image_file:
            encoded_string = base64.b64encode(image_file.read())  #bytes String
        return str(encoded_string,encoding='utf-8') # 即使強制用utf-8編碼，仍可以用base64.b64decode解碼印出圖片。
    else:
        return 'None'
    

def insertIntoMainTable(file,photos,folderName):
    """
    :type:file:json
    :type:photos:list
    :type:folderName:string
    :rtype:averageTime:string
    inserting data into database, especially for the table TripPlan .
    """ 
    #本地
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='admin',charset='utf8', db='tripresso')  #連結資料庫
    cursor = conn.cursor()
    # 確保資料庫接受utf8mb4格式的資料！
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    #----------------------------
    cursor.close()

    print('開始進行insert！資料一共有：'+str(len(file)))
    total = 0

    try:
        for key in list(file.keys())[0:]:
            print('進行第 '+key+'筆資料：')
            with conn.cursor() as cursor: #這種寫法讓cursor每執行完SQL後，就會休息(cursor.close())。
                
                begin = time.time()
                
                cursor.execute("SET foreign_key_checks = 0")

                # discount設成0元           
                SQL = ("insert into TripPlan (partner_id"
                ",giveaway_id"
                ",continent_id"
                ",tripPlanCodeName"
                ",tripPlan"
                ",days"
                ",introPhoto"
                ",dateOfDeparture"
                ",expense"
                ",discount"
                ",domainUrl"
                ",imgUrn"
                ",tripUrn"
                ") values ({0})".format(','.join(
                    ["'" +file[key]['partner_id']+"'" \
                    ,"'" +file[key]['giveaway_id']+"'" \
                    ,"'" +file[key]['continent_id']+"'" \
                    ,"'" +file[key]['tripPlanCodeName']+"'" \
                    ,"'" +file[key]['tripPlan']+"'" \
                    ,"'" +file[key]['days']+"'" \
                    ,"'" +loadPhotoInBase64(key,photos,folderName)+"'" \
                    ,"'" +file[key]['dateOfDeparture']+"'" \
                    ,"'" +file[key]['expense']+"'" \
                    ,"'" +str(0)+"'" \
                    ,"'" +file[key]['domainUrl']+"'" \
                    ,"'" +file[key]['imgUrn']+"'" \
                    ,"'" +file[key]['tripUrn']+"'" ]
                                            )
                                        )
                      )
                cursor.execute(SQL)
                cursor.execute("SET foreign_key_checks = 1")
                
            conn.commit()

            end = time.time()
            timeSpend = end - begin
            total += timeSpend
            print('每筆耗時：'+ str(timeSpend))
    except Exception as e:
        print('key='+key+'時，發生錯誤：' + str(e))
        conn.rollback()
        conn.close()
        
    finally:
        conn.close()

    print('done '+key)
    return '平均每筆耗時：'+str(total/len(file))+' 秒'

def insertIntoOthers():
    """
    inserting data into database, especially for the tables except for TripPlan.
    """ 
    conn = pymysql.connect('localhost',port=3306,user='root',passwd='admin',charset='utf8', db='tripresso')  #連結資料庫
    cursor = conn.cursor()
    # 確保資料庫接受utf8mb4格式的資料！
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    #----------------------------
    cursor.close()
    with open('./DateOf2019.json')as f:
        DateOf2019 = json.load(f)
    with open('./newAmazing_199_SET.json')as f:
        newAmazingFile = json.load(f)
    with open('./orangetour_200.json')as f:
        orangeTourFile = json.load(f)
    try:
        with conn.cursor() as cursor:
            # SQL 指令-------------------------
            SQL_Continent = "insert into Continent  values ('1','亞洲')"
            SQL_Country = "insert into Country values ('1','1','台灣','高雄','南部')"
            SQL_Giveaway = "insert into Giveaway values ('1',%s)"
            SQL_PartnerCorp = "insert into PartnerCorp values(%s,%s,%s)"
            SQL_WowFactor = "insert into WowFactor values ('1','地表最強','比薩諾思還強')"
            SQL_Date = "insert into Date (date) values (%s)"
            
            SQL_Evaluation_Of_PartnerCorp = ("insert into Evaluation_Of_PartnerCorp"
            "(partner_id,plan_id,schedule,serviceOfTourGuide,meals,accomodation,vehicle,responseFromCustomer,"
            "dateOfResponse,response)"
            "values('1','1','5','5','5','5','5','太棒了，真的比薩諾思還厲害！','2019-3-20','不只有薩諾思，還有孫悟空！謝謝')")
            
            SQL_Date_And_TripPlan = ("insert into Date_And_TripPlan"
            "(plan_id,date_id,availableNumber,totalNumber,readyToGo,terminate)"
            "values (%s,%s,%s,%s,%s,%s)")
            
            SQL_WowFactor_And_TripPlan = ("insert into WowFactor_And_TripPlan (plan_id,wow_id)"
            "values (%s,%s)")
            # cursor執行-------------------------
            cursor.execute("SET foreign_key_checks = 0")
            print('開始Continent表格插入資料：')
            cursor.execute(SQL_Continent)
            
            print('開始Country表格插入資料：')
            cursor.execute(SQL_Country)
            
            print('開始Giveaway表格插入資料：')
            cursor.execute(SQL_Giveaway,json.dumps(['繽紛款行李束帶','中華電信原號漫遊7日(2G)']))
            
            print('開始PartnerCorp表格插入資料：')
            paramsPartner = (('1','新魅力旅遊',newAmazingIntro),('2','澄果旅遊',orangeTour))
            cursor.executemany(SQL_PartnerCorp,paramsPartner)
            
            print('開始WowFactor表格插入資料：')
            cursor.execute(SQL_WowFactor)
            
            print('開始Evaluation_Of_PartnerCorp表格插入資料：')
            cursor.execute(SQL_Evaluation_Of_PartnerCorp)
            
            print('開始Date表格插入資料：')
            paramsDate = DateOf2019
            cursor.executemany(SQL_Date,paramsDate)
            
            print('開始Date_And_TripPlan & WowFactor_And_TripPlan 表格插入資料：')
            for key in newAmazingFile:
                plan_id = key
                date_id = DateOf2019.index(newAmazingFile[key]['dateOfDeparture'])+1
                availableNumber = int(newAmazingFile[key]['availableNumber'])
                totalNumber = int(newAmazingFile[key]['totalNumber'])
                if (totalNumber - availableNumber) == 0:
                    readyToGo = "0"
                    terminate = "0"
                elif (totalNumber - availableNumber) == totalNumber:
                    readyToGo = "1"
                    terminate = "1"
                elif availableNumber <= 5:
                    readyToGo = "1"
                    terminate = "0"
                paramsNewAmazing = (plan_id,date_id,availableNumber,totalNumber,readyToGo,terminate)
                cursor.execute(SQL_Date_And_TripPlan,paramsNewAmazing)
                cursor.execute(SQL_WowFactor_And_TripPlan,(plan_id,'1'))
            for key in orangeTourFile:
                plan_id = int(key)+199
                date_id = DateOf2019.index(orangeTourFile[key]['dateOfDeparture'])+1
                availableNumber = int(orangeTourFile[key]['availableNumber'])
                totalNumber = int(orangeTourFile[key]['totalNumber'])
                if (totalNumber - availableNumber) == 0:
                    readyToGo = "0"
                    terminate = "0"
                elif (totalNumber - availableNumber) == totalNumber:
                    readyToGo = "1"
                    terminate = "1"
                elif availableNumber <= 5:
                    readyToGo = "1"
                    terminate = "0"
                paramsOrangeTour = (plan_id,date_id,availableNumber,totalNumber,readyToGo,terminate)
                cursor.execute(SQL_Date_And_TripPlan,paramsOrangeTour)  
                cursor.execute(SQL_WowFactor_And_TripPlan,(plan_id,'1'))
            cursor.execute("SET foreign_key_checks = 1")
        conn.commit()
        print('完成其他表格資料插入！')
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
    finally:
        conn.close()  
        
if __name__ == '__main__':
    
    folderName1 = "photoForNewamazing_SET"
    folderName2 = "photoForOrangetour"
    photos1 = initialFile(folderName1)
    photos2 = initialFile(folderName2)

    fileName1 = "newAmazing_199_SET"
    fileName2 = "orangetour_200"
    file1 = loadDataInfo(fileName1)
    file2 = loadDataInfo(fileName2)
    
    averageTime1 = insertIntoMainTable(file1,photos1,folderName1)
    averageTime2 = insertIntoMainTable(file2,photos2,folderName2)
    print('檔案'+fileName1+'平均耗時：')
    print(averageTime1)
    print('檔案'+fileName2+'平均耗時：')
    print(averageTime2)
    print('開始其他表格的資料插入：')
    
    newAmazingIntro = ("創立於2001年的世興旅行社，秉持『以誠、實、信、義為宗旨，以客戶需求為核心，專業服務為導向，堅持讓客戶"
    "感受旅遊的新魅力』 的經營理念，草創初期僅有七名員工，但在全體人員勤奮的努力之下，於2002年成立台北分公司。"
    "並正式登記『新魅力旅遊』品牌識別，深入東南亞旅遊市場，以專業與豐富行程規劃下，確立專業 東南亞旅遊的形象。 "
    "十多年來世興旅行社更擴展日本、韓國、中國大陸、海島與歐洲…等地。忠於理念的經營方向、型態、制度以及企業文化，"
    "致力成為旅遊愛好者最愛的旅遊品牌。自2001年至今，每年連續獲得長榮航空公司以及各地觀光局的肯定，世興旅行社")
    orangeTour = ("自成立後以清新專業的形象震撼整個旅遊市場，以團隊多年控團經驗，推出多樣超值國內外旅遊產品，"
    "並結合各式通路，多元銷售，服務遍及全台。 澄果服務團隊秉持『澄心澄意做好每次旅遊!』的理念，與多家航空公司合作推出自家價格"
    "平實且超值的優質行程，如中國大陸、歐美長程、頂級遊輪、東北亞、東南亞地區、自由行等，產品遍及世界各地，至今已替無數旅客圓夢，"
    "帶給大家難忘的美好旅遊經歷。無論您是想要親子旅遊、古蹟巡禮、蜜月旅行、海島假期等專業團隊都能滿足您的需求；給您最完整、"
    "最貼心的專屬服務，就和澄果旅遊一起環遊世界，活到老，玩到老！ 澄心誠意，做好每一次旅遊！")
    insertIntoOthers()

