# MongoDB Exercises and PyMongo

### Example about nested arrays, dicts and a combination of both.
```json
{
  "name": "Juan Pérez",
  "age": 30,
  "address": {
    "street": "Calle Falsa",
    "number": 123,
    "city": "Madrid",
    "postal_code": "28013"
  },
  "phones": ["+34 600 123 456", "+34 600 654 321"],
  "projects": [
    {
      "name": "Project Alpha",
      "description": "Software development",
      "hours_worked": 120
    },
    {
      "name": "Project Beta",
      "description": "Database implementation",
      "hours_worked": 80
    }
  ],
  "skills": ["Python", "MongoDB", "Data Analysis"]
}
```

### 1. Find a Document by a Non-Nested Field Using $eq, $gt, or $lt

#### MongoDB Query
```json
db.employees.find({ "age": { "$gt": 25 } })
```

#### PyMongo Version
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.company
result = db.employees.find({ "age": { "$gt": 25 } })
for doc in result:
    print(doc)
```

### 2. Find a Document by a Nested Field Using $in and $exists

#### MongoDB Query
```json
db.employees.find({ "projects.name": { "$in": ["Project Alpha"] }, "address.postal_code": { "$exists": true } })
```

#### PyMongo Version
```python
result = db.employees.find({ "projects.name": { "$in": ["Project Alpha"] }, "address.postal_code": { "$exists": true } })
for doc in result:
    print(doc)
```

### 3. Insert a New Document

#### MongoDB Query
```json
db.employees.insertOne({
  "name": "Maria Garcia",
  "age": 28,
  "address": {
    "street": "Avenida Siempre Viva",
    "number": 742,
    "city": "Barcelona",
    "postal_code": "08001"
  },
  "phones": ["+34 600 789 012", "+34 600 987 210"],
  "projects": [
    {
      "name": "Project Gamma",
      "description": "Data analysis",
      "hours_worked": 100
    }
  ],
  "skills": ["SQL", "R", "Data Visualization"]
})
```

#### PyMongo Version
```python
new_employee = {
  "name": "Maria Garcia",
  "age": 28,
  "address": {
    "street": "Avenida Siempre Viva",
    "number": 742,
    "city": "Barcelona",
    "postal_code": "08001"
  },
  "phones": ["+34 600 789 012", "+34 600 987 210"],
  "projects": [
    {
      "name": "Project Gamma",
      "description": "Data analysis",
      "hours_worked": 100
    }
  ],
  "skills": ["SQL", "R", "Data Visualization"]
}
db.employees.insert_one(new_employee)
```

### 4. Update a Non-Nested Field

#### MongoDB Query
```json
db.employees.updateOne({ "name": "Juan Pérez" }, { "$set": { "age": 31 } })
```

#### PyMongo Version
```python
db.employees.update_one({ "name": "Juan Pérez" }, { "$set": { "age": 31 } })
```

### 5. Update a Nested Field

#### MongoDB Query
```json
db.employees.updateOne({ "name": "Juan Pérez" }, { "$set": { "address.city": "Sevilla" } })
```

#### PyMongo Version
```python
db.employees.update_one({ "name": "Juan Pérez" }, { "$set": { "address.city": "Sevilla" } })
```

### 6. Aggregation Query to Calculate the Sum or Average of a Numerical Field

#### MongoDB Query
```json
db.employees.aggregate([
  { "$unwind": "$projects" },
  { "$group": { "_id": "$name", "total_hours_worked": { "$sum": "$projects.hours_worked" } } }
])
```

#### PyMongo Version
```python
pipeline = [
  { "$unwind": "$projects" },
  { "$group": { "_id": "$name", "total_hours_worked": { "$sum": "$projects.hours_worked" } } }
]
result = db.employees.aggregate(pipeline)
for doc in result:
    print(doc)
```

### 7. Aggregation Query to Calculate the Max or Min of a Numerical Field in a Nested Field

#### MongoDB Query
```json
db.employees.aggregate([
  { "$unwind": "$projects" },
  { "$group": { "_id": "$name", "max_hours_worked": { "$max": "$projects.hours_worked" } } }
])
```

#### PyMongo Version
```python
pipeline = [
  { "$unwind": "$projects" },
  { "$group": { "_id": "$name", "max_hours_worked": { "$max": "$projects.hours_worked" } } }
]
result = db.employees.aggregate(pipeline)
for doc in result:
    print(doc)
```

### 8. Remove All Elements in a Collection Matching a Certain Criteria

#### MongoDB Query
```json
db.employees.deleteMany({ "age": { "$lt": 25 } })
```

#### PyMongo Version
```python
db.employees.delete_many({ "age": { "$lt": 25 } })
```

### 9. Completely Remove a Collection

#### MongoDB Query
```json
db.employees.drop()
```

#### PyMongo Version
```python
db.employees.drop()
```
