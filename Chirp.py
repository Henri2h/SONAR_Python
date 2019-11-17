class Chirp:

    def getChirp(self):
        file = open("Chirp.csv")
        lines = file.readlines()

        chirp = []
        for i in range(1, len(lines)):
            lsplit = lines[i].split(",")
            chirp.append(float(lsplit[1]))
        return chirp

    def getChirp2(self):
        file = open("Chirp.csv")
        lines = file.readlines()

        chirp = []
        for i in range(1, len(lines)):
            lsplit = lines[i].split(",")
            chirp.append([float(lsplit[1]), float(lsplit[1])])
        return chirp
