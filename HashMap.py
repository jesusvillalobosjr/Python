class HashMap:
    #Constructor for a hashmap with size of the given capacity
    def __init__(self,capacity):
        self.capacity = capacity
        self.list = []

        for i in range(capacity):
            self.list.append([])

    #Inserting an object into the hashtable, as well as replacing values with duplicate keys.
    def insert(self,key,value):
        list_index = hash(key) % self.capacity
        index_bucket = self.list[list_index]

        for i in range(index_bucket.__len__()):
            if index_bucket[i].ID == key:
                index_bucket[i] = value
                return
        
        index_bucket.append(value)

    #Lookup and return a package object based on the given input key.
    def lookup(self,key):
        list_index = hash(key) % self.capacity
        bucket = self.list[list_index]
        for item in bucket:
            if key == item.ID:
                return item
        return False

    def __str__(self):
        return f"{self.list}"