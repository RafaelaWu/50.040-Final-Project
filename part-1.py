import argparse
from collections import defaultdict
import math


def parse_training_file(file_name):
    print('Parsing training file...')
    training_file = open(file_name, 'r', encoding='utf-8')
    list_words = []
    list_occurrence_words = []
    list_tags = []
    list_sent = []
    curr_sent = []
    for line in training_file:
        if line != '' and line != '\n':
            content = line.strip().split()
            word = line[:(len(line) - len(content[-1])) - 2]
            tag = content[-1]
            if word not in list_occurrence_words:
                list_occurrence_words.append(word)
            curr_sent.append(tag)
            list_words.append(word)
            list_tags.append(tag)
        else:
            list_sent.append(curr_sent)
            curr_sent = []
    print('Parsing finished.')
    return list_words, list_tags, list_occurrence_words, list_sent


# This function estimates the emission parameter from the training set using MLE
# list_tags = nested list of sequences of y sequences
# list_words = nested list of sequences of x sequences
# Assume valid sequence
# Here, we handle the case where UNK tag appears in the code, generating the emission dictionary.
def emission_feature(list_words, list_tags):
    print('Calculating Emission...')
    str_dict = {}
    dictionary_emission = {}
    dictionary_tags = {}
    for i in range(len(list_tags)):
        if list_tags[i] not in dictionary_emission.keys():
            dictionary_emission[list_tags[i]] = {}
        if list_tags[i] not in dictionary_emission[list_tags[i]].keys():
            dictionary_emission[list_tags[i]][list_words[i]] = 1.0
        else:
            dictionary_emission[list_tags[i]][list_words[i]] += 1.0
        if list_tags[i] not in dictionary_tags.keys():
            dictionary_tags[list_tags[i]] = 1.0
        else:
            dictionary_tags[list_tags[i]] += 1.0
    for tag in dictionary_emission.keys():
        for word in list_words:
            str_feat = 'emission:' + tag + '+' + word
            if str_feat not in str_dict.keys():
                str_dict[str_feat] = 0.0
            if word in dictionary_emission[tag].keys():
                str_dict[str_feat] = math.log(float(dictionary_emission[tag][word]) / dictionary_tags[tag])
            else:
                str_dict[str_feat] = float('-inf')
    print('Finished.')
    return dictionary_emission, dictionary_tags, str_dict


def transition_feature(list_sent):
    print('Calculating Transition...')
    str_dict = {}
    dictionary_tags = {}
    dictionary_transition = {}

    for sent in list_sent:
        sent.insert(0, 'START')
        sent.append('END')
        for tag in sent:
            if tag not in dictionary_tags.keys():
                dictionary_tags[tag] = 1.0
            else:
                dictionary_tags[tag] += 1.0
            if tag not in dictionary_transition.keys():
                dictionary_transition[tag] = {}
        for i in range(len(sent)-1):
            if sent[i] not in dictionary_transition.keys():
                dictionary_transition[sent[i]] = {}
            if sent[i+1] not in dictionary_transition[sent[i]].keys():
                dictionary_transition[sent[i]][sent[i+1]] = 1.0
            else:
                dictionary_transition[sent[i]][sent[i+1]] += 1.0

    # Calculation
    for tag in dictionary_tags.keys():
        for cont_tag in dictionary_transition[tag].keys():
            str_feat = 'transition:' + tag + '+' + cont_tag
            if str_feat not in str_dict.keys():
                str_dict[str_feat] = 0.0
            str_dict[str_feat] = math.log(float(dictionary_transition[tag][cont_tag] /
                                 (dictionary_tags[tag])))

    print('Finished.')
    return str_dict


def part_1(train_file_name):
    list_words, list_tags, list_occurrence, list_sent = parse_training_file(train_file_name)
    dict_words, dict_tags, emis_str = emission_feature(list_words, list_tags)
    transit_str = transition_feature(list_sent)

    # print(emis_str['emission:B-positive+john'])
    # print(transit_str['transition:B-negative+I-negative'])


def transition(listy, first, second):
    check = False
    numerator = 0.0
    denominator = 0.0
    if first == "":
        check = True
        denominator = 1
    for line in listy:
        if (line == second) & check:
            numerator = numerator + 1
        check = False

        if line == first:
            check = True
            denominator = denominator + 1

    if second == "":
        numerator = numerator + 1

    if denominator != 0:
        return numerator / denominator
    else:
        return 0

def transitionlist(listy, rangexy):
    dictionary = {}
    rangey = rangexy.copy()
    rangey.append("")
    for i in range(len(rangey)):
        anotherdictionary = {}
        for j in range(len(rangey)):
            if ((i + j != 2 * len(rangey))):
                anotherdictionary[rangey[j]] = transition(listy, rangey[i], rangey[j])
        dictionary[rangey[i]] = anotherdictionary
    return dictionary

parser = argparse.ArgumentParser(description='Provide the training file you wish to use.')
parser.add_argument('-train', type=str)

args = parser.parse_args()
part_1(args.train)

# separator = ' '
# outputColumnIndex = 1
# discardInstance = []
# gold = open(args.standard, "r", encoding='UTF-8')
# prediction = open(args.output, "r", encoding='UTF-8')
# observed = get_observed(gold)
# predicted = get_predicted(prediction)
# compare_observed_to_predicted(observed, predicted)
