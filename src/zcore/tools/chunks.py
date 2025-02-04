from tools.file_manager import ZomboidChunks

def build_coordinate_list(coordX1, coordY1, coordX2, coordY2):
    coordinateList = []

    for x in range(coordX1, coordX2+1):
        for y in range(coordY1, coordY2+1):
            coordinateList.append(f"{x}_{y}")

    return coordinateList

def generate_chunk_list_from_range(chunkOne, chunkTwo):
    locationX1, locationY1 = map(int, chunkOne.split("_"))
    locationX2, locationY2 = map(int, chunkTwo.split("_"))

    rangeList = build_coordinate_list(
        locationX1,
        locationY1,
        locationX2,
        locationY2
    )

    return rangeList

def delete_chunks_from_file(fileObject):
    chunkFiles = ZomboidChunks()
    rangeList = chunkFiles.get_chunks_from(fileObject)
    chunkFiles.delete_chunks(rangeList)

def create_chunk_list_file(chunkOne, chunkTwo, fileName):
    rangeList = generate_chunk_list_from_range(chunkOne, chunkTwo)
    ZomboidChunks().chunk_list_to_file(rangeList, fileName)

def delete_chunks_from_given_range(chunkOne, chunkTwo):
    rangeList = generate_chunk_list_from_range(chunkOne, chunkTwo)
    ZomboidChunks().delete_chunks(rangeList)