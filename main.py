from flask import Flask, Blueprint, Response
from flask import render_template_string
import io
import base64
import asyncio
import threading
import queue
import time

from pymoo.visualization.scatter import Scatter

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

        print("Press enter to start optimization.")
        input() 
        

    def notify(self, algorithm):
        self.data["best"].append(algorithm.pop.get("F").min())
      

        # Send PO update to client
        F = algorithm.pop.get("F")
        plt = Scatter().add(F).show()

        # Set up I/O buffer to save the image 
        buffer = io.BytesIO()

        plt.fig.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)

        # Encode bytes
        plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        msg = self.format_sse(data=plot_base64)
        self.announcer.announce(msg=msg)

        if algorithm.termination.has_terminated():

            print("Press enter to exit")
            input() 


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
    def format_sse(data: str, event=None) -> str:
        """Formats a string and an event name in order to follow the event stream convention.

        >>> format_sse(data=json.dumps({'abc': 123}), event='Jackson 5')
        'event: Jackson 5\\ndata: {"abc": 123}\\n\\n'

        """

        msg = f'data: {data}\n\n'
        if event is not None:
            msg = f'event: {event}\n{msg}'
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

            <div id="po-container"></div>

          </body>

        </html>
        """ % Dashboard.dashboard_js()

        return template

    @staticmethod
    def dashboard_js(): 
        script = """

const evtSource = new EventSource("listen");

evtSource.onmessage = (event) => {
 

  // Create image if it doesn't already exist 
  if(document.getElementById("graph-image")  === null){

    var imageElement = document.createElement('img');

    imageElement.src = "data:image/gif; base64," + event.data

    imageElement.id = "graph-image"

    document.getElementById("po-container").appendChild(imageElement)

  }else{
    document.getElementById("graph-image").src = "data:image/gif; base64," + event.data
  }

};
        """

        return script



problem = get_problem("zdt1")

algorithm = NSGA2(pop_size=100)

res = minimize(problem,
               algorithm,
               ('n_gen', 200),
               seed=1,
               callback=Dashboard(),
               verbose=True)

