#!/bin/bash
python3 DecisionTree.py ./car/train.csv 6 0
python3 DecisionTree.py ./car/train.csv 6 1
python3 DecisionTree.py ./car/train.csv 6 2

python3 prediction.py ./car/test.csv 0
python3 prediction.py ./car/test.csv 1
python3 prediction.py ./car/test.csv 2
# python3 DecisionTree.py ./car/test.csv 2 0
# python3 DecisionTree.py ./car/test.csv 3 0
# python3 DecisionTree.py ./car/test.csv 4 0