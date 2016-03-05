import math
import random


def rand(a, b):
    return (b - a) * random.random() + a


def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill] * J)
    return m


def sigmoid(x):
    return math.tanh(x)


def dsigmoid(y):
    return 1.0 - y**2


class NeuralNetwork:
    def __init__(self, inputN=3, hiddenN=20, outputN=1):
        # number of input, hidden, and output nodes
        self.inputN = inputN + 1  # +1 for bias node
        self.hiddenN = hiddenN
        self.outputN = outputN

        # activations for nodes
        self.inputA = [1.0] * self.inputN
        self.hiddenA = [1.0] * self.hiddenN
        self.outputA = [1.0] * self.outputN

        # create weights
        self.inputW = makeMatrix(self.inputN, self.hiddenN)
        self.outputW = makeMatrix(self.hiddenN, self.outputN)

        # set them to random vaules
        for i in range(self.inputN):
            for j in range(self.hiddenN):
                self.inputW[i][j] = rand(-0.2, 0.2)

        for j in range(self.hiddenN):
            for k in range(self.outputN):
                self.outputW[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum
        self.ci = makeMatrix(self.inputN, self.hiddenN)
        self.co = makeMatrix(self.hiddenN, self.outputN)

    def update(self, inputs):
        if len(inputs) != self.inputN - 1:
            raise ValueError('wrong number of inputs')

        # input activations
        for i in range(self.inputN - 1):
            self.inputA[i] = inputs[i]

        # hidden activations
        for j in range(self.hiddenN):
            sum = 0.0
            for i in range(self.inputN):
                sum = sum + self.inputA[i] * self.inputW[i][j]
            self.hiddenA[j] = sigmoid(sum)

        # output activations
        for k in range(self.outputN):
            sum = 0.0
            for j in range(self.hiddenN):
                sum = sum + self.hiddenA[j] * self.outputW[j][k]
            self.outputA[k] = sigmoid(sum)

        return self.outputA[:]

    def backPropagate(self, targets, N, M):
        if len(targets) != self.outputN:
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        output_deltas = [0.0] * self.outputN
        for k in range(self.outputN):
            error = targets[k] - self.outputA[k]
            output_deltas[k] = dsigmoid(self.outputA[k]) * error

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.hiddenN
        for j in range(self.hiddenN):
            error = 0.0
            for k in range(self.outputN):
                error = error + output_deltas[k] * self.outputW[j][k]
            hidden_deltas[j] = dsigmoid(self.hiddenA[j]) * error

        # update output weights
        for j in range(self.hiddenN):
            for k in range(self.outputN):
                change = output_deltas[k] * self.hiddenA[j]
                self.outputW[j][k] = self.outputW[
                    j][k] + N * change + M * self.co[j][k]
                self.co[j][k] = change

        # update input weights
        for i in range(self.inputN):
            for j in range(self.hiddenN):
                change = hidden_deltas[j] * self.inputA[i]
                self.inputW[i][j] = self.inputW[
                    i][j] + N * change + M * self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        return sum(0.5 * (targets[k] -
                          self.outputA[k]) ** 2 for k in range(len(targets)))

    def test(self, inputN):
        print(inputN, '->', self.update(inputN))
        return self.update(inputN)[0]

    def weights(self):
        pass
        # print('Input weights: {}'.format(self.inputW))
        # print('Output weights: {}'.format(self.outputW))

    def train(self, patterns, iter=10000, N=0.05, M=0.05):
        # N: learning rate, M: momentum factor
        for i in range(iter):
            # print(i)
            error = 0.0
            for p in patterns:
                self.update(p[0])
                error = error + self.backPropagate(p[1], N, M)
            if not i % 100:
                print("Epoch: {} => Error: {}".format(i + 100, error))
        