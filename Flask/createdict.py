def CreateDict(m,*data):
    if len(data) == 0:
        dic = {"error_message":m}
    else:
        data = data[0]
        dic = {"id":data[0],"email":data[1],"key":data[3],"mcount":data[4],"message":m}
    return str(dic)