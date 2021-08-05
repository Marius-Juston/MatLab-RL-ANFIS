import numpy as np
import csv
import torch
from torch.utils.data import TensorDataset, DataLoader
import time
import matplotlib.pyplot as plt

import sys
import itertools
import numpy as np

import torch
from torch.utils.data import TensorDataset, DataLoader

import anfis
from membership import TrapezoidalMembFunc, make_trap_mfs, make_bell_mfs, BellMembFunc, Zero, make_zero
from experimental import train_anfis, test_anfis
dtype = torch.float

def input_data(inp,y, num_cases,num_inputs):
    x = torch.zeros((num_cases, num_inputs))
    with open(inp) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        inputs = []
        temp = 0
        for row in readCSV:
            temp_row = []
            for i in range(len(row)):
                temp_row.append(float(row[i]))
            x[temp] = torch.tensor(temp_row)

            temp +=1

        data = DataLoader(TensorDataset(x,y), batch_size = 64, shuffle = True)
        return data

def output_csv(filename,num_cases):
    y = torch.zeros((num_cases, 1))
    with open(filename) as csvfile:
        temp = 0
        readCSV = csv.reader(csvfile, delimiter=',')
        angular_velocity = []
        for row in readCSV:
            for i in range(len(row)):
                #angular_velocity.append(float(row[i]))
                y[temp] = float(row[i])
            temp += 1
        #    if temp == 50000:
        #        break
#        print(y)
        return y


def mfs_print(model):
    for i in range(len(model.input_keywords)):
        for j in range(model.number_of_mfs[model.input_keywords[i]]):
            print(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf{}'.format(j)].pretty())

def my_model():

    invardefs = [
            ('distance_line', [TrapezoidalMembFunc(-20,-20,-1.425,-0.825,1),
                               TrapezoidalMembFunc(-1.425,-0.825,-0.675,-0.075,2),
                               TrapezoidalMembFunc(-0.675,-0.075,0.075,0.675,3),
                               TrapezoidalMembFunc(0.075, 0.675, 0.825, 1.425,4),
                               TrapezoidalMembFunc(0.825, 1.425, 20, 20,5),
                               Zero()]),
            ('theta_far', [TrapezoidalMembFunc(-3.15, -3.15, -2.375, -1.375,1),
                           TrapezoidalMembFunc(-2.375, -1.375, -1.125, -0.125,2),
                           TrapezoidalMembFunc(-1.125, -0.125, 0.125, 1.125,3),
                           TrapezoidalMembFunc(0.125, 1.125, 1.375, 2.375,4),
                           TrapezoidalMembFunc(1.375, 2.375, 3.15, 3.15,5),
                           Zero()]),
            ('theta_near', [TrapezoidalMembFunc(-3.15, -3.15, -1.71, -0.99,1),
                            TrapezoidalMembFunc(-1.71, -0.99, -0.81, -0.09,2),
                            TrapezoidalMembFunc(-0.81, -0.09, 0.09, 0.81,3),
                            TrapezoidalMembFunc(0.09, 0.81, 0.99, 1.71,4),
                            TrapezoidalMembFunc(0.99, 1.71, 3.15, 3.15,5),
                            Zero()])
                                                                ]
    outvars = ['control_law']

    input_keywords = [] #list
    number_of_mfs = {} #dict
    for i in range(len(invardefs)):
        input_keywords.append(invardefs[i][0])
        number_of_mfs[invardefs[i][0]] = len(invardefs[i][1]) - 1
    #print(invardefs)

    anf = anfis.AnfisNet('ANFIS', invardefs, outvars, input_keywords, number_of_mfs, False)
    return anf

def training_data_selection(i, o):
    inputs = open(i)
    outputs = open(o)
    inputs = csv.reader(inputs)
    num_data= len(list(inputs))
    return num_data,i , o

def generate_txt(model):
    coeffs = (model.layer['consequent']._coeff).tolist()    ##print final coeffs in cnsequent layer.
    with open("coeffs.txt", 'w') as output:
        for row in coeffs:
            output.write(str(row) + '\n')

    mfs = []
    for i in range(len(model.input_keywords)):
        mfs.append(model.input_keywords[i])
        for j in range(model.number_of_mfs[model.input_keywords[i]]):
            mfs.append(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf{}'.format(j)].pretty())
    with open("mfs.txt", 'w') as output:
        for row in mfs:
            output.write(str(row) + '\n')


############################### MAIN FUNCTION HERE
if __name__ == '__main__':
    show_plots = True
    #if len(sys.argv) == 2:  # One arg: example
    #    example = sys.argv[1]
    #    show_plots = False
    time_start = time.clock() # computation time check
    print(time_start)
    model = my_model()
    ######################################
    num_data, i, o = training_data_selection("1inputs100.csv", "1outputs100.csv")
    num_inputs = len(model.input_keywords)

    outputs = output_csv(o, num_data)
    train_data = input_data(i, outputs, num_data, num_inputs)
    #print(*train_data)
    #print(model.layer['fuzzify'].varmfs)
    num_epchos = 20
    train_anfis(model, train_data, num_epchos, False)

    ##tuned membership parameters for x0 and mf0
    mfs_print(model)
    print( (time.clock() - time_start)    )  ##computation time check
#    print(model.layer['rules'].mf_indices)      ##print the rule bases you got
#    print(model.layer['rules'].num_rules())     ##print the number of rule bases
    test_data = train_data
    test_anfis(model, test_data, show_plots)
#    plot_final_mfs(model)
#    plot_final_mfs1(model)

    #print(model.layer['consequent']._coeff)
    generate_txt(model)
