import matplotlib
import glob

from scipy.io import loadmat, savemat
import os
import numpy as np

def get_file_trials(file_path):
    """
    Utility function to get trial data from a .mat file
    
    Args:
    file_path: String; Location of the matlab file
    ----------
    Returns:
    trials: nparray; trials from the .mat file
    """
    mat = loadmat(file_path)
    trials = mat["trial"][0]
    return np.array([a for a in trials])

def get_data(subject_files_path):
    """
    A function to read data from all subjects and concatenate it
    
    Args:
    ----------
    subject_files_path: String; Location of where subject files are located
    
    Returns:
    ----------
    final_data: nparray; contains concatenated data from all trials
    final_y: nparray; contains corresponding labels
    
    """
    labels = ["breath", "feet", "future", "worry"]
    l_trial_data = {}
    for l in labels:
        l_trial_data[l] = []
    for files in glob.glob(subject_files_path+str("/subject*")):
        for file in glob.glob(files + str("/*")):
            for label in labels:
                if(file.split("\\")[-1] == f"{label}_cleaned_ica_data.mat"):
                    l_trial_data[label].append(get_file_trials(file))
    trial_data = {}
    for l in labels:
        trial_data[l] = np.concatenate(l_trial_data[l], axis = 0)
    y = {}
    for i in range(len(labels)):
        y[labels[i]] = np.full(trial_data[labels[i]].shape[0],i)
    final_data = np.concatenate([i for i in trial_data.values()], axis = 0)
    final_y = np.concatenate([i for i in y.values()], axis = 0)
    return final_data, final_y