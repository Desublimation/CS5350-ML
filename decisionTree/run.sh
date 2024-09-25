#!/bin/bash
python3 DecisionTree.py ./car/train.csv 1 0
python3 DecisionTree.py ./car/train.csv 2 0
python3 DecisionTree.py ./car/train.csv 3 0
python3 DecisionTree.py ./car/train.csv 4 0
python3 DecisionTree.py ./car/train.csv 5 0
python3 DecisionTree.py ./car/train.csv 6 0

python3 DecisionTree.py ./car/train.csv 1 1
python3 DecisionTree.py ./car/train.csv 2 1
python3 DecisionTree.py ./car/train.csv 3 1
python3 DecisionTree.py ./car/train.csv 4 1
python3 DecisionTree.py ./car/train.csv 5 1
python3 DecisionTree.py ./car/train.csv 6 1

python3 DecisionTree.py ./car/train.csv 1 2
python3 DecisionTree.py ./car/train.csv 2 2
python3 DecisionTree.py ./car/train.csv 3 2
python3 DecisionTree.py ./car/train.csv 4 2
python3 DecisionTree.py ./car/train.csv 5 2
python3 DecisionTree.py ./car/train.csv 6 2

# predict:
python3 prediction.py