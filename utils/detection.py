import pandas as pd
import numpy as np

class Main():
    def __init__(self,debug=False):
        net_train_orig = pd.read_csv(r"D:\desktop\资料\2023春\实验日记\net_train.csv", sep=',', index_col=0)
        self.fun_list = net_train_orig['Modbus_Function_Code'].tolist()
        val_list = net_train_orig['Modbus_Value'].tolist()
        self.value_list = []
        for val in val_list:
            if val == 'Number of Elements: 1':
                val = [1]
            elif str(val) == 'nan':
                val = [0]
            else:
                a = val.split(';')
                x_list = []
                #print(a)
                for x in a:
                    x = x.lstrip(' ').split(' ')
                    for i in x:
                        i = int(i,16)
                        x_list.append(i)
                val = x_list
            self.value_list.append(val)
        #print(self.value_list)
                    
    def run(self):
        fun_num_dict = {}
        blank_num = 0
        val_num_dict = {}
        val_dict = {}
        for i,fun_code in enumerate(self.fun_list):
            if np.isnan(fun_code):#fun_code为空
                blank_num = blank_num + 1
                if 0 not in fun_num_dict:
                    fun_num_dict[0] = 1
                else:
                    fun_num_dict[0] = fun_num_dict[0] + 1
            elif fun_code not in fun_num_dict:
                fun_num_dict[fun_code] = 1
            else:
                fun_num_dict[fun_code] = fun_num_dict.get(fun_code,0) + 1
        for i,val in enumerate(self.value_list):
            if len(val) == 1:
                if val[0] == 1:
                    if 'Number of Elements: 1' not in val_num_dict:
                        val_num_dict['Number of Elements: 1'] = 1
                        val_dict['Number of Elements: 1'] = i
                    else:
                        val_num_dict['Number of Elements: 1'] = val_num_dict['Number of Elements: 1'] + 1
            elif str(val) not in val_num_dict:
                val_num_dict[str(val)] = 1
                val_dict[str(val)] = i
            else:
                val_num_dict[str(val)] = val_num_dict[str(val)] + 1
        #print(val_num_dict.keys())
        ###绘图
        key_list = val_num_dict.keys()
        val_chart_dict = [0] * len(key_list)
        for i in range(len(key_list)):
            val_chart_dict[i] = [0] * len(key_list)
        #print([i for i, x in enumerate(key_list) if x == 'Number of Elements: 1'])
        for i,val in enumerate(self.value_list):
            if len(val) == 1:
                val = 'Number of Elements: 1'
            else:
                val = str(val)
            if i+1 < len(self.value_list):
                if len(self.value_list[i+1]) == 1:
                    next_val = 'Number of Elements: 1'
                else:
                    next_val = str(self.value_list[i+1])
                n = [i for i, x in enumerate(key_list) if x == val]
                y = [i for i, x in enumerate(key_list) if x == next_val]
                n = n[0]
                y = y[0]
                val_chart_dict[n][y] = val_chart_dict[n][y] + 1
        ##########print(fun_num_dict)
        fkey_list = fun_num_dict.keys()
        fun_chart_dict = [0] * len(fkey_list)
        for i in range(len(fkey_list)):
            fun_chart_dict[i] = [0] * len(fkey_list)
        #print([i for i, x in enumerate(key_list) if x == 'Number of Elements: 1'])
        for i,val in enumerate(self.fun_list):
            if np.isnan(val):
                val = 0
            if i+1 < len(self.fun_list):
                if np.isnan(self.fun_list[i+1]) :
                    next_val = 0
                else:
                    next_val = self.fun_list[i+1]
                n = [i for i, x in enumerate(fkey_list) if x == val]
                y = [i for i, x in enumerate(fkey_list) if x == next_val]
                n = n[0]
                y = y[0]
                fun_chart_dict[n][y] = fun_chart_dict[n][y] + 1
        print(fun_chart_dict)
        print(fun_num_dict)
        print(val_chart_dict)
        print(val_num_dict)
            









if __name__ == "__main__":
    main = Main(debug=False)
    main.run() 