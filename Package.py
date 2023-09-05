class Package:
    #Constructor for a Package object with extra variable for the time departed and time delivered
    def __init__(self, ID, address,city,state,zip,deadline, weight):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.time_delivered = None
        self.time_departed = None

    #Provides the status of a package at a given input time
    def status_at_time(self,input_time):
        if self.time_departed > input_time:
            return f"ID:{self.ID}, Address: {self.address}, City: {self.city}, State: {self.state}, ZIP: {self.zip}, Deadline: {self.deadline}, Weight: {self.weight}, Status: At Hub"
        elif self.time_delivered > input_time:
            return f"ID:{self.ID}, Address: {self.address}, City: {self.city}, State: {self.state}, ZIP: {self.zip}, Deadline: {self.deadline}, Weight: {self.weight}, Status: In Route"
        else:
            return f"ID:{self.ID}, Address: {self.address}, City: {self.city}, State: {self.state}, ZIP: {self.zip}, Deadline: {self.deadline}, Weight: {self.weight}, Status: Delivered at {self.time_delivered}"