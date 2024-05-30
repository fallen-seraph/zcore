from tools.linux_files import LinuxFiles

def range_generator(locationX1, locationY1, locationX2, locationY2):
    mapFileList = []

    for x in range(locationX1, locationY1+1):
        for y in range (locationX2, locationY2+1):
            mapFileList.append(f"map_{str(x)}_{str(y)}.bin")

    return mapFileList

def chunks_by_range(chunkOne, chunkTwo, file_name):
    locationX1, locationY1 = map(int, chunkOne.split("_"))
    locationX2, locationY2 = map(int, chunkTwo.split("_"))

    range = range_generator(locationX1, locationY1, locationX2, locationY2)

    if file_name:
        LinuxFiles.chunks_to_file(range, file_name)
    else:
        LinuxFiles.delete_chunks(range)

def chunks_by_file(file):
    rangeList = []

    with open(file) as openFile:
        fileContents = openFile.read()
    rawList = list(filter(None, fileContents.split("\n")))
    for x in rawList:
        rangeList.append(f"map_{x}.bin")

    LinuxFiles.delete_chunks(rangeList)