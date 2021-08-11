import sqlite3

dataDictionary = [
{"ID": 17, "CODE": "SBK07", "NAME": "Surian", "TYPE": "Elevated" },
{"ID": 18, "CODE": "SBK08", "NAME": "Mutiara Damansara", "TYPE": "Elevated" },
{"ID": 19, "CODE": "SBK09", "NAME": "Bandar Utama", "TYPE": "Elevated" },
{"ID": 20, "CODE": "SBK10", "NAME": "TTDI", "TYPE": "Elevated" },
{"ID": 25, "CODE": "SBK12", "NAME": "Phileo Damansara", "TYPE": "Elevated" },
{"ID": 26, "CODE": "SBK13", "NAME": "Pusat Bandar Damansara", "TYPE": "Elevated" },
{"ID": 27, "CODE": "SBK14", "NAME": "Semantan", "TYPE": "Elevated" },
{"ID": 29, "CODE": "SBK15", "NAME": "Muzium Negara", "TYPE": "Underground" },
{"ID": 30, "CODE": "SBK16", "NAME": "Pasar Seni", "TYPE": "Underground" },
{"ID": 31, "CODE": "SBK17", "NAME": "Merdeka", "TYPE": "Underground" },
{"ID": 33, "CODE": "SBK18A", "NAME": "Bukit Bintang", "TYPE": "Underground" }
]

def insert_data(cursor, tableName, dataDictionary):
	insertQuery = f'''INSERT OR IGNORE INTO {tableName} VALUES ({dataDictionary["ID"]}, '{dataDictionary["CODE"]}', '{dataDictionary["NAME"]}', '{dataDictionary["TYPE"]}'); '''
	cursor.execute(insertQuery)
	if cursor.rowcount:
		print("Record inserted successfully into table ", cursor.rowcount)


try:
	dbConnection = sqlite3.connect('1704367_UECS3123_Assignment_May2021.sqlite')
	cursor = dbConnection.cursor()
	print("Database connected successfully")

	createQuery = '''
	CREATE TABLE IF NOT EXISTS stations(
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	CODE VARCHAR(10) NOT NULL,
	NAME VARCHAR(69) NOT NULL,
	TYPE VARCHAR(20) NOT NULL);
	'''

	cursor.execute(createQuery)

	print("Inserting data:")
	for data in dataDictionary:
		insert_data(cursor, 'stations', data)

	cursor.close()

except sqlite3.Error as error:
	print("Error in connecting to the database", error)

finally:
	dbConnection.commit()
	dbConnection.close()