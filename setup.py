from distutils.core import setup

setup(
    name="ChessComLibraryExport",
    version="0.1",
    description="Download your whole Chess.com Library (chess.com/library)",
    author="Manuel Pepe",
    author_email="manuelpepe-dev@outlook.com.ar",
    url="https://github.com/manuelpepe/ChessComLibraryExporter",
    py_modules=["chess_library_exporter"],
    install_requires=["selenium"],
    entry_points={"console_scripts": ["chess_library_exporter = chess_library_exporter:main"]},
)
