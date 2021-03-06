# Written by Timothy van der Valk, Frank van der Top, Shae Williams.
#
# Airplane data set importer class and input to the solver algorithms.
# Data can be loaded from Excel-type files for further processing.

import pandas as pd


class DataSet:
    # Parsed dataset from excel sheet for further processing.

    def __init__(self, file: str =""):
        self.safety_time = 0
        self.num_aircraft = 0
        self.earliest = []
        self.target = []
        self.latest = []
        self.safety_times = []

        # Load file if argument given.
        if file != "":
            self.load_excel(file)


    def __str__(self):
        # Convert to string using nice tabular representation.
        out = "Number of aircraft={:d}, Safety time={:d}\n".format(self.num_aircraft, self.safety_time)
        out += "Earliest, Target, Latest\n"
        for i in range(self.num_aircraft):
            out += "{:6d}, {:6d}, {:6d}\n".format(self.earliest[i], self.target[i], self.latest[i])
        return out


    def load_excel(self, file: str):
        # Load data set from excel sheet.
        # sheets=None loads all sheets.
        excel = pd.read_excel(file, sheet_name=None)
      
        # Retrieve the first sheet containing number of aircraft and safety time.
        # The first row is the columns row.
        # The second row is given by iloc[row, column].
        sheet1 = excel["General information"]
        self.num_aircraft = sheet1.columns[1]
        self.safety_time = sheet1.iloc[0, 1]
    
        # Retrieve the second sheet containg data.
        sheet2 = excel["Times per aircraft"]
        self.earliest = sheet2.iloc[:, 1].tolist()
        self.target = sheet2.iloc[:, 2].tolist()
        self.latest = sheet2.iloc[:, 3].tolist() 
        if file == "data_large_extended.xlsx" or file == "data_small_extended.xlsx":
            self.safety_times = sheet2.iloc[:, 6].tolist()
        else:
            self.safety_times = self.num_aircraft * [self.safety_time]
            
     
    def get_overlaps(self, plane: int):
        overlaps = set()
        e = self.earliest[plane]
        l = self.latest[plane]
        for i in range(self.num_aircraft):
            if i != plane and self.latest[i] >= e and self.earliest[i] <= l:
                overlaps.add(i)
        return list(overlaps)
