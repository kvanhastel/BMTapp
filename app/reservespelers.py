from classes.io import IO


def Reservespelers():
    spelers = []
    IO.download_ledenlijst()
    spelers = IO.inlezen_bestand()
    return spelers
