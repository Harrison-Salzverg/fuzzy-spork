class InMemoryDatabase:
    def __init__(self):
        self.data = {}  # Main data store for keys and values
        self.transaction_in_progress = False
        self.transaction_data = {}  # Store changes made during a transaction

    def begin_transaction(self):
        if self.transaction_in_progress:
            raise Exception("Transaction already in progress")
        self.transaction_in_progress = True
        self.transaction_data = {}

    def put(self, key, value):
        if not self.transaction_in_progress:
            raise Exception("No transaction in progress")
        
        self.transaction_data[key] = value

    def get(self, key):
        if key in self.transaction_data:
            return self.transaction_data[key]
        return self.data.get(key, None)

    def commit(self):
        if not self.transaction_in_progress:
            raise Exception("No transaction in progress")
        
        self.data.update(self.transaction_data)
        self.transaction_data = {}
        self.transaction_in_progress = False

    def rollback(self):
        if not self.transaction_in_progress:
            raise Exception("No transaction in progress")
        
        self.transaction_data = {}
        self.transaction_in_progress = False


#Example usage:
db = InMemoryDatabase()

#Set up initial key-value pairs
db.begin_transaction()
db.put("a", 10)
db.put("b", 20)
db.commit()

#Begin a transaction
db.begin_transaction()
db.put("a", 30)
db.put("c", 40)

#Changes made during the transaction are not visible
print(db.get("a"))  # Output: 10
print(db.get("c"))  # Output: None

#Commit the transaction
db.commit()

#Changes made during the transaction are now visible
print(db.get("a"))  #Output: 30
print(db.get("c"))  #Output: 40

#Another transaction
db.begin_transaction()
db.put("b", 50)
db.put("d", 60)

#Rollback this transaction
db.rollback()

#Changes made during the transaction are discarded
print(db.get("b"))  #Output: 20
print(db.get("d"))  #Output: None