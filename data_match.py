# DASH Program
# RA: Yupei Liu
# 2019/11/18



import pandas as pd



def number_to_label(number):
    switcher = {
        '31': 'Divisional',
        '32': 'Camp',
        '33': 'Hut',
        '34': 'Religious',
        '35': 'Educational',
        '36': 'Physical',
        '37': 'Colored Work',
        '38': 'Assn. Service Satisfactory',
        '39': 'Assn. Service Unsatis',
        '40': 'Male',
        '41': 'Business',
        '42': 'Stenographer-Clerk',
        '43': 'Accountant-Bookkeeper',
        '44': 'Purchasing Agent',
        '45': 'Canteen',
        '46': 'Mechanic',
        '47': 'Entertainment',
        '48': 'Warehouse or Shipping',
        '49': 'Mystery 1',
        '50': 'Female',
        '51': 'Lutheran or Other',
        '52': 'Congregational',
        '53': 'Episcopal',
        '54': 'Methodist',
        '55': 'Presbyterian',
        '56': 'Baptist',
        '57': 'Not a Church Member',
        '58': 'Mystery 2',
        '59': 'Mystery 3',
        '60': 'Married',
        '61': 'French',
        '62': 'Italian',
        '63': 'German',
        '64': 'Spanish or Other',
        '65': 'Mystery 4',
        '66': 'Mystery 5',
        '67': 'Mystery 6',
        '68': 'Education below College',
        '69': 'College Partial',
        '70': 'College Graduate',
        '71': 'First Placement 1',
        '72': 'First Placement 2',
        '73': 'First Placement 3',
        '74': 'First Placement 4',
        '75': 'First Placement 5',
        '76': 'Paid over $1200',
        '77': 'Paid over $2100',
        '78': 'Placed Home',
        '79': 'Placed Overseas',
        '80': 'Subsequent Overseas'
    }
    
    return switcher.get(number, "Invalid Match")



def generate_new_dict(dictionary):
    new_dictionary = {}
    
    for key in dictionary:
        new_key = number_to_label(key)
        new_value = dictionary[key]
        new_dictionary[new_key] = new_value
        
    return new_dictionary
        



def matching_data(data):
    for i in range(len(data['punchcard_numbers'])):
        dictionary = eval((data['punchcard_numbers'])[i])
        matched_dictionary = generate_new_dict(dictionary)
        matched_string = str(matched_dictionary)
        (data['punchcard_numbers'])[i] = '%s' % matched_string
        
    data.to_csv("/Users/admin/Desktop/work/DASH/ZOONIVERSE/matched_data.csv", index = False)



if __name__ == "__main__":
    pd.options.mode.chained_assignment = None
    #input_name = input("Please enter the input filename (including format suffix): ")
    input_name = "reduced_datatest.csv"
    data = pd.read_csv(input_name)
    print("Matching the data from numbers to the corresponding labels...")
    matching_data(data)
    print("The matching is successful!")