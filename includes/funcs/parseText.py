def parseVersion(text):
    updateH = {}
    nList = []
    for i in text.split("\n"):
        if(i == ""):
            updateH[version] = nList
            nList = []
        elif(i[0] == "-"):
            nList.append(i)
        else:
            version = i
    return list(updateH)