import base64
import io
import json
import os
import threading
import time
import webbrowser

import matplotlib.pyplot as plt
from flask import Flask, request
from flask_socketio import SocketIO
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.core.callback import Callback
from pymoo.indicators.hv import Hypervolume
from pymoo.optimize import minimize
from pymoo.problems import get_problem
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.visualization.pcp import PCP
from pymoo.visualization.scatter import Scatter


class Dashboard(Callback):
    def __init__(self, open_browser=False, develop=False, **kwargs) -> None:
        super().__init__()
        self.data["HV"] = []
        self.paused = False
        self.announcer = self.MessageAnnouncer()
        self.flask_thread = threading.Thread(target=self.start_server, daemon=True)
        self.flask_thread.start()

        self.develop = develop

        url = "localhost"
        if develop:
            url += ":3000"
            self.develop_thread = threading.Thread(target=self.start_dev_server)
            self.develop_thread.start()
        else:
            url += ":5000"

        if open_browser:
            threading.Timer(1.25, lambda: webbrowser.open(url)).start()

        # Default visualizations + user defined ones
        self.visualizations = dict(
            {
                "HV": self.plot_hv,
                "Pareto Front Scatter Plot": self.plot_scatter,
                "PCP Plot": self.plot_pcp,
            },
            **kwargs,
        )

        # User defined visualizations
        self.overview_fields = [
            "algorithm",
            "problem",
            "generation",
            "seed",
            "pop_size",
        ]

    def start_dev_server(self):
        # Go to the path "nuxt-module"
        os.chdir("frontend")

        # Run the development server
        os.system("npm run dev")

    def notify(self, algorithm):
        while self.paused:
            time.sleep(1)
        # PO values
        pf = algorithm.pop.get("F")

        # HV reference point
        self.hv_ref_point = algorithm.problem.nadir_point()
        if self.hv_ref_point is None:
            self.hv_ref_point = [1 for a in range(algorithm.problem.n_obj)]

        # HV values
        hv_indicator = Hypervolume(ref_point=self.hv_ref_point)
        self.data["HV"].append(hv_indicator.do(pf))

        ## Overview table
        # Build the data for the overview table
        overview_dict = {}

        for o in self.overview_fields:
            overview_func = getattr(self, "overview_" + o)

            overview_dict[o] = overview_func(algorithm)

        # Send off overview table
        self.announcer.announce(plot_title="Overview", content=overview_dict)

        ## Dashboard tables
        for v in self.visualizations:
            plotter = self.visualizations[v]

            fig = plotter(self, algorithm)

            # Set up I/O buffer to save the image
            buffer = io.BytesIO()

            fig.savefig(buffer, format="png", dpi=100)

            plt.close(fig)

            buffer.seek(0)

            # Encode bytes
            plot_base64 = base64.b64encode(buffer.read()).decode("utf-8")

            self.announcer.announce(plot_title=v, content=plot_base64)

    def start_server(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        @self.app.route("/pause", methods=["POST"])
        def pause():
            self.paused = not self.paused
            self.announcer.pause(self.paused)
            if self.paused:
                return "Paused"
            else:
                return "Unpaused"

        @self.socketio.event
        def connect():
            print(f"Client {request.sid} connected")
            self.announcer.set_socketio(self.socketio, request.sid, self.paused)

        @self.socketio.event
        def disconnect():
            print("Client disconnected")

        self.socketio.run(self.app, port=5000)

    class MessageAnnouncer:
        def __init__(self):
            self.socketio = None
            self.historical = []

        def set_socketio(self, socketio, sid, paused):
            if not self.socketio:
                self.socketio = socketio
            self.socketio.emit(
                "initial_data", {"msg": json.dumps(self.historical)}, room=sid
            )
            self.socketio.emit("pause", {"msg": json.dumps(paused)})

        def announce(self, plot_title, content):
            self.historical.append({"title": plot_title, "content": content})
            if self.socketio:
                self.socketio.emit(
                    "update",
                    {"msg": json.dumps({"title": plot_title, "content": content})},
                )

        def pause(self, paused):
            if self.socketio:
                self.socketio.emit("pause", {"msg": json.dumps(paused)})

    ## Dashboard plots
    @staticmethod
    def plot_scatter(context, algorithm):
        # Send PO update to client
        F = algorithm.pop.get("F")
        plot = Scatter().add(F)
        plot.plot_if_not_done_yet()

        return plot.fig

    @staticmethod
    def plot_pcp(context, algorithm):
        # Send PO update to client
        F = algorithm.pop.get("F")
        plot = PCP().add(F)
        plot.plot_if_not_done_yet()

        return plot.fig

    @staticmethod
    def plot_hv(context, algorithm):
        # Send PO update to client
        hv_series = context.data["HV"]
        gen_series = list(range(len(hv_series)))

        plt.figure(figsize=(7, 7))
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


def main():
    # 2 dimension example
    # problem = get_problem("zdt2")

    # algorithm = NSGA2(pop_size=100)

    # res = minimize(problem,
    #               algorithm,
    #               ('n_gen', 200),
    #               seed=1,
    #               callback=Dashboard(),
    #               verbose=True)

    # create the reference directions to be used for the optimization
    ref_dirs = get_reference_directions("das-dennis", 3, n_partitions=12)

    # create the algorithm object
    algorithm = NSGA3(pop_size=92, ref_dirs=ref_dirs)

    # execute the optimization
    _ = minimize(
        get_problem("dtlz1"),
        algorithm,
        seed=2018194,
        callback=Dashboard(develop=True),
        termination=("n_gen", 600),
    )


if __name__ == "__main__":
    main()
