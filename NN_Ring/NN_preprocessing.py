# 00 - Import Dependencies
import os, json
import numpy as np
from matplotlib import pyplot as plt

# 01 - Combines all the json data into one list
def load_multiple_json_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                file_data = json.load(file)
                data.extend(file_data)  # Use extend if each file contains a list
    return data

# 02 - Calculates the [number of entries each label has] and the [lengh of each entry]
def calculate_metrics(data):
    label_count = {} #{label: nr_of_entries} = number of entries each label has
    length_counts = [] #the length of each entry

    for entry in data:
        # Calculating the number of entries per label
        if entry["label"] not in label_count:
            label_count[entry["label"]] = 1
        else:
            label_count[entry["label"]] += 1

        length_counts.append(len(entry["sequence"]))

    return label_count, length_counts

def create_boxplot(length_count):
    fig = plt.figure(figsize = (10, 7))
    plt.boxplot(length_count)
    plt.show()

# 02 - Remove Outliers
def remove_outliers(data, length_counts):
    Q1 = np.percentile(length_counts, 25)
    Q3 = np.percentile(length_counts, 75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    filtered_label_count = {} #{label: nr_of_entries}
    filtered_length_counts = [] #the length of each entry

    filtered_data = []

    for entry in data:
        if lower_bound <= len(entry["sequence"]) and len(entry["sequence"]) <= upper_bound:

            filtered_data.append(entry)
            filtered_length_counts.append(len(entry["sequence"]))

            if entry["label"] not in filtered_label_count:
                filtered_label_count[entry["label"]] = 1
            else:
                filtered_label_count[entry["label"]] += 1

    return filtered_data, filtered_label_count, filtered_length_counts

# 03 - Pads all sequences to same (max) length

def create_padding(sequence, length):
    #only for one individual

    if len(sequence) < length:
        while len(sequence) != length:
            sequence.append([0, 0, 0])

    return sequence



def apply_padding(data, length):
    padded_data = []
    for entry in data:
        padded_data.append(create_padding(entry["sequence"], length))

    padded_data_with_labels = []
    for x in range(len(data)):
        padded_data_with_labels.append({
            "label": data[x]["label"],
            "sequence": padded_data[x]
        })

    return padded_data_with_labels

def NN_preprocessor(directory):
    data = load_multiple_json_files(directory)
    print(f"All Entries: {len(data)}")

    label_count, length_counts = calculate_metrics(data)
    print(label_count)
    # create_boxplot(length_counts)

    filtered_data, filtered_label_count, filtered_length_counts = remove_outliers(data, length_counts)
    print(filtered_label_count)
    # create_boxplot(filtered_length_counts)

    padding = max(filtered_length_counts)
    padded_data = apply_padding(filtered_data, padding)
    print(len(padded_data[0]["sequence"]))

    return padded_data, padding

if __name__ == "__main__":
    directory = 'training_data'
    NN_preprocessor(directory)