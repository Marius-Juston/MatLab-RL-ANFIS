#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    ANFIS in torch: some simple functions to supply data and plot results.
    @author: James Power <james.power@mu.ie> Apr 12 18:13:10 2019
"""

import matplotlib.pyplot as plt
import time
import torch
import torch.nn.functional as F

dtype = torch.float

def mfs_print(model):
    for i in range(len(model.input_keywords)):
        for j in range(model.number_of_mfs[model.input_keywords[i]]):
            print(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf{}'.format(j)].pretty())


def _mk_param(val):
    '''Make a torch parameter from a scalar value'''
    if isinstance(val, torch.Tensor):
        val = val.item()
    return torch.nn.Parameter(torch.tensor(val, dtype=torch.float))

def averaging(model,input):
    #far
    left = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf1'].a.item())
    right = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf3'].d.item())
    avg = (left + right) / 2
    left = -avg
    right = avg
    with torch.no_grad():
        model.layer['fuzzify'].varmfs[input].mfdefs['mf1'].a.copy_(torch.tensor(left,dtype=torch.float))
        model.layer['fuzzify'].varmfs[input].mfdefs['mf3'].d.copy_(torch.tensor(right,dtype=torch.float))

    #close far
    left = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf1'].b.item())
    right = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf3'].c.item())
    avg = (left + right) / 2
    left = -avg
    right = avg
    with torch.no_grad():
        model.layer['fuzzify'].varmfs[input].mfdefs['mf1'].b.copy_(torch.tensor(left,dtype=torch.float))
        model.layer['fuzzify'].varmfs[input].mfdefs['mf3'].c.copy_(torch.tensor(right,dtype=torch.float))

    #near
    left = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].a.item())
    right = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].d.item())
    avg = (left + right) / 2
    left = -avg
    right = avg
    with torch.no_grad():
        model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].a.copy_(torch.tensor(left,dtype=torch.float))
        model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].d.copy_(torch.tensor(right,dtype=torch.float))

    #close_near
    left = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].b.item())
    right = abs(model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].c.item())
    avg = (left + right) / 2
    left = -avg
    right = avg
    with torch.no_grad():
        model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].b.copy_(torch.tensor(left,dtype=torch.float))
        model.layer['fuzzify'].varmfs[input].mfdefs['mf2'].c.copy_(torch.tensor(right,dtype=torch.float))

def mfs_constraint(model):

    for i in range(len(model.input_keywords)):
        for j in range(model.number_of_mfs[model.input_keywords[i]]):
            averaging(model, model.input_keywords[i])

            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf0'].c = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf1'].a.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf0'].d = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf1'].b.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf1'].c = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf2'].a.item())

            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf1'].d = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf2'].b.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf3'].a = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf2'].c.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf3'].b = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf2'].d.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf4'].a = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf3'].c.item())
            model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf4'].b = torch.tensor(model.layer['fuzzify'].varmfs[model.input_keywords[i]].mfdefs['mf3'].d.item())


class TwoLayerNet(torch.nn.Module):
    '''
        From the pytorch examples, a simjple 2-layer neural net.
        https://pytorch.org/tutorials/beginner/pytorch_with_examples.html
    '''
    def __init__(self, d_in, hidden_size, d_out):
        super(TwoLayerNet, self).__init__()
        self.linear1 = torch.nn.Linear(d_in, hidden_size)
        self.linear2 = torch.nn.Linear(hidden_size, d_out)

    def forward(self, x):
        h_relu = self.linear1(x).clamp(min=0)
        y_pred = self.linear2(h_relu)
        return y_pred



def linear_model(x, y, epochs=200, hidden_size=10):
    '''
        Predict y from x using a simple linear model with one hidden layer.
        https://pytorch.org/tutorials/beginner/pytorch_with_examples.html
    '''
    assert x.shape[0] == y.shape[0], 'x and y have different batch sizes'
    d_in = x.shape[1]
    d_out = y.shape[1]
    model = TwoLayerNet(d_in, hidden_size, d_out)
    criterion = torch.nn.MSELoss(reduction='sum')
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)
    errors = []
    for t in range(epochs):
        y_pred = model(x)
        tot_loss = criterion(y_pred, y)
        perc_loss = 100. * torch.sqrt(tot_loss).item() / y.sum()
        errors.append(perc_loss)
        if t % 10 == 0 or epochs < 20:
            print('epoch {:4d}: {:.5f} {:.2f}%'.format(t, tot_loss, perc_loss))
        optimizer.zero_grad()
        tot_loss.backward()
        optimizer.step()
    return model, errors


def plotErrors(errors):
    '''
        Plot the given list of error rates against no. of epochs
    '''
    plt.plot(range(len(errors)), errors, '-ro', label='errors')
    plt.ylabel('Percentage error')
    plt.xlabel('Epoch')
    plt.show()


def plotResults(y_actual, y_predicted):
    '''
        Plot the actual and predicted y values (in different colours).
    '''
    plt.plot(range(len(y_predicted)), y_predicted.detach().numpy(),
             'r', label='trained')
    plt.plot(range(len(y_actual)), y_actual.numpy(), 'b', label='original')
    plt.legend(loc='upper left')
    plt.show()


def _plot_mfs(var_name, fv, model):
    '''
        A simple utility function to plot the MFs for a variable.
        Supply the variable name, MFs and a set of x values to plot.
    '''
    # Sort x so we only plot each x-value once:
    #xsort, _ = x.sort()
#    for mfname, yvals in fv.fuzzify(xsort):
#        temp = 'mf5'
#        if (mfname == temp) is False:
#            plt.plot(xsort.tolist(), yvals.tolist(), label=mfname)
    zero_length = (model.number_of_mfs[var_name])
    x = torch.zeros(10000)
    y = -5
    for i in range(10000):
        x[i] = torch.tensor(y)
        y += 0.001
    for mfname, yvals in fv.fuzzify(x):
#        print(mfname)
#        print(yvals)
        temp = 'mf{}'.format(zero_length)
        if (mfname == temp) is False:
            plt.plot(x, yvals.tolist(), label=mfname)

    plt.xlabel('Values for variable {} ({} MFs)'.format(var_name, fv.num_mfs))
    plt.ylabel('Membership')
    plt.legend(bbox_to_anchor=(1., 0.95))
    plt.show()


def plot_all_mfs(model, x):
    for i, (var_name, fv) in enumerate(model.layer.fuzzify.varmfs.items()):
        #_plot_mfs(var_name, fv, x[:, i])
        _plot_mfs(var_name, fv, model)


def calc_error(y_pred, y_actual):
    #change 0 to 1e-12
    with torch.no_grad():
        tot_loss = F.mse_loss(y_pred, y_actual)
        rmse = torch.sqrt(tot_loss).item()
        perc_loss = torch.mean(100. * torch.abs((y_pred - y_actual)
                               / y_actual))
    #    perc_loss = 0.1
        ss_total = torch.sum((y_actual - torch.mean(y_actual))**2)
        ss_regression = torch.sum((y_actual - y_pred)**2)
        rsq = (1 - (ss_regression / ss_total)) * 100
    return(tot_loss, rmse, perc_loss,rsq)


def test_anfis(model, data, show_plots=False):
    '''
        Do a single forward pass with x and compare with y_actual.
    '''
    x, y_actual = data.dataset.tensors
    if show_plots:
        plot_all_mfs(model, x)
    print('### Testing for {} cases'.format(x.shape[0]))
    y_pred = model(x)
    mse, rmse, perc_loss, rsq= calc_error(y_pred, y_actual)
    print('MSE={:.5f}, RMSE={:.5f} ={:.2f}%, RSQ ={:.2f}% '
          .format(mse, rmse, perc_loss,rsq))
    if show_plots:
        plotResults(y_actual, y_pred)


def train_anfis_with(model, data, optimizer, criterion,
                     epochs=500, show_plots=False):
    '''
        Train the given model using the given (x,y) data.
    '''
    if show_plots:
        plot_all_mfs(model, data.dataset.tensors[0])
    temp = []
    temp1 = []
    temp2 = []
    errors = []  # Keep a list of these for plotting afterwards
    print('### Training for {} epochs, training size = {} cases'.
          format(epochs, data.dataset.tensors[0].shape[0]))
    for t in range(epochs):
        # Process each mini-batch in turn:
        #do like model.layer['fuzzify'].varmfs['x0'].mfdefs['mf0'].b
        #  = model.layer['fuzzify'].varmfs['x0'].mfdefs['mf0'].a to make symmetric
        for x, y_actual in data:
            y_pred = model(x)
            # Compute and print loss
            loss = criterion(y_pred, y_actual)
            # Zero gradients, perform a backward pass, and update the weights.
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # Epoch ending, so now fit the coefficients based on all data:

        #mfs_print(model)
        #print(list(model.parameters()))
        x, y_actual = data.dataset.tensors
        mfs_constraint(model)
    #    with torch.no_grad():
    #        model.fit_coeff(x, y_actual)
        #print(model.layer['consequent'].coefficients)

        #if t == 5:
            #model.layer['consequent'].coefficients = torch.nn.Parameter(torch.zeros(torch.Size([25, 1, 4]), dtype=dtype, requires_grad=True))
            #self._coeff = torch.zeros(torch.Size([25, 1, 4]), dtype=dtype, requires_grad=True)

        # Get the error rate for the whole batch:
        y_pred = model(x)
        mse, rmse, perc_loss, rsq = calc_error(y_pred, y_actual)
        errors.append(perc_loss)
        # Print some progress information as the net is trained:
    #    print(model.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf2'].b.requires_grad)
    #    print(model.layer['fuzzify'].varmfs['theta_near'].mfdefs['mf2'].pretty())
        temp.append(mse.item())
        time123 = ( (time.clock() - 0.5)    )
        temp1.append(time123)
        temp2.append(rsq.item())
        mfs_print(model)
        if epochs < 30 or t % 10 == 0:
            print('epoch {:4d}: MSE={:.5f}, RMSE={:.5f} ={:.2f}%, RSQ ={:.2f}% '
                  .format(t, mse, rmse, perc_loss,rsq))
        #    print(perc_loss)
    # End of training, so graph the results:

    with open("mse.txt", 'w') as output:
        for row in temp:
            output.write(str(row) + '\n')
    with open("time.txt", 'w') as output:
        for row in temp1:
            output.write(str(row) + '\n')
    with open("rsq.txt", 'w') as output:
        for row in temp2:
            output.write(str(row) + '\n')

    if show_plots:
        plotErrors(errors)
        y_actual = data.dataset.tensors[1]
        y_pred = model(data.dataset.tensors[0])
        plotResults(y_actual, y_pred)


def train_anfis(model, data, epochs=500, show_plots=False):
    '''
        Train the given model using the given (x,y) data.
    '''
    #x, y_actual = data.dataset.tensors
    #if show_plots:
    #    plot_all_mfs(model, x)
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-4, momentum=0.99)
    # optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    criterion = torch.nn.MSELoss(reduction='sum')
#    print(model.parameters())
    train_anfis_with(model, data, optimizer, criterion, epochs, show_plots)


if __name__ == '__main__':
    x = torch.arange(1, 100, dtype=dtype).unsqueeze(1)
    y = torch.pow(x, 3)
    model, errors = linear_model(x, y, 100)
    plotErrors(errors)
    plotResults(y, model(x))
