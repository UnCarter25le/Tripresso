#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymysql

#1
SQL_PartnerCorp = """CREATE TABLE PartnerCorp(

partner_id mediumint primary key,
partnerName nvarchar(20) Unique default Null,
partnerIntro  nvarchar(300) Not Null default "None"
)"""

#2
SQL_Giveaway = """CREATE TABLE Giveaway(

giveaway_id smallint primary key,
giveaway JSON default null
)"""

#3
SQL_Continent = """CREATE TABLE Continent(

continent_id tinyint primary key,
continent nvarchar(5) Not Null default "None"
)"""

#4
SQL_TripPlan = """CREATE TABLE TripPlan(
plan_id int primary key auto_increment,
partner_id mediumint,
giveaway_id smallint,
continent_id tinyint,
tripPlanCodeName char(12) Unique default Null,
tripPlan  nvarchar(100) Not Null default "None",
days tinyint Not Null default 0,
introPhoto MEDIUMBLOB,
dateOfDeparture Date default Null,
expense  decimal(10) Not Null default 0,
discount  decimal(6) Not Null default 0,
domainUrl varchar(40) Not Null default "None",
imgUrn varchar(100) Not Null default "None",
tripUrn varchar(65) Not Null default "None",

Constraint TripPlan2PartnerCorp foreign key(partner_id)
references PartnerCorp(partner_id) 
ON UPDATE CASCADE ON DELETE CASCADE,

Constraint TripPlan2Giveaway foreign key(giveaway_id)
references Giveaway(giveaway_id) 
ON UPDATE CASCADE ON DELETE CASCADE,

Constraint TripPlan2Continent foreign key(continent_id)
references Continent(continent_id) 
ON UPDATE CASCADE ON DELETE CASCADE
)"""

#5
SQL_Evaluation_Of_PartnerCorp = """CREATE TABLE Evaluation_Of_PartnerCorp(

evaluation_id mediumint primary key auto_increment,
partner_id mediumint,
plan_id int,
schedule tinyint Not Null default 0,
serviceOfTourGuide tinyint Not Null default 0,
meals  tinyint Not Null default 0,
accomodation tinyint Not Null default 0,
vehicle tinyint Not Null default 0,
responseFromCustomer nvarchar(500) Not Null default "None",
dateOfResponse Date  default Null,
response nvarchar(500) Not Null default "None",

Constraint Evaluation2PartnerCorp foreign key(partner_id)
references PartnerCorp(partner_id) 
ON UPDATE CASCADE ON DELETE CASCADE,

Constraint Evaluation2TripPlan foreign key(plan_id)
references TripPlan(plan_id) 
ON UPDATE CASCADE ON DELETE CASCADE
)"""

#6
SQL_Country = """CREATE TABLE Country(

province_or_county_id  smallint primary key,
continent_id tinyint,
countryName nvarchar(10) Not Null default "None",
nameOfProvinceOrCounty nvarchar(10) Not Null default "None",
region nvarchar(10) Not Null default "None",

Constraint Country2Continent foreign key(continent_id)
references Continent(continent_id) 
ON UPDATE CASCADE ON DELETE CASCADE
)"""

#7
SQL_Date = """CREATE TABLE Date(

date_id smallint primary key auto_increment,
date Date default Null
)"""

#8
SQL_WowFactor = """CREATE TABLE WowFactor(

wow_id tinyint primary key,
wowFactor nvarchar(10) Unique default Null,
wowDescription nvarchar(100) Not Null default "None"
)"""

#9PRIMARY KEY (plan_id,date_id),
SQL_Date_And_TripPlan = """CREATE TABLE Date_And_TripPlan(
_id int primary key auto_increment,
plan_id int,
date_id smallint,
availableNumber smallint Not Null default 0,
totalNumber smallint Not Null default 0,
readyToGo boolean default False,
terminate boolean default False,

Constraint 1_Date_And_TripPlan foreign key(plan_id)
references TripPlan(plan_id)
ON UPDATE CASCADE ON DELETE CASCADE,

Constraint 2_Date_And_TripPlan foreign key(date_id)
references Date(date_id)
ON UPDATE CASCADE ON DELETE CASCADE
)"""

#10PRIMARY KEY(plan_id,wow_id),
SQL_WowFactor_And_TripPlan = """CREATE TABLE WowFactor_And_TripPlan(
_id int primary key auto_increment,
plan_id int,
wow_id tinyint,

Constraint 1_WowFactor_And_TripPlan foreign key(plan_id)
references TripPlan(plan_id) 
ON UPDATE CASCADE ON DELETE CASCADE,

Constraint 2_WowFactor_And_TripPlan foreign key(wow_id)
references WowFactor(wow_id) 
ON UPDATE CASCADE ON DELETE CASCADE
)"""

if __name__ == '__main__':
    
    conn = pymysql.connect('localhost',user='root',passwd='admin',port=3306,db='tripresso',charset='utf8')

    tableArray = ["PartnerCorp",                  "Giveaway",                  "Continent",                  "TripPlan",                  "Evaluation_Of_PartnerCorp",                  "Country",                  "Date",                  "WowFactor",                  "Date_And_TripPlan",                  "WowFactor_And_TripPlan"]
    #把表格除掉。
    for tableName in tableArray:
        with conn.cursor() as cursor:
            cursor.execute("SET foreign_key_checks = 0")
            cursor.execute("DROP TABLE if exists {}".format(tableName))
            cursor.execute("SET foreign_key_checks = 1")

    SQLArray = [SQL_PartnerCorp,                SQL_Giveaway,                SQL_Continent,                SQL_TripPlan,                SQL_Evaluation_Of_PartnerCorp,                SQL_Country,                SQL_Date,                SQL_WowFactor,                SQL_Date_And_TripPlan,                SQL_WowFactor_And_TripPlan]
    #新建表格。
    for SQLTable in SQLArray:
        with conn.cursor() as cursor:
            cursor.execute(SQLTable)

    conn.close()

