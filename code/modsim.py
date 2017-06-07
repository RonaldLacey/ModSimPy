"""
Code from Modeling and Simulation in Python.

Copyright 2017 Allen Downey

License: https://creativecommons.org/licenses/by/4.0)
"""

from __future__ import print_function, division

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import seaborn as sns
sns.set(style='white', font_scale=1.5)

from scipy.integrate import odeint

from pint import UnitRegistry
UNITS = UnitRegistry()


def underride(d, **options):
    """Add key-value pairs to d only if key is not in d.

    If d is None, create a new dictionary.

    d: dictionary
    options: keyword args to add to d
    """
    if d is None:
        d = {}

    for key, val in options.items():
        d.setdefault(key, val)

    return d


class Simplot:
    """Provides a simplified interface to matplotlib."""

    def __init__(self):
        """Initializes the instance variables."""
        # map from Figure to FigureState
        self.figure_states = dict()
        
    def get_figure_state(self, figure=None):
        """Gets the state of the current figure.

        figure: Figure

        returns: FigureState object
        """
        if figure is None:
            figure = plt.gcf()
        
        try:
            return self.figure_states[figure]
        except KeyError:
            figure_state = FigureState()
            self.figure_states[figure] = figure_state
            return figure_state
    
SIMPLOT = Simplot()


class FigureState:
    """Encapsulates information about the current figure."""
    def __init__(self):
        # map from style tuple to Lines object
        self.lines = dict()
        
    def get_line(self, style, kwargs):
        """Gets the line object for a given style tuple.

        style: Matplotlib style string
        kwargs: dictionary of style options

        returns: maplotlib.lines.Lines2D
        """
        key = style, kwargs.get('color')
        
        try:
            return self.lines[key]
        except KeyError:
            line = self.make_line(style, kwargs)
            self.lines[key] = line
            return line
    
    def make_line(self, style, kwargs):
        underride(kwargs, linewidth=2, alpha=0.6)
        lines = plt.plot([], style, **kwargs)
        return lines[0]

    def clear_lines(self):
        self.lines = dict()


def plot(*args, **kwargs):
    """Makes line plots.
    
    args can be:
      plot(y)
      plot(y, style_string)
      plot(x, y)
      plot(x, y, style_string)
    
    kwargs are the same as for pyplot.plot
    
    If x or y have attributes label and/or units,
    label the axes accordingly.
    
    """
    x = None
    y = None
    style = 'bo-'
    
    # parse the args the same way plt.plot does:
    # 
    if len(args) == 1:
        y = args[0]
    elif len(args) == 2:
        if isinstance(args[1], str):
            y, style = args
        else:
            x, y = args
    elif len(args) == 3:
        x, y, style = args

    #print(type(x))
    #print(type(y))
        
    figure = plt.gcf()
    figure_state = SIMPLOT.get_figure_state(figure)
    line = figure_state.get_line(style, kwargs)
    
    ys = line.get_ydata()
    ys = np.append(ys, y)
    line.set_ydata(ys)

    if x is None:
        xs = np.arange(len(ys))
    else:
        xs = line.get_xdata()
        xs = np.append(xs, x)
    
    line.set_xdata(xs)
    
    #print(line.get_xdata())
    #print(line.get_ydata())
    
    axes = plt.gca()
    axes.relim()
    axes.autoscale_view(True, True, True)
    axes.margins(0.02)
    figure.canvas.draw()
    

def newfig(**kwargs):
    """Creates a new figure."""
    fig = plt.figure()
    fig.set(**kwargs)
    fig.canvas.draw()


savefig = plt.savefig

    
def label_axes(ylabel, xlabel, title=None, **kwargs):
    ax = plt.gca()
    ax.set_ylabel(ylabel, **kwargs)
    ax.set_xlabel(xlabel, **kwargs)
    if title is not None:
        ax.set_title(title, **kwargs)

    # TODO: consider setting labels automatically based on
    # object attributes
    # label the y axis
    #label = getattr(y, 'label', 'y')
    #units = getattr(y, 'units', 'dimensionless')
    #plt.ylabel('%s (%s)' % (label, units))
    
xlabel = plt.xlabel
ylabel = plt.ylabel
title = plt.title
legend = plt.legend

def nolegend():
    # TODO
    pass

class Array(np.ndarray):
    pass


class State:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


def print_state(state):
    for name, value in state.__dict__.items():
        print(name, '=', value)


def flip(p=0.5):
    return np.random.random() < p
