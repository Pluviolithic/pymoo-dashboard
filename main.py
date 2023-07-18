
from flask import Flask
from flask import render_template
import io
import base64

# TODO delete these eventually
from pymoo.visualization.scatter import Scatter
from pymoo.problems import get_problem

import numpy as np

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.util.display.column import Column
from pymoo.util.display.output import Output

app = Flask(__name__)

@app.route('/')
def main():

    # Get demo code 
    F = get_problem("zdt3").pareto_front()
    plt = Scatter().add(F).show()

    # Set up I/O buffer to save the image 
    buffer = io.BytesIO()

    plt.fig.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)

    # Encode bytes
    plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    return render_template('app.html', image=plot_base64)


class MyOutput(Output):

    def __init__(self):
        super().__init__()
        self.x_mean = Column("x_mean", width=13)
        self.x_std = Column("x_std", width=13)
        self.columns += [self.x_mean, self.x_std]

        

        app.run() 
         

    def update(self, algorithm):
        super().update(algorithm)
        self.x_mean.set(np.mean(algorithm.pop.get("X")))
        self.x_std.set(np.std(algorithm.pop.get("X")))


problem = get_problem("zdt2")

algorithm = NSGA2(pop_size=100)

res = minimize(problem,
               algorithm,
               ('n_gen', 200),
               seed=1,
               output=MyOutput(),
               verbose=True)





