from math import log
from texttable import Texttable


class DataSet:
    def __init__(self, data):
        self._data = data
        self._entropy = 0
        for feature_value in Feature(data[0].__len__() - 1, data).get_value():
            self._entropy += self.minus_plog_2(feature_value.get_occurrences() / data.__len__() - 1)

    def get_entropy(self):
        return self._entropy

    def get_data(self):
        return self._data

    def __str__(self):
        table = Texttable()
        table.header(self._data[0])
        for i in range(1, self._data.__len__()): table.add_row(self._data[i])
        return table.draw().__str__()

    def minus_plog_2(self, p):
        return_value = 0
        if not p == 0:
            return_value = (-1) * p * log(p, 2)
        return return_value


class Feature:
    def __init__(self, column, data):
        self._name = data[0][column]
        self._value = set()
        for row in range(1, data.__len__()):
            self._value.add(FeatureValue(data[row][column]))
        for featureValue in self._value:
            counter = 0
            for row in range(1, data.__len__()):
                if featureValue.get_name() == data[row][column]:
                    counter += 1
                    featureValue.set_occurrences(counter)

    def get_name(self):
        return self._name

    def get_value(self):
        return self._value

    def __str__(self):
        return self._name


class FeatureValue:
    def __init__(self, name):
        self._name = name
        self._occurrences = 0

    def get_name(self): return self._name

    def get_occurrences(self): return self._occurrences

    def set_occurrences(self, occurrences): self._occurrences = occurrences

    def __str__(self): return self._name

    def __eq__(self, other): return (isinstance(other, FeatureValue)) and (other._name == self._name)

    def __hash__(self): return hash(self._name)


def generate_info_table(featureInfoGain):
    table = Texttable()
    table.header(['Feature', 'Information gain'])
    for key in featureInfoGain:
        table.add_row([key, round(featureInfoGain[key], 5)])
    return table.draw().__str__()


weather = ""
contact = ""


def create_data_set(featureValue, column, data):
    return_data = [[FeatureValue for i in range(data[0].__len__())]
                   for j in range(featureValue.get_occurrences() + 1)]
    return_data[0] = data[0]
    counter = 1
    for row in range(1, data.__len__()):
        if data[row][column] == featureValue.get_name():
            return_data[counter] = data[row]
            counter += 1
    return DataSet([row[:column] + row[column + 1:] for row in return_data])


datas = {"weather": weather, "contact": contact}
for key in datas:
    print(key, "dataset")
    dataSet = DataSet(datas[key])
    print(dataSet)
    featureInfoGain = {}
    for column in range(0, dataSet.get_data()[0].__len__() - 1):
        feature = Feature(column, dataSet.get_data())
        dataSets = [DataSet for i in range(feature.get_value().__len__())]
        i = 0
        for featureValue in feature.get_value():
            dataSet[i] = create_data_set(featureValue, column, dataSet.get_data())
            i += 1
    summation = 0
    for i in range(0, dataSets.__len__()):
        summation += (((dataSets[i].get_data()).__len__() - 1) /
                      (dataSet.get_data().__len__() - 1)) * dataSets[i].get_entropy()
    featureInfoGain[feature] = dataSet.get_entropy() - summation
