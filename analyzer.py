import requests as r
import time

from neuralNetwork import NeuralNetwork


def normalize(p, m, M):
    return ((2 * p - (M + m)) / (M - m))


def denormalize(p, m, M):
    return (((p * (M - m)) / 2) + (M + m)) / 2


def rolling_window(seq, size):
    it = iter(seq)
    win = [next(it) for cnt in [0] * size]
    yield win

    for elem in it:  # Subsequent windows
        win[:-1] = win[1:]
        win[-1] = elem
        yield win


def mavg(vals, size):
    return [sum(w) / len(w) for w in rolling_window(vals, size)]


def mins(vals, size):
    return [min(w) for w in rolling_window(vals, size)]


def maxs(vals, size):
    return [max(w) for w in rolling_window(vals, size)]


def get_timeseries(vals, win):
    mavg_ = mavg(vals, win)
    mins_ = mins(vals, win)
    maxs_ = maxs(vals, win)

    returnData = []

    # build items of the form [[average, minimum, maximum], normalized price]
    for a, m, M, idx in zip(mavg_, mins_, maxs_, range(len(mavg_))):
        inputN = [a, m, M]
        price = normalize(vals[len(mavg_) - (idx + 1)], m, M)
        outN = [price]

        returnData.append([inputN, outN])

    return returnData


def get_historical(ticker):
    historicalPrices = []

    r.get("http://api.kibot.com/?action=login&user=guest&password=guest")

    # get 14 days of data from API (business days only, could be < 10)
    url = "http://api.kibot.com/?action=history&symbol={}&interval=daily&period=50&unadjusted=1&startDate=1/25/2016".format(
        ticker)

    apiData = r.get(url).text.split("\n")
    # print(apiData)

    for line in apiData:
        if line:
            try:
                tempLine = line.split(',')
                price = float(tempLine[1])
                historicalPrices.append(price)
            except Exception:
                pass

    return historicalPrices


def get_training(ticker):
    historical_data = get_historical(ticker)[::-1]
    trainingData = get_timeseries(historical_data, 5)

    return trainingData


def get_prediction(ticker):
    hist = get_historical(ticker)[::-1][-5:]
    # hist = data[-5:]

    # get five 5-day moving averages, 5-day lows, and 5-day highs
    pred = get_timeseries(hist, 5)
    # print pred
    return pred[0][0]

nn = NeuralNetwork()

def analyzeSymbol(ticker):
    data = get_historical(ticker)
    trainingData = get_training(data)

    nn = NeuralNetwork()
    nn.train(trainingData)

    # get rolling data for most recent day
    prediction_data = get_prediction(ticker)
    returnPrice = nn.test(prediction_data)

    confidence = returnPrice

    # print(prediction_data)
    predicted_price = denormalize(
        returnPrice, prediction_data[1], prediction_data[2])

    return predicted_price, abs(confidence)
