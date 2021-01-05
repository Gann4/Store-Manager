import json, os, requests

class Sales():
    def __init__(self, working_directory, filename):
        self.fullpath = f"{working_directory}\\{filename}"

    def AddData(self, y2r=None, m2r=None, d2r=None, data2r=None):
        if y2r is None and m2r is None and d2r is None and data2r is None:
            return "You must set at least the first argument."
        with open(self.fullpath, "r") as f:
            data = json.load(f)
        ## Secure data type ##
        if data2r != None: data2r = int(data2r)
        ## -- -- -- -- -- ##
        if y2r in data:
            if m2r in data[y2r]:
                if d2r in data[y2r][m2r]: data[y2r][m2r][d2r].append(data2r)
                else: data[y2r][m2r][d2r] = [data2r]
            else: data[y2r][m2r] = {d2r:[data2r]}
        else: data[y2r] = {m2r:{d2r:[data2r]}}
        with open(self.fullpath, "w") as f:
            json.dump(data, f, indent=4)

    def RemoveData(self, y2r=None, m2r=None, d2r=None, dataIndex=None):
        with open(self.fullpath, "r") as f:
            data = json.load(f)
        ## Secure data type ##
        if dataIndex != None: dataIndex = int(dataIndex)
        ## -- -- -- -- -- -- ##
        if y2r is not None and y2r in data:
            if m2r is not None and m2r in data[y2r]:
                if d2r is not None and d2r in data[y2r][m2r]:
                    if dataIndex is not None and len(data[y2r][m2r][d2r]) >= 0: 
                        del data[y2r][m2r][d2r][dataIndex]
                    else: del data[y2r][m2r][d2r]
                else: del data[y2r][m2r]
            else: del data[y2r]
        else: raise Exception("No data assigned to remove or it doesn't exists inside the json file.")

        with open(self.fullpath, "w") as f:
            json.dump(data, f, indent=4)

    def GetSavedData(self):
        with open(self.fullpath, "r") as f:
            return json.load(f)

    def ReplaceData(self, y2r, m2r, d2r, i2r, new_value):
        i2r = int(i2r)
        new_value = int(new_value)
        
        sv_data = self.GetSavedData()
        sv_data[y2r][m2r][d2r][i2r] = new_value

        with open(self.fullpath, "w") as f:
            json.dump(sv_data, f, indent=4)

    def GetTotalOf(self, y2r=None, m2r=None, d2r=None, i2r=None):
        with open(self.fullpath, "r") as f:
            data = json.load(f)
        total = 0
        if y2r is not None:
            if y2r in data:
                if m2r is not None:
                    if m2r in data[y2r]:
                        if d2r is not None:
                            if d2r in data[y2r][m2r]:
                                if i2r is not None: 
                                    try: return data[y2r][m2r][d2r][i2r]
                                    except: return 0
                                else:
                                    for i in data[y2r][m2r][d2r]:
                                        total += i
                            else: print(f"No data found for {y2r}/{m2r}/{d2r}")
                        else:
                            for d in data[y2r][m2r].keys():
                                for i in data[y2r][m2r][d]:
                                    total += i
                    else: print(f"No data found for {y2r}/{m2r}")
                else:
                    for m in data[y2r].keys():
                        for d in data[y2r][m].keys():
                            for i in data[y2r][m][d]:
                                total += i
            else: 
                for y in data.keys():
                    for m in data[y].keys():
                        for d in data[y][m].keys():
                            for i in data[y][m][d]:
                                total += i
        return total

class Config():
    def __init__(self, working_directory, filename):
        self.fullpath = f"{working_directory}\\{filename}"

    def GetCloudData(self, key=None):
        with requests.get("https://ldpstore.000webhostapp.com") as r:
            return json.loads(r.content)[key] if key != None else json.loads(r.content)

    def GetLocalCfgData(self, key=None):
        global config
        if not os.path.exists(config.fullpath): raise Exception("File 'config.json' couldn't be found.")

        with open(config.fullpath, "r") as f:
            return json.load(f)[key] if key != None else json.load(f)

    def IsOutdated(self):
        return self.GetCloudData("version") != self.GetLocalCfgData("version")

class DueDates():
    def __init__(self, working_directory, filename):
        self.fullpath = f"{working_directory}\\{filename}"

# Main file setup
app_version = "0.1.3"
data_folder = "\\appdata\\"
wkdir = os.getcwd() + data_folder

sales = Sales(wkdir, "ventas.json")
config = Config(wkdir, "config.json")
duedates = DueDates(wkdir, "vencimientos.json")

if not os.path.exists(sales.fullpath): 
    with open(sales.fullpath, "w") as f: json.dump({}, f, indent=4)
with open(config.fullpath, "w") as f: json.dump({"version": app_version}, f, indent=4)
with open(duedates.fullpath, "w") as f: json.dump({}, f, indent=4)