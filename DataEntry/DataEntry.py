import MySQLdb

class DataEntry:  

    def __init__(self, myHost, myUser, myPasswd, myDb):
        self.db=MySQLdb.connect(host=myHost,user=myUser,
        passwd=myPasswd,db=myDb)

        self.c=self.db.cursor()

    def createInsertQuery(self, table, arg):
        try:
            query = "INSERT INTO " + table + " VALUES ("
            for x in arg:
                query += x + ","
            query = query[:-1]
            query += ')'
        except:
            pass

        print(query)
        return query
    
    def close(self):
        self.db.close() 

    def getTable(self, table):
        self.c.execute("SELECT * FROM " + table)
        return self.c.fetchall()
    
    def insertData(self, table, data):
        arg = []
        print("Splitting data")
        for n in data:
            print("Got data: " + n) 
            arg.append(n)
            
        try:
            print("Creating query")
            self.c.execute(self.createInsertQuery(table,arg))
            self.db.commit()
            return True
        except:
            self.db.rollback()
        return False
        
