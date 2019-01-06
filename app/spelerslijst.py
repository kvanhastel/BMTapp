from classes.io import IO


def Spelerslijst():
    spelerslijst = []
    IO.download_ledenlijst()
    spelerslijst = IO.inlezen_bestand()
    return spelerslijst
