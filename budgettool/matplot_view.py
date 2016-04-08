import matplotlib.pyplot as plt
import numpy as np

def plot_forecast(forecast):
    x_values = np.array([entry.date for entry in forecast])
    y_values = np.array([entry.balance for entry in forecast])
    plt.plot(x_values, y_values)
    plt.grid()
    plt.show()
