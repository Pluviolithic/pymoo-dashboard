from flask import Flask, Blueprint, Response
from flask import render_template_string
import io
import base64
import asyncio
import threading
import queue
import time
import json

from pymoo.visualization.scatter import Scatter
from pymoo.visualization.pcp import PCP

import matplotlib.pyplot as plt
import numpy as np

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.core.callback import Callback
from pymoo.optimize import minimize
from pymoo.indicators.hv import Hypervolume


class Dashboard(Callback):

    def __init__(self) -> None:
        super().__init__()
        self.data["HV"] = []

        self.announcer = self.MessageAnnouncer()    

        self.flask_thread = threading.Thread(target=self.start_server, daemon=True)
        self.flask_thread.start() 

        self.visualizations = {
            "HV": self.plot_hv,
            "Pareto Front Scatter Plot": self.plot_scatter,
            "PCP Plot": self.plot_pcp
                }

        # Initially chosen HV point
        self.hv_ref_point  =  np.array([1, 1])

        self.overview_fields = ['algorithm', 'problem', 'generation', 'seed', 'pop_size']

        print("Press enter to start optimization.")
        input() 
        

    def notify(self, algorithm):

        ## Book keeping

        # PO values 
        pf = algorithm.pop.get("F")

        # HV values 
        hv_indicator = Hypervolume(ref_point=self.hv_ref_point)
        self.data["HV"].append(hv_indicator.do(pf))


        ## Overview table
        # Build the data for the overview table
        overview_dict = {}

        for o in self.overview_fields:

            overview_func =  getattr(self, "overview_" + o)

            overview_dict[o] = overview_func(algorithm)

        msg = self.format_sse(overview_dict, "Overview")

        # Send off overview table
        self.announcer.announce(msg=msg)

        
        ## Dashboard tables
        for v in self.visualizations: 

            plotter = self.visualizations[v]

            fig = plotter(algorithm)

            # Set up I/O buffer to save the image 
            buffer = io.BytesIO()

            fig.savefig(buffer, format='png', dpi=100)
            buffer.seek(0)

            # Encode bytes
            plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')

            msg = self.format_sse(plot_base64, v)
            
            self.announcer.announce(msg=msg)


    def start_server(self):
        # Set up blueprints to organize routes
        self.app = Flask(__name__)        

        blue_print = Blueprint('blue_print', __name__)
        blue_print.add_url_rule('/', view_func=self.dash_home)
        blue_print.add_url_rule('/listen', view_func=self.listen)

        self.app.register_blueprint(blue_print)
        self.app.run() 


    # SSE listeners
    def listen(self):

        def stream():
            messages = self.announcer.listen()  # returns a queue.Queue
            while True:
                msg = messages.get()  # blocks until a new message arrives
                yield msg

        return Response(stream(), mimetype='text/event-stream')

    # Dashboard homepage
    def dash_home(self):

        return render_template_string(self.dashboard_template())


    # SSE code taken from https://github.com/MaxHalford/flask-sse-no-deps
    class MessageAnnouncer:

        def __init__(self):
            self.listeners = []

        def listen(self):
            self.listeners.append(queue.Queue(maxsize=5))
            return self.listeners[-1]

        def announce(self, msg):
            # We go in reverse order because we might have to delete an element, which will shift the
            # indices backward
            for i in reversed(range(len(self.listeners))):
                try:
                    self.listeners[i].put_nowait(msg)
                except queue.Full:
                    del self.listeners[i]


    @staticmethod
    def format_sse(content, plot_title) -> str:
        """Formats a string and an event name in order to follow the event stream convention.

        >>> format_sse(data=json.dumps({'abc': 123}), event='Jackson 5')
        'event: Jackson 5\\ndata: {"abc": 123}\\n\\n'

        """

        if isinstance(content, dict):
            payload = "{\"title\": \"%s\", \"content\": %s}" % (plot_title, json.dumps(content))
        elif isinstance(content, str): 
            payload = "{\"title\": \"%s\", \"content\": \"%s\"}" % (plot_title, content)
        else: 
            raise TypeError("Wrong data given to format_sse")


        msg = f'data: {payload}\n\n'

        return msg

    @staticmethod
    def dashboard_template(): 
    
        template = Dashboard.read_source_file("Dashboard.html")        

        template = template % (Dashboard.dashboard_js(), Dashboard.dashboard_css())

        return template

    @staticmethod
    def dashboard_js(): 

        script = Dashboard.read_source_file("Dashboard.js")        

        return script

    @staticmethod
    def dashboard_css(): 

        script = Dashboard.read_source_file("Dashboard.css")

        return script


    @staticmethod
    def read_source_file(file_path): 

        with open(file_path, 'r') as file:
        
            file_content = file.read()

        return file_content

    ## Dashboard plots
    def plot_scatter(self, algorithm):

        # Send PO update to client
        F = algorithm.pop.get("F")
        plot = Scatter().add(F).show()
   
        return plot.fig


    def plot_pcp(self, algorithm):

        # Send PO update to client
        F = algorithm.pop.get("F")
        plot = PCP().add(F).show()
   
        return plot.fig


    def plot_hv(self, algorithm):

        # Send PO update to client
        hv_series = self.data["HV"]
        gen_series = list(range(len(hv_series)))

        plt.figure(figsize=(7,7))
        plt.plot(gen_series, hv_series)
        plot = plt.gcf() 

        return plot
        
    ## Overview functions
    @staticmethod
    def overview_problem(algorithm):
        return type(algorithm.problem).__name__

    @staticmethod
    def overview_algorithm(algorithm):
        return type(algorithm).__name__

    @staticmethod
    def overview_generation(algorithm):
        return algorithm.n_gen

    @staticmethod
    def overview_seed(algorithm):
        return algorithm.seed

    @staticmethod
    def overview_pop_size(algorithm):
        return len(algorithm.pop)

if __name__ == "__main__": 

    problem = get_problem("zdt2")

    algorithm = NSGA2(pop_size=100)

    res = minimize(problem,
                   algorithm,
                   ('n_gen', 200),
                   seed=1,
                   callback=Dashboard(),
                   verbose=True)

