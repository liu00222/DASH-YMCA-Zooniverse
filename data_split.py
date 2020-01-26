# DASH Program
# RA: Yupei Liu
# 2020/01/03

import pandas as pd


def number_to_label(number):
    switcher = {
        '31': 'divisional',
        '32': 'camp',
        '33': 'hut',
        '34': 'religious',
        '35': 'educational',
        '36': 'physical',
        '37': 'colored_work',
        '38': 'assn._service_satisfactory',
        '39': 'assn._service_unsatis',
        '40': 'male',
        '41': 'business',
        '42': 'stenographer-clerk',
        '43': 'accountant-bookkeeper',
        '44': 'purchasing_agent',
        '45': 'canteen',
        '46': 'mechanic',
        '47': 'entertainment',
        '48': 'warehouse_or_shipping',
        '49': 'punchcard_49',
        '50': 'female',
        '51': 'lutheran_or_other',
        '52': 'congregational',
        '53': 'episcopal',
        '54': 'methodist',
        '55': 'presbyterian',
        '56': 'baptist',
        '57': 'not_a_church_member',
        '58': 'punchcard_58',
        '59': 'punchcard_59',
        '60': 'married',
        '61': 'french',
        '62': 'italian',
        '63': 'german',
        '64': 'spanish_or_other',
        '65': 'punchcard_65',
        '66': 'punchcard_66',
        '67': 'punchcard_67',
        '68': 'education_below_college',
        '69': 'college_partial',
        '70': 'college_graduate',
        '71': 'first_placement_1',
        '72': 'first_placement_2',
        '73': 'first_placement_3',
        '74': 'first_placement_4',
        '75': 'first_placement_5',
        '76': 'paid_over_$1200',
        '77': 'paid_over_$2100',
        '78': 'placed_home',
        '79': 'placed_overseas',
        '80': 'subsequent_overseas'
    }

    return switcher.get(number)


def split_punch_numbers(data):
    n = len(data['punchcard_numbers'])
    x = 50
    result = []

    for i in range(x):
        sub_list = [0] * n
        result += [sub_list]

    for i in range(n):
        dictionary = eval((data['punchcard_numbers'])[i])
        keys = list(dictionary.keys())
        for j in range(len(keys)):
            key = keys[j]
            value = dictionary[key]

            if ',' in key:
                new_keys = key.split(',')
                for k in range(len(new_keys)):
                    if new_keys[k].isnumeric() and int(new_keys[k]) <= 80 and int(new_keys[k]) >= 31:
                        result[int(new_keys[k]) - 31][i] = value
            elif ' ' in key:
                new_keys = key.split(' ')
                for k in range(len(new_keys)):
                    if new_keys[k].isnumeric() and int(new_keys[k]) <= 80 and int(new_keys[k]) >= 31:
                        result[int(new_keys[k]) - 31][i] = value
            else:
                if key.isnumeric() and int(key) <= 80 and int(key) >= 31:
                    result[int(key) - 31][i] = value

    for i in range(x):
        data[number_to_label(str(i + 31))] = result[i]

    return


def split_colors(data):
    n = len(data['card_color'])
    white = [0] * n
    beige = [0] * n
    blue = [0] * n
    sure = [0] * n
    result = {'white': white, 'beige': beige, 'blue': blue, 'not sure': sure}
    colors = ['white', 'beige', 'blue', 'not sure']

    for i in range(n):
        dictionary = eval((data['card_color'])[i])
        keys = list(dictionary.keys())
        values = []
        for j in range(len(keys)):
            key = keys[j]
            value = dictionary[key]
            values.append(value)

            if 'hite' in key:
                result['white'][i] = value
            elif 'eige' in key:
                result['beige'][i] = value
            elif 'lue' in key:
                result['blue'][i] = value
            elif 'sure' in key or 'Other' in key or 'other' in key:
                result['not sure'][i] = value
            else:
                print("no such color!")

        #agreement = False
        #total = float(sum(values))
        #for k in range(len(values)):
        #    if values[k] / total > 0.5:
        #        agreement = True
        #if not agreement:
        #    print(str(data['filename'][i] + " has no agreement on colors!"))

    for color in colors:
        data[color] = result[color]

    return


if __name__ == "__main__":
    pd.options.mode.chained_assignment = None

    input_name = "reduced_datatest.csv"
    data = pd.read_csv(input_name)
    split_colors(data)
    split_punch_numbers(data)

    data.to_csv("/Users/admin/Desktop/work/DASH/DASH-YMCA-Zoonizerse/test_data.csv", index = False)
