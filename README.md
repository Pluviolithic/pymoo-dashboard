# pymoo dashboard

_A tool to display live visualizations of your pymoo projects in real time_

## Development Setup

### Python requirements
You will need to install [Rye](https://rye.astral.sh/guide/installation/):

```shell
curl -sSf https://rye.astral.sh/get | bash
```

Then enter the pymoo-dashboard directory and sync rye:

```shell
rye sync
```

### Node requirements
This project uses Node, Nuxt, and Vue to build its front end UI. So to start:
1. Install Node.js
2. Enter the front end directory `cd frontend`
3. Run `npm install`

## Running for development

To run a sample optimization problem, activate the virtual environment and run `dashboard`.
```
source .venv/bin/activate
dashboard
```

To save the hassle of activating the virtual environment manually, consider installing a shell plugin
like [zsh-autoswitch-virtualenv](https://github.com/MichaelAquilina/zsh-autoswitch-virtualenv).

## Building the project
For Unix based OSes
```
./build.sh
```

## Deploying to pymoo

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
