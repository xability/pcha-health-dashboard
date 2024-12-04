import pandas as pd
from pymongo import MongoClient

# Cosmos DB connection details
connection_string = "mongodb://pcha:DBQWfFLdaAwofXET3QyLDt1ndCAbJdGwoq8iF4u79P2A0QArmODzkbENAMqtobHZOhDn765q2dlmACDbeuMcHg==@pcha.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@pcha@"
                
client = MongoClient(connection_string, tlsAllowInvalidCertificates=True)

db = client['pcha_db']
collection = db['health_data']

# user_id = "001241.6ef3475d9ab64f6f8ff3e3d2c4bd3a68.1716"
# user_id = "000437.0325043b95b0433d9c66b7a67c7d794b.2014"
# cursor = collection.find({"user_id": user_id})


cursor = collection.find()

# Flatten the data
flattened_data = []

for document in cursor:
    _id = document["_id"]
    user_id = document["user_id"]
    for date_entry in document["dates"]:
        flattened_entry = {"_id": _id, "user_id": user_id, "date": date_entry["date"]}
        for key, value in date_entry["data"].items():
            flattened_entry[key] = value["value"]
        flattened_data.append(flattened_entry)

# Convert to DataFrame
df = pd.DataFrame(flattened_data)

# Write the DataFrame to a CSV file
csv_filename = "healthdata.csv"
df.to_csv(csv_filename, index=False)

print(f"Data has been written to {csv_filename}")