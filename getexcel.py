from openpyxl import load_workbook
import time

def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    if len(val) == n:
      yield list(val)

class GetExcel():
    def createList(self,path):
        global numaralar
        numaralar = []
        workbook = load_workbook(filename=path, read_only=True)
        worksheet = workbook.active
        #start_time = time.time()
        i = 0
        for row in worksheet.rows:
            for cell in row:
                i += 1
                numaralar.append(cell.value)
            if(i % 2 == 0):
                numaralar.append("❌")
        #print("--- {} seconds ---".format(time.time() - start_time)) ## Time of Get Data
        numaralar = (list(group(numaralar, 3)))

        """
        for i in range(0,1000000):
            cell_A = "{}{}".format("A", i+1)
            name = worksheet[cell_A].value
            if i == 1001:
                #numaralar = []
                break
            if name == "None" or name is None:
                break
            elif name != "" or name is not None:
                cell_B = "{}{}".format("B", i+1)
                phone_number = worksheet[cell_B].value
                if phone_number != "" or phone_number is not None:
                    numaralar.append([])
                    numaralar[i].append(str(name))
                    numaralar[i].append(str(phone_number))
                    numaralar[i].append("❌")
        """
    def getList(self):
        global numaralar
        return numaralar