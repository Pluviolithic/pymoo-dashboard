from flask import Flask, Blueprint
from flask import render_template
import io
import base64
import asyncio
import threading
#
# TODO delete these eventually
from pymoo.visualization.scatter import Scatter
from pymoo.problems import get_problem
# end delete these 

import matplotlib.pyplot as plt
import numpy as np

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.problems import get_problem
from pymoo.core.callback import Callback
from pymoo.optimize import minimize


class MyCallback(Callback):

    def __init__(self) -> None:
        super().__init__()
        self.data["best"] = []

        self.flask_thread = threading.Thread(target=self.start_server, daemon=True)
        self.flask_thread.start() 

    def notify(self, algorithm):
        self.data["best"].append(algorithm.pop.get("F").min())
       
        if algorithm.termination.has_terminated():
            print("Press any key and enter to exit")
            input() 


    def start_server(self):
        # Set up blueprints to organize routes
        self.app = Flask(__name__)        

        blue_print = Blueprint('blue_print', __name__)
        blue_print.add_url_rule('/', view_func=self.dash_home)

        self.app.register_blueprint(blue_print)
        self.app.run() 

    def dash_home(self):

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

problem = get_problem("sphere")

algorithm = GA(pop_size=100)

res = minimize(problem,
               algorithm,
               ('n_gen', 20),
               seed=1,
               callback=MyCallback(),
               verbose=True)

