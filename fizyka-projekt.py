# -*- coding: utf-8 -*-
from flask import Flask, render_template
from pyping import ping
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
app = Flask(__name__)


def make_histogram():
    hist, bins = np.histogram([measurement.ping for measurement in measurements.data],
                              bins=int(sqrt(len(measurements.data))))
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    fig, ax = plt.subplots()
    ax.bar(center, hist, align='center', width=width)
    fig.savefig("static/histogram.png")


class Measuerements:
    def __init__(self, host):
        self.host = host
        self.data = list()
        self.count = 0.0
        self.avg = 0.0
        self.__sum = 0.0

    def measure(self):
        m = self.Measurement(self)
        self.data.append(m)
        self.count += 1.0
        self.__sum += m.ping
        self.avg = self.__sum/self.count

    class Measurement:
        def __init__(self, parent):
            self.ping = float(
                ping(hostname=parent.host,
                timeout=2000,
                count=1).avg_rtt
            )


@app.route('/')
def hello_world():
    return render_template("index.html", measurements=measurements)

if __name__ == '__main__':
    import sys
    print sys.argv
    print "Wykonywanie pomiarów"
    measurements = Measuerements("wp.pl")
    for i in range(100):
        measurements.measure()
    make_histogram()
    app.run(host="localhost", port=5000)
