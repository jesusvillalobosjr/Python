from Truck import Truck
from Package import Package
from HashMap import HashMap
from datetime import timedelta
from sys import maxsize
import csv

#Open CSV file to read to find distances and turn it into a list in order to access the information by indexes
with open('DistanceTable.csv','r',encoding='utf-8-sig') as distance_csv:
    #Read CSV file, turn it into a list and store it in a variable.
    distance_csv_reader = list(csv.reader(distance_csv))

#Function to find distance between locations given indexes.
def find_distance(row,column):
    distance = distance_csv_reader[row][column]
    if(distance == ''):
        distance = distance_csv_reader[column][row]
    return float(distance)

#Function to input all packages into a hashtable with the key being their ID keeping them unique.
def insert_package_info(package_file, hashTable):
    with open(package_file,'r',encoding='utf-8-sig') as package_information:
        package_iterator = list(csv.reader(package_information))
        for package in package_iterator:
            package_id = int(package[0])
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zip = package[4]
            package_deadline = package[5]
            package_weight = package[6]
            insert = Package(package_id,package_address,package_city,package_state,package_zip,package_deadline,package_weight)
            hashTable.insert(package_id,insert)

#Open a csv file that maps the string address into a numbered index to facilitate the use of addresses
with open('AddressToIndex.csv','r',encoding='utf-8-sig') as address_csv:
    address_to_index = list(csv.reader(address_csv))

#Using our address_to_index we return an index based on the string address
def index_for_address(address):
    for address_in_file in address_to_index:
        if(address == address_in_file[2]):
            return int(address_in_file[0])

#Function to load truck based on the array of ID's given in the truck object's packages array
def load_truck(truck):
    packages_to_be_loaded = []
    for package_id in truck.packages:
        package_to_load = hashtable.lookup(package_id)
        package_to_load.time_departed = truck.time
        packages_to_be_loaded.append(package_to_load)
    truck.packages = packages_to_be_loaded

#Deliver packages until the array of packages is empty
def deliver(truck):
    packages = truck.packages
    while packages.__len__() != 0:
        next_address = maxsize
        time_to_destination = 0
        next_package = None
        for package in packages:
            distance = find_distance(index_for_address(package.address),index_for_address(truck.current_address))
            if distance < next_address:
                next_address = distance
                next_package = package
        time_to_destination = next_address/truck.speed
        truck.time += timedelta(hours=time_to_destination)
        truck.mileage += next_address
        truck.current_address = next_package.address
        next_package.time_delivered = truck.time
        packages.remove(next_package)


#Create hashmap and insert all packages, the key being the package ID and the value being the packet object
hashtable = HashMap(20)
insert_package_info('PackageFile.csv',hashtable)

#Instantiate first truck object and pass in an array based on the packages deadlines, in this case the earliest deadlines
first_truck = Truck(16,18,0.0,[1,2,7,10,13,14,15,16,19,20,29,30,31,34,37,40],'4001 South 700 East',timedelta(hours=8))

#Instantiate second truck object with packages that were required to be on the second truck and other packages.
second_truck = Truck(16,18,0.0,[3,4,5,6,11,17,18,22,23,24,25,28,32,33,36,38],'4001 South 700 East',timedelta(hours=9,minutes=5))

#Load first 2 trucks with the actual package objects
load_truck(first_truck)
load_truck(second_truck)

#Deliver the first and second truck
deliver(first_truck)
deliver(second_truck)

#Instantiate third truck with the remaining packages including the one with the incorrect address and getting the time for the 
#driver that finishes first
third_truck = Truck(16,18,0.0,[8,9,12,21,26,27,35,39],'4001 South 700 East',min(first_truck.time,second_truck.time))

#Load final truck
load_truck(third_truck)

#Deliver final truck
deliver(third_truck)


class Main:
    #Student Name: Jesus Villalobos Jr
    #Student ID: 010610245
    print("Western Governers University Parsel System Routing Program \n")
    print("The following is the total mileage for all three trucks")
    print(f"Truck 1: {round(first_truck.mileage,2)} miles, Truck 2: {round(second_truck.mileage,2)} miles, Truck 3: {round(third_truck.mileage,2)} miles \n")

    #Get input for user to specify if they would like to view a specific package or all packages, if invalid output is set the program will exit
    packet_input = input("If you would like to look up an individual packet type 'single', if if you would like to look up every package type 'all', anythin else will cause program to end. \nEnter here: ")
    if packet_input.lower() == 'single':
        try:
            single_ID = input('Enter ID for package: ')

            #Get package based on ID selected by User
            package = hashtable.lookup(int(single_ID))
            
            #Get time from the user
            time_status = input('Enter time in hours,minutes,seconds(include commas) : ')
            time_status = time_status.split(',')
            time_status = timedelta(hours=int(time_status[0]),minutes=int(time_status[1]),seconds=int(time_status[2]))

            #Print package information at time given by the user
            if(package):
                print(package.status_at_time(time_status))
            else:
                print("Invalid ID, please start program again.")
                exit()
        except ValueError:
            #If proper ID or time wasn't selected the program will exit
            print("Invalid date, please start program again.")
            exit()
    elif(packet_input.lower() == 'all'):
        try:
            #Get time from the user
            time_status = input('Enter time in hours,minutes,seconds(include commas) : ')
            time_status = time_status.split(',')
            time_status = timedelta(hours=int(time_status[0]),minutes=int(time_status[1]),seconds=int(time_status[2]))

            #Print out information for all packets at time given by the use
            for i in range(1,41):
                package = hashtable.lookup(int(i))
                print(package.status_at_time(time_status))

        except ValueError:
            #If proper ID or time wasn't selected the program will exit
            print("Invalid time, please start program again.")
            exit()
    else:
        print("Invalid input, please start program again.")
        exit()