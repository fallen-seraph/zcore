from tools.linux_files import LinuxFiles

def range_generator(locationX1, locationY1, locationX2, locationY2):
    mapFileList = []

    for x in range(locationX1, locationY1+1):
        for y in range (locationX2, locationY2+1):
            mapFileList.append(f"map_{str(x)}_{str(y)}.bin")

    return mapFileList