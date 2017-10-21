import MySQLdb
from DataEntry import DataEntry

class DbManager:
    def __init__(self, myHost, myUser, myPasswd, myDb):
        
        self.db=MySQLdb.connect(host=myHost,user=myUser,
        passwd=myPasswd,db=myDb)

        self.c=self.db.cursor()
        self.mydb = myDb
        self.db = DataEntry(myHost, myUser, myPasswd, myDb)
        self.deviceTable = "Devices"
        self.addressTable = "Addresses"

    def getTables(self):
        try:
            self.c.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                           + "WHERE TABLE_TYPE = 'BASE TABLE' "
                           + "AND TABLE_SCHEMA='" + self.mydb + "'")
            return self.c.fetchall()
        except:
            pass
        
    def decodeID(self, deviceID):
        try:
            self.c.execute("SELECT `Table Name` FROM `" + self.deviceTable + "` WHERE "
                           + "`Device ID` = " + `deviceID`)
            return self.c.fetchall()[0][0]
        except:
            pass      

    def getDevices(self):
        try:
            self.c.execute("SELECT `Table Name` FROM `" + self.deviceTable + "`")
            return self.c.fetchall()
        except:
            pass
        
        
    def getSensorCount(self, deviceName):
        try:
            self.c.execute("SELECT Count(*) FROM `" + self.addressTable + "` WHERE "
                           + "`Table Name` = \"" + deviceName + "\"")
            return self.c.fetchall()[0][0]
        except:
            pass

    def tableExists(self,tables,device):
        if(any(device in x for x in tables)):
            return True
        else:
            return False



    def createTable(self,tableName, numSensors):
        
        query = "CREATE TABLE `" + tableName + "` (`TimeStamp` timestamp, "

        for i in range(0, numSensors):
            query += "`Sensor" + `(i+1)` + "` double,"
        query = query[:-1]
        query += ');'

        try:
            self.c.execute(query)
            return True
        except:
            return False

    def insertData(self, deviceID, numSensors, data):
        table = self.decodeID(deviceID)
        if(not self.tableExists(self.getTables(), table)):
            print("Creating Table")
            if(not self.createTable(table, numSensors)):
                print("Table Creation Failed")
        if(self.db.insertData(table, data)):
            return True
        else:
            return False
         

    
