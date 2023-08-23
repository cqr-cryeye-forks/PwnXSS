import pathlib
from typing import Final

ROOT_PATH: Final[pathlib.Path] = pathlib.Path(__file__).parent
TEMP_PATH_FOR_DATA: Final[pathlib.Path] = ROOT_PATH.joinpath("xss.json")
