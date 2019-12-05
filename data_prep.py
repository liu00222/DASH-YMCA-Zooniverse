import pandas as pd
import numpy as np
import json
import sys
from datetime import datetime

pd.options.mode.chained_assignment = None

################################################################################
#### extract data
################################################################################
def extract_data(data, version=0):
    # remove everything before 2018 April 02 (line 54 in csv)
    dt_frmt = "%Y-%m-%d  %H:%M:%S UTC"
    data["created_dt"] = [datetime.strptime(i, dt_frmt) for i in data["created_at"]]
    data = data[data["created_dt"] > datetime(2018, 4, 1)]


    # convert json columns to json
    data["json_metadata"] = data["metadata"].apply(json.loads)
    data["json_annotations"] = data["annotations"].apply(json.loads)
    data["json_subject_data"] = data["subject_data"].apply(json.loads)


    # get filename
    def grabFn(x):
        subj = str(x["subject_ids"])
        return x["json_subject_data"][subj]["Filename"]
    data["filename"] = data.apply(grabFn, axis=1)

    # get whether or not it's retired
    def grabRetired(x):
        subj = str(x["subject_ids"])
        ret = x["json_subject_data"][subj]["retired"]
        yn = ["no", "yes"]
        return yn[ret is not None]
    data["retired"] = data.apply(grabRetired, axis=1)


    # get card color from annotations
    def getCardColor(x):
        val = x["json_annotations"][0]["value"]
        if len(val) == 0:
            return "NA"
        elif len(val) == 1:
            return val[0]
        else:
            return val
    data["card_color"] = data.apply(getCardColor, axis=1)


    # get the punches with x and y coordinates
    def getPunches(x):
        points = x["json_annotations"][1]["value"]
        def getXYval(p):
            n_val = p["details"][0]["value"]
            x_val = p["x"]
            y_val = p["y"]
            return n_val, x_val, y_val
        simple_points = [getXYval(p) for p in points]
        simple_points.sort()
        return simple_points

    punches = []
    for i in range(len(data)):
        punches.append(getPunches(data.iloc[i]))
    data["punches"] = punches


    # get only the numbers from the punchcards
    def getNumbers(x):
        points = x["json_annotations"][1]["value"]
        simple_points = [p["details"][0]["value"] for p in points]
        simple_points.sort()
        return simple_points

    numbers = []
    for i in range(len(data)):
        numbers.append(getNumbers(data.iloc[i]))
    data["punches_numbers_only"] = numbers


    # trim down columns to get rid of things we won't use
    data = data[["classification_id", "user_name", "workflow_name",
                 "workflow_version", "created_at", "subject_ids", "filename",
                 "retired", "card_color", "punches", "punches_numbers_only"]]

    # save extracted columns sorted by subject id
    data = data.sort_values("subject_ids")
    data.to_csv("extracted_data{0}.csv".format(version), index=False)
    
    return data


################################################################################
#### reduce data
################################################################################
def reduce_data(data, version=0):
    # reduce data so it says how many people agree upon values
    new_data = pd.DataFrame(columns=["subject_id", "filename", "num_classifications",
                                     "card_color", "punchcard_numbers",
                                     "card_color_agreement", "punchcard_agreement"])
    for f in data["subject_ids"].unique():
        group = data[data["subject_ids"] == f]

        card_colors = dict()
        punch_numbers = dict()
        n = 0
        for i in range(len(group)):
            n += 1
            cur_line = group.iloc[i]
            # get filenames and subject ids
            subj = cur_line["subject_ids"]
            fns = cur_line["filename"]

            # get card colors
            cc = cur_line["card_color"]
            if cc not in card_colors:
                card_colors[cc] = 0
            card_colors[cc] += 1

            # get punch numbers
            for pn in cur_line["punches_numbers_only"]:
                if pn not in punch_numbers:
                    punch_numbers[pn] = 0
                punch_numbers[pn] += 1

        c_agree = len(card_colors) == 1
        if len(punch_numbers) > 0:
            p_agree = all(np.equal(list(punch_numbers.values()), max(punch_numbers.values())))
        else:
            p_agree = True
        sbj_data = {"subject_id":subj, "filename":fns, "num_classifications":n,
                    "card_color":[card_colors], "punchcard_numbers":[punch_numbers],
                    "card_color_agreement":c_agree, "punchcard_agreement":p_agree}
        sbj_data = pd.DataFrame.from_dict(sbj_data)
        new_data = new_data.append(sbj_data)

    new_data = new_data.sort_values(["card_color_agreement", "punchcard_agreement", 
                                     "num_classifications", "subject_id"],
                                    ascending = [True, True, False, True])
    new_data = new_data[["subject_id", "filename", "num_classifications",
                         "card_color", "punchcard_numbers",
                         "card_color_agreement", "punchcard_agreement"]]
    new_data.to_csv("reduced_data{0}.csv".format(version), index=False)

    return new_data

if __name__ == "__main__":
    if len(sys.argv) == 3:
        data = pd.read_csv(sys.argv[1])
        print("Extracting data")
        data = extract_data(data, sys.argv[2])
        print("Reducing data")
        data = reduce_data(data, sys.argv[2])
    else:
        print("The program must be run as \"python data_prep.py <input_file_name> <output_suffix>\"")