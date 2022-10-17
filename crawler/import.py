inF = open("flight_data.txt")
data = inF.read()
dataArray = data.split("\n\nseperator\n\n")
print(len(dataArray))