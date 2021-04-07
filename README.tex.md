# hr-graphs-ph
geometric graphs based on a [Hertzsprung–Russell diagram](https://en.wikipedia.org/wiki/Hertzsprung%E2%80%93Russell_diagram) and their corresponding persistent homology graph families
___

an H-R diagram (which is obtainable from [this](https://github.com/izzorts/hr-graphs-ph/blob/master/original%20code%20and%20data/simple_plot_9_python.py)):

![hr diagram](https://github.com/izzorts/hr-graphs-ph/blob/master/outputs/HRdiagram.png)

a slightly deformed (minmax scaled and rotated), otherwise common H-R diagram, which is one of the outputs of `HR_graph.ipynb`:

![transformed hr diagram](https://github.com/izzorts/hr-graphs-ph/blob/master/outputs/hrdiag.png)

and its corresponding "H-R graph", which is a geometric graph based on the stars' magnitudes and luminosities, for a suitable distance threshold:

![hr graph](https://github.com/izzorts/hr-graphs-ph/blob/master/outputs/hrgraph.png)

by varying this threshold we obtain graphs for different spatial resolutions (see [persistent homology](https://en.wikipedia.org/wiki/Persistent_homology)), yielding the following gif:

![hr ph gif](https://github.com/izzorts/hr-graphs-ph/blob/master/outputs/output.gif)

A [geometrical graph, or spatial network](https://en.wikipedia.org/wiki/Spatial_network), is a graph whose vertices are associated with spatial elements, i.e., with elements pertaining to some metric space $M = (S, d)$, where $S$ is a set and $d$ is a metric over $S$. In this case, in particular, we used $d = \mathcal{l}_2$.
