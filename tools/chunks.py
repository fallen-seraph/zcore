from tools.linux_files import LinuxFiles

def range_generator(locationX1, locationY1, locationX2, locationY2):
    mapFileList = []

    for x in range(locationX1, locationX2+1):
        for y in range(locationY1, locationY2+1):
            mapFileList.append(f"{x}_{y}")

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

    with file as openFile:
        fileContents = openFile.read()
    rangeList = list(filter(None, fileContents.split("\n")))

    LinuxFiles.delete_chunks(rangeList)