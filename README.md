# hr-graphs-ph
geometric graphs based on a [Hertzsprung–Russell diagram](https://en.wikipedia.org/wiki/Hertzsprung%E2%80%93Russell_diagram) and their corresponding persistent homology graph families
___

an HR diagram (which is obtainable from [this](https://github.com/izzorts/hr-graphs-ph/blob/master/original%20code%20and%20data/simple_plot_9_python.py)):

![hr diagram](https://github.com/izzortsi/hr-graphs-ph/blob/master/src/outputs/HR_diag.png)

by constructing a geometric graph using the original HR diagram, while still helding the points fixed, we obtain the following: 

![hr_diagram2](https://github.com/izzortsi/hr-graphs-ph/blob/master/src/outputs/HR_diag_edges_0.09.png)

if we now let loose of the points coordinates and let adjacency between vertices guide the layout of the graph we obtain one of what we call its corresponding "HR graph", for a suitable distance threshold:

![hr graph1](https://github.com/izzortsi/hr-graphs-ph/blob/master/src/outputs/HR_sfdp0.001.png)

for different such thresholds:
![hr graph2](https://github.com/izzortsi/hr-graphs-ph/blob/master/src/outputs/HR_sfdp0.03.png)

and

![hr graph3](https://github.com/izzortsi/hr-graphs-ph/blob/master/src/outputs/HR_sfdp0.05.png)

and

![hr graph4](https://github.com/izzortsi/hr-graphs-ph/blob/master/src/outputs/HR_sfdp0.09.png)

finally, by varying this threshold we obtain a sequence of graphs for different spatial resolutions (see [persistent homology](https://en.wikipedia.org/wiki/Persistent_homology)), yielding the following animation:

![hr ph gif](https://github.com/izzortsi/hr-graphs-ph/blob/master/src/outputs/hrph.gif)

