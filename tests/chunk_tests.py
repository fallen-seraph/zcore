from tools import chunks
from pathlib import Path

def range_generator_test():
    test1 = chunks.build_coordinate_list(0, 0, 1, 1)
    test2 = chunks.build_coordinate_list(0, 0, 5, 5)

    if "0_0" in test1:
        print("Test 1: True")
    else:
        print("Test 1: False")

    if "3_3" in test2 and "3_5" in test2:
        print("Test 2: True")
    else:
        print("Test 2: False")

    if "7_3" not in test2:
        print("Test 3: True")
    else:
        print("Test 3: False")

def generate_chunk_list_from_range_test():
    test1 = chunks.generate_chunk_list_from_range("0_0", "10_10")

    testList = ["0_5", "2_6", "6_9"]

    print("3 Coordinate Checks:")
    for x in testList:
        if x in test1:
            print("True")

def build_test_chunk_file():
    filePath = Path("tests") / "chunkList.txt"
    testList = ["1281_647", "1281_646", "1282_647", "1282_646"]

    with open(filePath, "w") as openFile:
        for chunkFileName in testList:
            openFile.write(chunkFileName+"\n")

def get_chunks_from_test():
    filePath = Path("tests") / "chunkList.txt"
    with open(filePath, "r") as fileObject:
        test1 = chunks.get_chunks_from(fileObject)
        filePath.unlink()

    testList = ["1281_646", "1282_647"]

    print("2 Coordinate Checks:")
    for x in testList:
        if x in test1:
            print("True")
        else:
            print("False")

def main():
    range_generator_test()
    generate_chunk_list_from_range_test()
    build_test_chunk_file()
    get_chunks_from_test()

if __name__ == '__main__':
    main()