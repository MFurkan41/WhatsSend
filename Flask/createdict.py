def CreateDict(m,*data):
    if len(data) == 0:
        dic = {"error_message":m}
    else:
        data = data[0]
        dic = {"id":data[0],"name":data[1],"email":data[2],"key":data[4],"mcount":data[5],"message":m}
    return str(dic)