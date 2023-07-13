import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Reads all the files/data from Data/9.2_Experiment3 directory
all_filenames = glob.glob('Data/9.2_Experiment3/*.xls')
T_data = {}
analyzed_T_data = {}

for filename in all_filenames:
    split_filename = filename.split()
    if "Analyzed" in split_filename:
        analyzed_T_data[filename] = pd.read_csv(filename, delimiter='\t')
    else:
        T_data[filename] = pd.read_csv(filename, delimiter='\t', names=["signal"])

# Exponential decay fit
def fit_exp(x, a, b):
   x = np.array(x)
   return np.exp(-a * x) + b

def time_constant_plotter(data):
   filename = data[0]
   signal = list(data[1]["signal"])
   data_points = [i + 1 for i in range(len(signal))]

   cropped_signal = []
   cropped_data_points = []

   # Finds the slope
   for i in range(len(signal)):
      slope = abs(
         (signal[i - 1] - signal[i]) / (data_points[i - 1] - data_points[i]))
      if round(slope, 2) != 0:
         cropped_signal.append(signal[i])
         cropped_data_points.append(data_points[i])

   # Crop data since anything outside the bounds were background noises picked up by apparatus
   cropped_signal += signal[max(cropped_data_points) - 1:]
   cropped_data_points += data_points[max(cropped_data_points) - 1:]
   scaled_cropped_data_points = data_points[:len(cropped_signal)]

   exp_opt, exp_pcov = curve_fit(fit_exp, scaled_cropped_data_points,
                                 cropped_signal)
   fit_uncertainties = np.sqrt(np.diag(exp_pcov))
   time_constant = 1 / exp_opt[0] * 0.03125

   # Plotting and plot configurations
   plt.figure(figsize=(15, 10))
   plt.plot(signal, label="Raw data")
   plt.plot(cropped_data_points, fit_exp(scaled_cropped_data_points, *exp_opt),
            label="Fit: exp(-{:.3f} * x) + ({:.3f})".format(exp_opt[0],
                                                            exp_opt[1]))
   plt.title(filename)
   plt.xlabel("Data Points")
   plt.ylabel("Signal")
   plt.legend()
   plt.grid(alpha=0.3)
   plt.show()

   return filename, time_constant, exp_opt, fit_uncertainties

#Stores analyzed data
analyzed_data = {}

# Plotting for all data sets
for dataset in T_data.items():
    plotter_data = time_constant_plotter(dataset)
    analyzed_data[plotter_data[0]] = {"time constant (s)": plotter_data[1],
                                     "fit parameters": plotter_data[2],
                                     "fit uncertainties": plotter_data[3]}