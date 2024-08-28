import file_manager

def range_generator(locationX1, locationY1, locationX2, locationY2):
    mapFileList = []

    for x in range(locationX1, locationX2+1):
        for y in range(locationY1, locationY2+1):
            mapFileList.append(f"{x}_{y}")

    return mapFileList

def chunks_by_range(chunkOne, chunkTwo, file_name):
    chunkFiles = file_manager.ZomboidChunks()
    locationX1, locationY1 = map(int, chunkOne.split("_"))
    locationX2, locationY2 = map(int, chunkTwo.split("_"))

    range = range_generator(locationX1, locationY1, locationX2, locationY2)

    if file_name:
        chunkFiles.chunk_list_to_file(range, file_name)
    else:
        chunkFiles.delete_chunks(range)

def chunks_by_file(file):
    chunkFiles = file_manager.ZomboidChunks()
    rangeList = []

    with file as openFile:
        fileContents = openFile.read()
    rangeList = list(filter(None, fileContents.split("\n")))

    chunkFiles.delete_chunks(rangeList)