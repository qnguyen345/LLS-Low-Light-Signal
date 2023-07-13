import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

# reads in all the files/data from Data/16.2_Experiment9 directory
all_filenames_100k = glob.glob('Data/16.2_Experiment9/100kOhm/*.xls')
all_filenames_10k = glob.glob('Data/16.2_Experiment9/10kOhm/*.xls')

def file_sorter(all_filenames):
   johnson_data = {}
   analyzed_johnson_data = {}
   for filename in all_filenames:
      split_filename = filename.split()
      if "Analyzed" in split_filename:
         analyzed_johnson_data[filename] = pd.read_csv(filename, delimiter='\t')
      else:
         johnson_data[filename] = pd.read_csv(filename, delimiter='\t',
                                              names=["signal"])
   return johnson_data, analyzed_johnson_data

# Method that plots Johnson noise
def johnson_plotter(data, resistor, not_analyzed = False):
   if not_analyzed:
      # Experimental
      time_constants = []
      avg_R = []
      for dataset in data.items():
         R = dataset[1]["<R>"]
         sqrt_dR2 = dataset[1]["<dR^2>^1/2"]
         dR = dataset[1]["<dR> "]
         avg_R.append(np.mean(sqrt_dR2))
         time_constant = float(dataset[0].split(" = ")[1].split(" ")[0])
         time_constants.append(time_constant)

      # Theoretical
      def total_noise(T, R):
         bandwidth = 5 / (64 * T)
         V_J = np.sqrt(4 * constants.k * 300 * R * 10 ** 3 * (bandwidth))
         V_I = 6e-9 * np.sqrt(bandwidth)
         return np.sqrt((V_J ** 2 + V_I ** 2) * np.sqrt(2))

      # Theoretical_T = np.linspace(min(time_constants), max(time_constants), 100)
      theoretical_T = np.array(time_constants)

      experimental_points = list(zip(time_constants, avg_R))
      experimental_points.sort()
      theoretical_points = list(
         zip(theoretical_T, total_noise(theoretical_T, resistor)))
      theoretical_points.sort()

      # Plotting and plot configurations
      plt.figure(figsize=(10, 8))
      plt.plot([i[0] for i in experimental_points],
               [i[1] for i in experimental_points], 'o-', label="Experimental")
      plt.plot([i[0] for i in theoretical_points],
               [i[1] for i in theoretical_points], 'o-', label="Theoretical")
      plt.title("{} $k\Omega$ : {}\n".format(resistor, dataset[0]))
      plt.xlabel("Time Constant (s)")
      plt.ylabel("Average <dR$^2$>$^{1/2}$ (V)")
      plt.grid(alpha=0.3)
      plt.legend()
      plt.tight_layout()
      plt.show()

   else:
      for dataset in data.items():
         plt.figure(figsize=(15, 8))
         plt.plot(dataset[1]["signal"])
         plt.title("{} $k\Omega$ Analyzed Data\n".format(resistor))
         plt.xlabel("Data Points")
         plt.ylabel("$V_{rms}$")
         plt.grid(alpha=0.3)
         plt.show()

# For 100kOhm resistor
johnson_data_100k, analyzed_johnson_data_100k = file_sorter(all_filenames_100k)
johnson_plotter(johnson_data_100k, 99.7, not_analyzed = False)

# For 10kOhm resistor
johnson_data_10k, analyzed_johnson_data_10k = file_sorter(all_filenames_10k)
johnson_plotter(johnson_data_10k, 9.92, not_analyzed = False)
