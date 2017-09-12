from DataEntry import DataEntry

deviceID = 1
table = "HotWaterTank"
db = DataEntry("127.0.0.1", "root", "Sabean456", "AER-Data")
data = ["NULL", "17.3", "20.2", "21.3", "20.1", "19.4"]


if(db.insertData(deviceID, table, data)):
    print("Inserted Data")

else:
    print("Failed to insert data")

        
