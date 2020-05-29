from openpyxl import load_workbook


class GetExcel():
    def createList(self,path):
        global numaralar
        numaralar = []
        workbook = load_workbook(filename=path, read_only=True)
        worksheet = workbook.active
        for i in range(0,1000000):
            cell_A = "{}{}".format("A", i+1)
            name = worksheet[cell_A].value
            if name == "None" or name is None:
                break
            if name != "" or name is not None:
                cell_B = "{}{}".format("B", i+1)
                phone_number = worksheet[cell_B].value
                if phone_number != "" or phone_number is not None:
                    numaralar.append([])
                    numaralar[i].append(str(name))
                    numaralar[i].append(str(phone_number))
                    numaralar[i].append("❌")
    def getList(self):
        global numaralar
        return numaralar