import shutil
from pathlib import Path

zcorePath = Path.home() / "zcore/"

def windows_config_builder():
    zcorePath.mkdir(parents=True, exist_ok=True)

def zcore_config_copy():
    shutil.copy2(Path("config.ini"), zcorePath)

def windows_config_cleanup():
    shutil.rmtree(zcorePath)