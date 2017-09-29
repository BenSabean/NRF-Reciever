import MySQLdb

class DbManager:
    def __init__(self, myHost, myUser, myPasswd, myDb):
        
        self.db=MySQLdb.connect(host=myHost,user=myUser,
        passwd=myPasswd,db=myDb)

        self.c=self.db.cursor()
        self.mydb = myDb
        self.deviceTable = "Devices"

    def GetTables(self):
        try:
            self.c.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                           + "WHERE TABLE_TYPE = 'BASE TABLE' "
                           + "AND TABLE_SCHEMA='" + self.mydb + "'")
            return self.c.fetchall()
        except:
            pass

    def GetDevices(self):
        try:
            self.c.execute("SELECT `Table Name` FROM `" + self.deviceTable + "`")
            return self.c.fetchall()
        except:
            pass

    def TableExists(self,tables,device):
        if(any(device in x for x in tables)):
            return True
        else:
            return False
'''
    def createTable(self,tablename,db):
        try:
      
'''      
    def run(self):
        #while True:
        devices = self.GetDevices()

        for row in devices:
            if(!self.TableExists(self.GetTables(), row)):
                
      
    
