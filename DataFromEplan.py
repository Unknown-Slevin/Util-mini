
import openpyxl

class DataFromEplan:

    def __init__(self):
        self.io = {0: ""}
        self.name_var = {0: ""}
        self.name_var_length = 1

        self.io.clear()
        self.name_var.clear()


    def readExel(self, file_path_eplan):

        wb = openpyxl.load_workbook(file_path_eplan)
        sheet = wb['sheet1']

        for i in range(1, sheet.max_row):
            io = sheet[f"A{i}"]
            name_var = sheet[f"B{i}"]
            if (name_var.value != None):
                self.name_var[self.name_var_length] = name_var.value
                self.io[self.name_var_length] = io.value
                self.name_var_length = self.name_var_length + 1

    def print(self):
        print(self.io)
        print(self.name_var)
        print(f"length: {self.name_var_length}")
        print()

    def getVar(self, i):
        return self.name_var[i]

    def getIO(self, i):
        return self.io[i]