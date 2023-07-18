from flask import Flask
from flask import render_template

from pymoo.visualization.scatter import Scatter
from pymoo.problems import get_problem

import io
import base64

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

    

