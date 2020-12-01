# this will be used for helper functions
import json

# read data from json file
def readFromJson(fileName):
    # print("read json file")
    with open(fileName) as f:
        data = json.load(f)
        print("data from json file",data)
        return data

# write data to json file
def writeToJson(fileName, data):
    # print("write to json file",data)
    with open(fileName, 'w') as json_file:
        json.dump(data, json_file)
        # print("Done")
