### Overall Summary:
For this assignment, I created two files: ‘synthetic-decision-tree.py’ and ‘video-games-decision-tree.py’. The first, is to be directed towards the ‘synthetic-1.csv’, ‘synthetic-2.csv’, ‘synthetic-3.csv’, and ‘synthetic-4.csv’ files, while the latter is to be directed towards the ‘Video_Games_Sales.csv’ file. Implementation-wise, both programs ultimately have the same major steps to creating the decision tree. First, entropy is calculated in order to find the highest information gain among the attributes. Then, using this information, the data is split into bins. The ID3 function is recursively called for each bin, allowing the program to repeat the last steps until an edge case is hit. Such edge cases include when there are no other attributes left and when all the class labels for an attribute are the same.

### Synthetic Decision Tree:
In order to discretize the data of the ‘synthetic’ .csv files, I plotted the data of the two attributes and analyzed a somewhat average boundary to split the data into two bins. To comprehend every step of my program, I did hardcode quite a bit (an example being the boundaries). The ‘synthetic-decision-tree.py’ program allows the user to either input a coordinate of data or an entire .csv file with two columns of data. It will then output the predicted values of the given attributes. In addition, the program creates a graph for the data, in which the circular coordinate points are colored according to their actual class labels, while the background colors are the predictions of class labels in the bordered region. The graphs are illustrated below. In addition, I added test files of each synthetic set of data, which are the same as the training data, excluding the class labels. 

The errors of each set of data are the following:
synthetic-1.csv error: 0.0%
synthetic-2.csv error: 12.99%
synthetic-3.csv error: 17.65%
synthetic-4.csv error: 62.6%

Imported libraries for this file include:
import csv
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from pylab import *
from matplotlib.patches import Rectangle
import copy

### Video Games Decision Tree
Contrary to the synthetic decision tree program, I discretized the floating point data columns provided in the ‘Video-Games-Sales.csv’ by 10 bins, each including the same number of examples. I did not include the rows of data missing information. Furthermore, I was able to complete and store the decision tree; however, did not have time to traverse and calculate the error. 

Imported libraries for this file include:
import csv
import math
import time


