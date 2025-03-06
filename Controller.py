

DIGITAL_INPUT = 2
RESISTANCE_INPUT = 3
DIGITAL_OUTPUT = 17
VOLTAGE_OUTPUT = 18

BIT_0 = 1
BIT_1 = 2
BIT_2 = 4
BIT_3 = 8
BIT_4 = 16
BIT_5 = 32
BIT_6 = 64
BIT_7 = 128

DEFAULT_BIN_OUTPUT_DIGIT = 32512

NUMBER_UNIVERSAL_OUTPUT = 8

POSITION_REG_BIN_DIGIT = 3

class Controller:
    def __init__(self, config):
        self.conf = config
        self.regBinDigit = 0

    def getRegBinDigit(self):
        return self.regBinDigit

    def getNameVarPlC(self, var_eplan):
        var_plc = ""
        if f"{var_eplan}" in self.conf.Var:
            var_plc = self.conf.Var[f"{var_eplan}"]
        else:
            print("key not exist!!!!")
        return var_plc

    def getGroupTypeio(self, var_eplan):

        group_typeio = ""
        if f"{var_eplan}" in self.conf.typeio:
            group_typeio = self.conf.typeio[f"{var_eplan}"]
        return  group_typeio

    def getNumVar(self, group_typeio, var_plc):

        num = 0
        var_dict =  getattr(self.conf, group_typeio)

        if f"{var_plc}" in var_dict:
            num = var_dict[f"{var_plc}"][0]
        return num

    def getNumTypeIO(self, group_typeio, type_io):
        num_type = 0

        if (group_typeio == "Di"):
            num_type = DIGITAL_INPUT
            return num_type
        if (group_typeio == "Ai"):
            num_type = RESISTANCE_INPUT
            return num_type
        if (group_typeio == "Do"):
            num_type = DIGITAL_OUTPUT
            return num_type
        if (group_typeio == "Ao"):
            num_type = VOLTAGE_OUTPUT
            return num_type
        return 0

    def getNumMethodIO(self, var_eplan):
        method = 0
        if f"{var_eplan}" in self.conf.Method:
            method = self.conf.Method[f"{var_eplan}"][0]
        return method

    def getBinOutputDigit(self, io):

        new_bin_num = ''
        if (io == "UO1"):
            new_bin_num = DEFAULT_BIN_OUTPUT_DIGIT | BIT_0
        if (io == "UO2"):
            new_bin_num = DEFAULT_BIN_OUTPUT_DIGIT | BIT_1
        if (io == "UO3"):
            new_bin_num = DEFAULT_BIN_OUTPUT_DIGIT | BIT_2
        if (io == "UO4"):
            new_bin_num = DEFAULT_BIN_OUTPUT_DIGIT | BIT_3
        if (io == "UO5"):
            new_bin_num = DEFAULT_BIN_OUTPUT_DIGIT | BIT_4
        if (io == "UO6"):
            new_bin_num = DEFAULT_BIN_OUTPUT_DIGIT | BIT_5
        if (io == "UO7"):
            new_bin_num = DEFAULT_BIN_OUTPUT_DIGIT | BIT_6
        if (io == "UO8"):
            new_bin_num = DEFAULT_BIN_OUTPUT_DIGIT | BIT_7
        print(f"new bin: {new_bin_num}")
        return new_bin_num

    def checkUseUniversalOutput(self, io):
        for i in range(1, NUMBER_UNIVERSAL_OUTPUT + 1):
            if (io == f"UO{i}"):
                print("universal output use!")
                return 1
        return 0

    def getRegistr(self, group_typeio, name_io):
        reg = (0, 0, 0)
        if (group_typeio == "Ai" or group_typeio == "Di"):
            if f"{name_io}" in self.conf.RegUi:
                reg = self.conf.RegUi[f"{name_io}"]

        if (group_typeio == "Ao" or group_typeio == "Do"):
            if f"{name_io}" in self.conf.RegUo:
                reg = self.conf.RegUo[f"{name_io}"]
                self.regBinDigit = self.conf.RegUo[f"{name_io}"][POSITION_REG_BIN_DIGIT]
        return reg

    def getValueAndReg(self, var_eplan, io):
        val_reg = (0, 0, 0, 0, 0, 0)

        var_plc = self.getNameVarPlC(var_eplan)
        group_typeio = self.getGroupTypeio(var_eplan)
        print(f"group_typeio: {group_typeio}")
        print(f"var_plc: {var_plc}")

        num_var_plc = self.getNumVar(group_typeio[0], var_plc[0])
        print(f"num_var_plc: {num_var_plc}")

        num_typeio = self.getNumTypeIO(group_typeio[0], 0)
        print(f"num_typeio: {num_typeio}")

        num_method = self.getNumMethodIO(var_eplan)
        print(f"num_method: {num_method}")

        reg = self.getRegistr(group_typeio[0], io)
        print(reg)

        use_universal_output = self.checkUseUniversalOutput(io)

        bin_output_digit = DEFAULT_BIN_OUTPUT_DIGIT

        if (group_typeio[0] == "Do" and use_universal_output == 1):
            bin_output_digit = self.getBinOutputDigit(io)

        if (group_typeio[0] == "Ai" or group_typeio[0] == "Di"):
            val_reg = (num_var_plc, num_typeio, num_method, reg)
        else:
            val_reg = (num_var_plc, num_typeio, num_method, bin_output_digit, reg)


        return val_reg
