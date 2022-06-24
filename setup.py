from pathlib import Path
from setuptools import setup


README = Path(__file__).parent / "README.md"
with open(README, "r") as fp:
    long_description = fp.read()


setup(
    name="ChessComLibraryExport",
    version="0.3",
    description="Download your whole Chess.com Library (chess.com/library)",
    author="Manuel Pepe",
    author_email="manuelpepe-dev@outlook.com.ar",
    url="https://github.com/manuelpepe/ChessComLibraryExporter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["chess_library_exporter"],
    install_requires=["selenium", "webdriver_manager"],
    entry_points={"console_scripts": ["chess_library_exporter = chess_library_exporter:main"]},
)
