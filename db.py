import json
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database',
    port=3306
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS buildings (
    accountId INT PRIMARY KEY,
    isCommercial BOOLEAN,
    address TEXT,
    buildingType VARCHAR(100),
    roomsCount INT,
    residentsCount INT,
    totalArea FLOAT,
    consumption JSON,
    prediction FLOAT
)
""")

with open('dataset_train.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for entry in data:
    accountId = entry.get("accountId")
    isCommercial = entry.get("isCommercial", False)
    address = entry.get("address", "")
    buildingType = entry.get("buildingType", "")
    roomsCount = entry.get("roomsCount")
    residentsCount = entry.get("residentsCount")
    totalArea = entry.get("totalArea")
    consumption = json.dumps(entry.get("consumption", {}), ensure_ascii=False)
    prediction = 1.0 if isCommercial else 0.0

    cursor.execute("""
        INSERT INTO buildings (
            accountId, isCommercial, address, buildingType,
            roomsCount, residentsCount, totalArea, consumption, prediction
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            isCommercial=VALUES(isCommercial),
            address=VALUES(address),
            buildingType=VALUES(buildingType),
            roomsCount=VALUES(roomsCount),
            residentsCount=VALUES(residentsCount),
            totalArea=VALUES(totalArea),
            consumption=VALUES(consumption),
            prediction=VALUES(prediction)
    """, (accountId, isCommercial, address, buildingType,
          roomsCount, residentsCount, totalArea, consumption, prediction))

conn.commit()

cursor.close()
conn.close()
