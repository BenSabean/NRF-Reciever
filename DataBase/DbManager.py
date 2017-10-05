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

    def GetTables(self):
        try:
            self.c.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                           + "WHERE TABLE_TYPE = 'BASE TABLE' "
                           + "AND TABLE_SCHEMA='" + self.mydb + "'")
            return self.c.fetchall()[0]
        except:
            pass
        
    def DecodeID(self, deviceID):
        try:
            self.c.execute("SELECT `Table Name` FROM `" + self.deviceTable + "` WHERE "
                           + "`Device ID` = " + `deviceID`)
            return self.c.fetchall()[0][0]
        except:
            pass      

    def GetDevices(self):
        try:
            self.c.execute("SELECT `Table Name` FROM `" + self.deviceTable + "`")
            return self.c.fetchall()
        except:
            pass
        
        
    def GetSensorCount(self, deviceName):
        try:
            self.c.execute("SELECT Count(*) FROM `" + self.addressTable + "` WHERE "
                           + "`Table Name` = \"" + deviceName + "\"")
            return self.c.fetchall()[0][0]
        except:
            pass

    def TableExists(self,tables,device):
        if(any(device in x for x in tables)):
            return True
        else:
            return False



    def CreateTable(self,tableName, numSensors):
        
        query = "CREATE TABLE `" + tableName + "` (`TimeStamp` timestamp, "

        for i in range(0, numSensors):
            query += "`Sensor" + `(i+1)` + "` double,"
        query = query[:-1]
        query += ');'

        print(query)

        try:
            self.c.execute(query)
            return True
        except:
            return False

    def InsertData(self, deviceID, numSensors, data):
        table = self.DecodeID(deviceID)
        if(not self.TableExists(self.GetTables(), table)):
            self.CreateTable(table, numSensors)
        if(self.db.insertData(table, data)):
            return True
        else:
            return False
         

    
