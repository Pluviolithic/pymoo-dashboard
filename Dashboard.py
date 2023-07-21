from flask import Flask, Blueprint, Response
from flask import render_template_string
import io
import base64
import asyncio
import threading
import queue
import time


from pymoo.visualization.scatter import Scatter
from pymoo.visualization.pcp import PCP

import matplotlib.pyplot as plt
import numpy as np

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.core.callback import Callback
from pymoo.optimize import minimize


class Dashboard(Callback):

    def __init__(self) -> None:
        super().__init__()
        self.data["best"] = []

        self.announcer = self.MessageAnnouncer()    

        self.flask_thread = threading.Thread(target=self.start_server, daemon=True)
        self.flask_thread.start() 

        self.visualizations = {
            "scatter": Dashboard.plot_scatter,
            "pcp": Dashboard.plot_pcp
                }

        print("Press enter to start optimization.")
        input() 
        

    def notify(self, algorithm):

        # Record PO values 
        self.data["best"].append(algorithm.pop.get("F").min())
   
        for v in self.visualizations: 

            plotter = self.visualizations[v]

            plt = plotter(algorithm)

            # Set up I/O buffer to save the image 
            buffer = io.BytesIO()

            plt.fig.savefig(buffer, format='png', dpi=50)
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
    def plot_scatter(algorithm):

        # Send PO update to client
        F = algorithm.pop.get("F")
        plt = Scatter().add(F).show()
   
        return plt


    @staticmethod
    def plot_pcp(algorithm):

        # Send PO update to client
        F = algorithm.pop.get("F")
        plt = PCP().add(F).show()
   
        return plt

    

    @staticmethod
    def format_sse(data: str, plot_title) -> str:
        """Formats a string and an event name in order to follow the event stream convention.

        >>> format_sse(data=json.dumps({'abc': 123}), event='Jackson 5')
        'event: Jackson 5\\ndata: {"abc": 123}\\n\\n'

        """

        payload = "{\"title\": \"%s\", \"image\": \"%s\"}" % (plot_title, data)


        msg = f'data: {payload}\n\n'

        return msg

    @staticmethod
    def dashboard_template(): 
        template = """
        <!doctype html>

        <html>

          <head>
            <script >
              %s 
            </script>
          </head>

          <body>
            <title>Hello from Flask</title>
            <h1>Hello, Pymoo!</h1>

            <div id="plot-container"></div>

          </body>

        </html>
        """ % Dashboard.dashboard_js()

        return template

    @staticmethod
    def dashboard_js(): 
        script = """

const evtSource = new EventSource("listen");

evtSource.onmessage = (event) => {

  data = JSON.parse(event.data)

  title = data.title

  // Create image if it doesn't already exist 
  if(document.getElementById("graph-image-" + title)  === null){

    // Image wrapper 
    var wrapperElement = document.createElement('div')
    wrapperElement.id = "plot-wrapper-" + title

    // Image element
    var imageElement = document.createElement('img');
    imageElement.src = "data:image/gif; base64," + data.image
    imageElement.id = "graph-image-" + title

    // Title element 
    var header = document.createElement('h2');
    var headerContent = document.createTextNode(title);
    header.appendChild(headerContent);

    // insert data into documeent
    document.getElementById("plot-container").appendChild(wrapperElement)
    document.getElementById("plot-wrapper-" + title).appendChild(header)
    document.getElementById("plot-wrapper-" + title).appendChild(imageElement)




  }else{
    document.getElementById("graph-image-" + title).src = "data:image/gif; base64," + data.image
  }

};
        """

        return script


if __name__ == "__main__": 

    problem = get_problem("zdt2")

    algorithm = NSGA2(pop_size=100)

    res = minimize(problem,
                   algorithm,
                   ('n_gen', 200),
                   seed=1,
                   callback=Dashboard(),
                   verbose=True)

