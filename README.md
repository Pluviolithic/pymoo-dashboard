# pymoo dashboard

_A tool to display live visualizations of your pymoo projects in real time_

## Install for development

### Python requirements
You will need to install Python (and preferably Anaconda). Once your environment is set up, you will need to run:

```shell
pip install pymoo Flask 
```

### Node requirements
Y

## Running for development

```
python Dashboard.py
```



## Integrating into Pymoo projects 

Simply set the Pymoo callback function as `Dashboard()` and you're good to go. 
Make sure the `Dashboard.html`, `Dashboard.js`, and `Dashboard.css` are all in the 
same directory as whereever `Dashboard.py` is deployed to.

## Example: 
```python         
    # create the reference directions to be used for the optimization
    ref_dirs = get_reference_directions("das-dennis", 3, n_partitions=12)

    # create the algorithm object
    algorithm = NSGA3(pop_size=92,
                      ref_dirs=ref_dirs)

    # execute the optimization
    res = minimize(get_problem("dtlz1"),
                   algorithm,
                   seed=2018194,
                   callback=Dashboard(),
                   termination=('n_gen', 600))
```

