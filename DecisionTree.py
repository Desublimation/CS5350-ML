import threading
import sys
import csv
import os
import pandas as pd
import math

class DecisionTree:
    def __init__(self, treeType):
        self.keys = []
        self.result_val = []
        self.root_attr = dict()
        self.thisTree = dict()
        self.layer = 0
        self.lock = threading.Lock()
        if treeType == "car":
            self.keys = ["buying","maint","doors","persons","lug_boot","safety","label"]
            self.result_val = ["unacc", "acc", "good", "vgood"]
            self.root_attr = {"buying":["vhigh","high","med","low"], "maint":["vhigh","high","med","low"], 
                              "doors":["2","3","4","5more"], "persons":["2","4","more"], "lug_boot":["small","med","big"],
                              "safety":["low","med","high"], "label":self.result_val.copy()}
        elif treeType == "bank":
            self.keys = ["age", "job", "marital", "education", "default", "balance", "housing", "loan", "contact", "day", "month", "duration", "campaign", "pdays", "previous", "poutcome","y "]
            self.result_val = ["yes", "no"]
            self.root_attr = {}
            

        self.dataStorage = {key: [] for key in self.keys}
        self.rows = 0
        self.dataArr = []
        # self.count_dict = dict()
    
    def loadData(self, dataLine: list[list[str]]) -> bool:
        try:
            self.dataArr.append(dataLine)
            for key, value in zip(self.dataStorage.keys(), dataLine):
                self.dataStorage[key].append(value)
            self.row += 1
            return True
        except:
            return False

    def accountAttribute(self, current_list,result_list):
        count_dict = dict()
        result_dict = {key: int(0) for key in self.result_val}
        total_result = result_dict.copy()
        for i in range(len(current_list)):
            current_attr = current_list[i]
            current_result = result_list[i]
            total_result[current_result]+=1
            if  current_attr in count_dict:
                temp_dict = count_dict[current_attr]
                temp_dict[current_result] += 1
            else:
                temp_dict = result_dict.copy()
                temp_dict[current_result] = 1
                count_dict[current_attr] = temp_dict
        count_dict["total"] = total_result
        return count_dict

    def expection(self, count_dict, ratio_dict):
        exp_result = 0
        attributes_num = dict()
        for key1, val1 in count_dict.items():
            attr_num = 0
            for key2, val2 in val1.items():
                attr_num += val2
            attributes_num[key1] = attr_num
        total_num = attributes_num["total"]
        for key, val in ratio_dict.items():
            if key == 'total':
                continue
            current_exp = attributes_num[key]/total_num * ratio_dict[key]
            exp_result += current_exp
        
        return exp_result

    def entropy(self, my_dict):
        total = int(0)
        result = 0
        ratio_list = []
        for key, val in my_dict.items():
            total +=val
        for key,val in my_dict.items():
            current_ratio = val/total
            ratio_list.append(current_ratio)
        
        for r in ratio_list:
            current_log = 0
            if r != 0:
                current_log = math.log2(r)
            result += (-1)*r*current_log
        return result

    def ME(self, my_dict):
        total = int(0)
        result = 0
        ratio_list = []
        for key, val in my_dict.items():
            total +=val
        max_value = max(my_dict.values())
        result = 1-max_value/total
        return result

    def Gini_index(self, my_dict):
        total = int(0)
        result = 0
        ratio_list = []
        for key, val in my_dict.items():
            total +=val
        for key,val in my_dict.items():
            current_ratio = val/total
            ratio_list.append(current_ratio)
        for r in ratio_list:
            result += r*r
        result = (-1)*result + 1
        return result
    # 0: entropy
    # 1: Majority Error
    # 2: Gini Index
    def find_root(self, gain_type, count_dict):
        # entropy
        if gain_type == 0:
            entropy_dict = dict()
            for key1, val1 in count_dict.items():
                current_entropy_dict = dict()
                for key2, val2 in val1.items():
                    current_entropy_dict[key2] = self.entropy(val2)
                entropy_dict[key1] = current_entropy_dict

            exp_dict = dict()
            for key, val in count_dict.items():
                curr_exp = self.expection(val,entropy_dict[key])
                exp_dict[key] = curr_exp

            total_entropy = 0
            for key, val in entropy_dict.items():
                total_entropy = val["total"]
                break
            
            # print(f"total entropy: \n{total_entropy}")
            # print(f"")

            info_gain = dict()
            for key, val in exp_dict.items():
                info_gain[key] = total_entropy - val
            # print(f"infomation gain: \n{info_gain}")
            # Find the key corresponding to the maximum value (optional)
            max_key = max(info_gain, key=info_gain.get)
            # print(f"best fit: {max_key}")
            return max_key
        
        # majority error
        elif gain_type == 1:
            Majority_error_dict = dict()
            for key1, val1 in count_dict.items():
                current_ME_dict = dict()
                for key2, val2 in val1.items():
                    current_ME_dict[key2] = self.ME(val2)
                Majority_error_dict[key1] = current_ME_dict
            # print(f"majority error static: \n{Majority_error_dict}")
            # print(f"")
            
            exp_dict = dict()
            for key, val in count_dict.items():
                curr_exp = self.expection(val,Majority_error_dict[key])
                exp_dict[key] = curr_exp
            # print(f"expection: \n{exp_dict}")
            # print(f"")

            total_ME = 0
            for key, val in Majority_error_dict.items():
                total_ME = val["total"]
                break
            # print(f"total ME: \n{total_ME}")
            # print(f"")

            Gain = dict()
            for key, val in exp_dict.items():
                Gain[key] = total_ME - val
            # print(f"ME gain: \n{Gain}")
            # Find the key corresponding to the maximum value (optional)
            max_key = max(Gain, key=Gain.get)
            # print(f"best fit: {max_key}")
            return max_key
        
        # Gini index
        elif gain_type == 2:
            GI_dict = dict()
            for key1, val1 in count_dict.items():
                current_GI_dict = dict()
                for key2, val2 in val1.items():
                    current_GI_dict[key2] = self.Gini_index(val2)
                GI_dict[key1] = current_GI_dict
            # print(f"majority error static: \n{GI_dict}")
            # print(f"")

            exp_dict = dict()
            for key, val in count_dict.items():
                curr_exp = self.expection(val,GI_dict[key])
                exp_dict[key] = curr_exp
            # print(f"expection: \n{exp_dict}")
            # print(f"")

            total_GI = 0    
            for key, val in GI_dict.items():
                total_GI = val["total"]
                break
            # print(f"total Gini Index: \n{total_GI}")
            # print(f"")

            Gain = dict()
            for key, val in exp_dict.items():
                Gain[key] = total_GI - val
            # print(f"GI gain: \n{Gain}")
            # Find the key corresponding to the maximum value (optional)
            max_key = max(Gain, key=Gain.get)
            # print(f"best fit: {max_key}")
            return max_key
        else:
            raise ValueError(f"gain_type({gain_type}) is not correct, please retry: [0]:Entorpy, [1]: Majority Error, [2]: Gini Index.")
    
    def new_form(self, my_dict, layerTuple):
        form_dict = {}
        # print(f"in new_form: {layerTuple}")
        for attr in layerTuple[1]:
            # Step 1: Convert the dictionary to a pandas DataFrame
            df = pd.DataFrame(my_dict)
            # Step 2: Filter rows where "Outlook" is "S"
            filtered_df = df[df[layerTuple[0]] == attr]
            # Step 3: Drop the root column from the filtered DataFrame
            filtered_df = filtered_df.drop(columns=layerTuple[0])
            filtered_dict = filtered_df.to_dict(orient="list")
            form_dict[attr] = filtered_dict
            # Print the filtered DataFrame
            df = pd.DataFrame(filtered_dict)
            # print(f"in new_form: \n{df}")

        return form_dict
    
    def build_tree(self, deepth:int, gain_type:int, handle_missing = False):
        
        layerTuple = self.build_one_layer(self.dataStorage, self.result_val, gain_type)
        form_dict = self.new_form(self.dataStorage, layerTuple)
        self.branches(form_dict,1,deepth,gain_type,layerTuple)
        print(f"{self.thisTree}")
        # print(f"layer {self.layer}")

    def build_one_layer(self, form_dict,label_list, gain_type,lastLayerTuple = None):
        # build dict record every attrbuite and its related label
        count_label_dict = dict()
        for key in form_dict.keys():
            if key == self.keys[len(self.keys)-1]:
                continue
            result_key = self.keys[len(self.keys)-1]
            result_list = form_dict[result_key]
            counted_dict = self.accountAttribute(form_dict[key],result_list)
            count_label_dict[key] = counted_dict
        
        # find the best fit root in current layer
        best_fit = self.find_root(gain_type, count_label_dict)
        best_fit_attrbuilts = self.root_attr[best_fit]
        # draw this layer tree
        layerTuple = (best_fit,best_fit_attrbuilts)
        self.drawTree(layerTuple, lastLayerTuple,False)
        
        return layerTuple
    
    def branches(self,forDict, currentDepth, exp_depth, gainType, layerTuple):
        
        if len(forDict) == 0:
            return
        deleteForms = []
        # print(f"last layer: {layerTuple}")
        for key, form in forDict.items():
            # if len(forDict)!=0:
            #     print(f"current layertuple:{layerTuple}\n{pd.DataFrame(form)}")
            if len(form) == 0:
                deleteForms.append(key)
                continue
            if all(not v for v in form.values()):
                deleteForms.append(key)
                continue
                
            leaf = self.findLeaf(form)
            if leaf != None:
                self.drawTree((key, [leaf]), (layerTuple[0], key),True)
                deleteForms.append(key)



        for form in deleteForms:
            forDict.pop(form)
        
        if len(forDict) == 0:
            return
        if currentDepth >= exp_depth:
            return
        currentDepth+=1
        
        for key, form in forDict.items():
            layerTuple2 = self.build_one_layer(form,self.result_val,gainType,(layerTuple[0], key))
            # print(f"current layer: {layerTuple2}")
            
            next_form_dict = self.new_form(form,layerTuple2)
            self.branches(next_form_dict, currentDepth, exp_depth, gainType,layerTuple2)
        self.layer+=1

    def findLeaf(self, my_dict):
        result_root = self.keys[len(self.keys)-1]
        try:
            curr_result = my_dict[result_root][0]
        except:
            print(f"{my_dict}")
        resultList = []
            
        # curr_result = ""
        # try:
        #     curr_result = my_dict[result_root][0]
        # except:
        #     print(f"curr_result is not avalible")    
        #     print(my_dict)
        #     # df = pd.DataFrame(my_dict)
        for attr in my_dict[result_root]:
            if attr != curr_result:
                # if len(my_dict)==2:
                #     return "binary"
                return None
        return curr_result

    def checkData(self, dataType = "dict", attribute = "all"):
        row = int(0)
        # col = int(0)
        if dataType == "arr":
            for l in self.dataArr:
                if attribute == "all":
                    print(l)
                    row+=1
                else:
                    if attribute in l:
                        print(l)
                        row += 1
        if dataType == "dict":
            df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in self.dataStorage.items()]))
            print(df)

    #leaf: (key, [leaf])|(last_root, last_attr)
    #branch: (current_root, current_attr_list)|(last_root, last_attr)
    def drawTree(self, currentlayer, lastlayer=None, isLeaf = False):
        current_root, current_leafs = currentlayer  # Unpack the current layer
        # result_dict_samples = 
        if lastlayer is None:
            # Initialize the tree if there is no last layer (first layer)
            self.thisTree[current_root] = {leaf: {} for leaf in current_leafs}
        else:
            # Unpack the last layer
            last_root, last_leaf = lastlayer
            for key, val in self.thisTree.items():
                if key == last_root:
                    for key2, val2 in val.items():
                        for r in self.result_val:
                            if r in list(val2.keys()):
                                break
                        if key2 == last_leaf:
                            # val2[current_root] = {curr_attr:{} for curr_attr in current_leafs}
                            # val[current_root] = {curr_attr:{} for curr_attr in current_leafs}

                            if isLeaf or key2 == current_root:
                                val[current_root] = {curr_attr:{} for curr_attr in current_leafs}

                            else:
                                val2[current_root] = {curr_attr:{} for curr_attr in current_leafs}
                else: 
                    for key2, subbranch in val.items():
                        self.insert_branch(subbranch,currentlayer, lastlayer,isLeaf)

    def insert_branch(self, subbranch, currentlayer, lastlayer, isLeaf = False):
        current_root, current_leafs = currentlayer  # Unpack the current layer
        last_root, last_leaf = lastlayer
        for key, val in subbranch.items():
                if key == last_root:
                    for key2, val2 in val.items():
                        for r in self.result_val:
                            if r in list(val2.keys()):
                                break
                        
                        if key2 == last_leaf:
                            if isLeaf or key2 == current_root:
                                val[current_root] ={curr_attr:{} for curr_attr in current_leafs}
                            else:
                                val2[current_root] ={curr_attr:{} for curr_attr in current_leafs}
                else: 
                    for key2, subbranch2 in val.items():
                        self.insert_branch(subbranch2,currentlayer, lastlayer)


    def print_tree(self, d, indent=0):
        for key, value in d.items():
            print('  ' * indent + str(key))  # Print the key with indentation
            if isinstance(value, dict) and value:  # If the value is a non-empty dictionary
                self.print_tree(value, indent + 1)  # Recursively print the nested dictionary


    # def readFile(self, fileNames):
    #     for file_name in fileNames:
    #         file_extension = os.path.splitext(file_name)[1].lower()
    #         if file_extension == '.txt':
    #             with open(file_name, 'r') as file:
    #                 print(f"read .txt file")
    #                 for line in file:
    #                     # row = line.strip.split()
    #                     print(f"{line}")
    #         elif file_extension == '.csv':
    #             with open(file_name,'r') as file:
    #                 reader = csv.reader(file)
    #                 for row in reader:
    #                     self.loadData(row)

def read_csv_file(file_name, dTree):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            dTree.loadData(row)
        # dTree.checkData("dict")
            # print(row)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        typeList = ["Info. Gain", "Majority Error", "Gini Index"]
        file_name = sys.argv[1]  # The first argument is the file name
        deepth = sys.argv[2]
        gaintype = int(sys.argv[3])
        if gaintype<3:
            dTree = DecisionTree("car")
            read_csv_file(file_name, dTree)
            print(f"use {typeList[gaintype]}, with deep {deepth} here is the tree")
            dTree.build_tree(deepth=int(deepth),gain_type=int(gaintype))
            print()
        else:
            print("Please provide a CSV file, deepth: int, gain_type: [0]entropy,[1]ME,[2]GI .")
    else:
        print("Please provide a CSV file, deepth: int, gain_type: [0]entropy,[1]ME,[2]GI .")