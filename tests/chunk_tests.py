from pathlib import Path

import tests.windows_config_setup as wcs

def test_range_generator():
    coordList = chunks.build_coordinate_list(0, 0, 5, 5)

    assert "0_0" in chunks.build_coordinate_list(0, 0, 1, 1)
    assert "3_3" in coordList
    assert "3_5" in coordList
    assert "7_3" not in coordList

def test_generate_chunk_list_from_range():
    test1 = chunks.generate_chunk_list_from_range("0_0", "10_10")

    testList = ["0_5", "2_6", "6_9"]

    for coord in testList:
        if coord in test1:
            assert coord in test1

def build_test_chunk_file():
    filePath = Path("tests") / "chunkList.txt"
    testList = ["1281_647", "1281_646", "1282_647", "1282_646"]

    with open(filePath, "w") as openFile:
        for chunkFileName in testList:
            openFile.write(chunkFileName+"\n")

def get_chunks_from_test():
    filePath = Path("tests") / "chunkList.txt"
    with open(filePath, "r") as fileObject:
        test1 = chunks.delete_chunks_from_file(fileObject)
        filePath.unlink()

    testList = ["1281_646", "1282_647"]

    print("2 Coordinate Checks:")
    for x in testList:
        assert x in test1

if __name__ == '__main__':
    wcs.windows_config_builder()
    wcs.zcore_config_copy()
    from tools import chunks
    test_range_generator()
    test_generate_chunk_list_from_range()
    #build_test_chunk_file()
    #test_get_chunks_from()
    wcs.windows_config_cleanup()