"""Plot graph of forecast."""

def plot_forecast(forecast):
    """Plot a graph of the forecast."""
    import matplotlib.pyplot as plt
    import numpy as np
    
    x_values = np.array([entry.date for entry in forecast])
    y_values = np.array([entry.balance for entry in forecast])
    figure = plt.figure()
    plt.plot(x_values, y_values)
    figure.autofmt_xdate()
    plt.grid()
    plt.show()
