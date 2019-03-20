
# Tripresso
------
## Intention of this project:

- In order to meet __Tripresso Corporation's ([website](https://www.tripresso.com/ "旅遊咖"))__ expectation.



---
# Next, there are several parts having those who are interested in here get evolved in this project  easily.
> ##  packageNeeded:

- ## Package needed for database:
![database](https://github.com/UnCarter25le/Tripresso/blob/master/packageNeededForDatabase.png)


- ## Package needed for crawler:
![crawler](https://github.com/UnCarter25le/Tripresso/blob/master/packageNeededForCrawler.png)


> ##  Project Overview: 

![ProjectOverview](https://github.com/UnCarter25le/Tripresso/blob/master/ProjectOverview.png)

- ## DatabaseInfo: 
This is the place showing us information about database(MySQL), such as each table condition, ERmodel for Tripresso [website](https://www.tripresso.com/agency/NEWAMAZE "旅遊咖x新魅力"),the overview for database named __"tripresso"__,and back-up file named __"back_tripresso.sql"__ for corresponding database.

- ## DataSetAndPrograms:
    - this is the place showing us details concerning executable programs and usable dataset. For example, it would take us about __1200 seconds__ to executing __"crawlerForNewAmazing.py"__ and __"crawlerForOrangeTour.py"__, which will generate raw data in html-txt format and download photos for follow-up data processing. It will be help to __reduce precious time__ by leaving comments at lines __"photoUri and photoDownload..."__:
```
若不要下載圖片，請在下面一組if else中註解掉photoUri and photoDownload。 圖片有部屬在不同的網域中。。。
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
```

    - Also, I have default pages from 1 to 10, and we are able to adjust it to the effective range!
```
for page in range(1,11):
    crawler(page,url)
```

    - Next, we are capable of downloading photos alternatively by executing __"photoForNewAmazing.py"__ and __"photoForOrangeTour.py"__ to have those if we have done jobs of getting raw data(checking the folder named __crawlerForNewamazing__ and __crawlerForOrangetour__.) __Look, if completing photos download at the initial stage, we can neglect this part!__
    - Fourthly, after removing possible duplicates in data set, we have to rely on files to give us a favor to insert data into database, such as __"newAmazing_199_SET.json"__,__"DateOf2019.json"__,__"orangetour_200.json"__,__"photoForNewamazing_SET"__,__"photoForOrangetour"__. I believe it's time to checking us MySQL account information!
![MySQL account](https://github.com/UnCarter25le/Tripresso/blob/master/pleaseCheckAccountInfoForMySQL.png)

    - Finally, before executing two files,__"createTables.py"__ and __"dataInsert.py"__ to have data into database, please create  a database named __"tripresso"__ and it's format must be compatiable utf8mb4! If we get ready for executing two files, we can just do it now.
    
    - __NOTE: we can directly use back-up file named  "back_tripresso.sql" to import data immediately. Of course, creating database named "tripresso" is necessary.__ 

- ## PhotoSet:

    - Here is notes for making crawlers.
- ## iPYNB_File:

    - Here is my work places.
    
    
>  ## Database Info: 

- ## I believe these photos will help us to take a closer look at how is going on in executing programs:

    - ERmodel for Tripresso [website](https://www.tripresso.com/agency/NEWAMAZE "旅遊咖x新魅力")
![ERmodel for Tripresso website](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/TripressoERmodel.png)

    - Database overview:
![database overview](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/databaseOverview.png)

    - table_Continent:
![--](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/table_Continent.png)
    
    - table_Country:
![--](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/table_Country.png)
    
    - table_Date:
![--](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/table_Date.png)

    - table_Date_And_TripPlan:
![--](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/table_Date_And_TripPlan.png)

    - table_Evaluation_Of_PartnerCorp:
![--](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/table_Evaluation_Of_PartnerCorp.png)

    - table_Giveaway:
![--](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/table_Giveaway.png)

    - table_PartnerCorp:
![--](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/table_PartnerCorp.png)

    - table_TripPlan:
![--](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/table_TripPlan.png)

    - table_WowFactor:
![--](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/table_WowFactor.png)

    - table_WowFactor_And_TripPlan:
![--](https://github.com/UnCarter25le/Tripresso/blob/master/DatabaseInfo/table_WowFactor_And_TripPlan.png)

 
-----


# Finally, for me:)


it's not until completing this mission that I have this chance to sharpen my skills further more as to web scraping, functional programming style, and entity relationship modeling.I wish those who are watching this project now will be moved by __my industrious attitude.__
