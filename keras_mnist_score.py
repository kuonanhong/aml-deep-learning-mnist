"""
Prepare the web service definition by authoring init() and run() functions. 
Test the functions before deploying the web service.
"""

# To generate the schema file, simply execute this scoring script. Make sure that you are using Azure ML Python environment.
# Running this file creates a service-schema.json file under the current working directory that contains the schema 
# of the web service input. It also test the scoring script before creating the web service.
# cd C:\Users\<user-name>\AppData\Local\amlworkbench\Python\python score.py

#Here is the CLI command to create a realtime scoring web service

# Create realtime service
#az ml env setup -g env4entityextractorrg -n env4entityextractor --cluster -z 5 -l eastus2

# Set up AML environment and compute with ACS
#az ml env set --cluster-name env4entityextractor --resource-group env4entityextractorrg

#C:\dl4nlp\models>az ml service create realtime -n extract-biomedical-entities -f score.py -m lstm_bidirectional_model.h5 -s service-schema.json -r python -d resources.pkl -d DataReader.py -d EntityExtractor.py -c scoring_conda_dependencies.yml

#Here is the CLI command to run Kubernetes
#C:\Users\<user-name>\bin\kubectl.exe proxy --kubeconfig C:\Users\hacker\.kube\config


import os
import sys
import json
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Flatten, Dense
from azureml.api.schema.dataTypes import DataTypes
from azureml.api.schema.sampleDefinition import SampleDefinition
from azureml.api.realtime.services import generate_schema

img_width, img_height = 28, 28

# init loads the model (global)
def init():
    """ Initialize and load the model
    """
    global model

    # define architecture of the model.  same architecture used in the train step
    model = Sequential()

    model.add(Conv2D(16, (5, 5), input_shape=(img_width, img_height, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (5, 5)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())    # this converts our 3D feature maps to 1D feature vectors
    model.add(Dense(1000))
    model.add(Activation('relu'))

    model.add(Dense(10))
    model.add(Activation('softmax'))
    # finished model definition

    try:
        # this model was downloaded and copied to the this location on the execution
        # target after the training step prior to running this script
        model_file_path = "mnistneuralnet.h5"
        
        #load the model
        print("Loading trained neural net {}".format(model_file_path))
        model.load_weights(model_file_path)
    except:
        print("can't load the neural network model")
        pass

 
# run takes an input numpy array and performs prediction   
def run(input_array):
    """ Classify the input using the loaded model
    """
    
    try:
        # model.predict returns something like [[0,1,0,0,0,0,0,0,0,0]], so we take the 0th element
        prediction = model.predict(input_array)[0]

        best_class = ''
        best_conf = -1
        for n in [0,1,2,3,4,5,6,7,8,9]:
            if (prediction[n] > best_conf):
                best_class = str(n)
                best_conf = prediction[n]

        return best_class
    except Exception as e:
        return (str(e))

   

def main(): 

    input_array = np.array([[[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [61, 61, 61], [3, 3, 3], [42, 42, 42], [118, 118, 118], [193, 193, 193], [118, 118, 118], [118, 118, 118], [61, 61, 61], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [14, 14, 14], [179, 179, 179], [245, 245, 245], [236, 236, 236], [242, 242, 242], [254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254], [245, 245, 245], [235, 235, 235], [84, 84, 84], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [151, 151, 151], [254, 254, 254], [254, 254, 254], [254, 254, 254], [213, 213, 213], [192, 192, 192], [178, 178, 178], [178, 178, 178], [180, 180, 180], [254, 254, 254], [254, 254, 254], [241, 241, 241], [46, 46, 46], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [43, 43, 43], [235, 235, 235], [254, 254, 254], [226, 226, 226], [64, 64, 64], [28, 28, 28], [12, 12, 12], [0, 0, 0], [0, 0, 0], [2, 2, 2], [128, 128, 128], [252, 252, 252], [255, 255, 255], [173, 173, 173], [17, 17, 17], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [56, 56, 56], [254, 254, 254], [253, 253, 253], [107, 107, 107], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [134, 134, 134], [250, 250, 250], [254, 254, 254], [75, 75, 75], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [63, 63, 63], [254, 254, 254], [158, 158, 158], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [221, 221, 221], [254, 254, 254], [157, 157, 157], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [194, 194, 194], [254, 254, 254], [103, 103, 103], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [150, 150, 150], [254, 254, 254], [213, 213, 213], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [34, 34, 34], [220, 220, 220], [239, 239, 239], [58, 58, 58], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [84, 84, 84], [254, 254, 254], [213, 213, 213], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [126, 126, 126], [254, 254, 254], [171, 171, 171], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [84, 84, 84], [254, 254, 254], [213, 213, 213], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [214, 214, 214], [239, 239, 239], [60, 60, 60], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [84, 84, 84], [254, 254, 254], [213, 213, 213], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [214, 214, 214], [199, 199, 199], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [84, 84, 84], [254, 254, 254], [213, 213, 213], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [11, 11, 11], [219, 219, 219], [199, 199, 199], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [84, 84, 84], [254, 254, 254], [213, 213, 213], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [98, 98, 98], [254, 254, 254], [199, 199, 199], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [162, 162, 162], [254, 254, 254], [209, 209, 209], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [98, 98, 98], [254, 254, 254], [199, 199, 199], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [51, 51, 51], [238, 238, 238], [254, 254, 254], [75, 75, 75], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [98, 98, 98], [254, 254, 254], [199, 199, 199], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [51, 51, 51], [165, 165, 165], [254, 254, 254], [195, 195, 195], [4, 4, 4], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [66, 66, 66], [241, 241, 241], [199, 199, 199], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [3, 3, 3], [167, 167, 167], [254, 254, 254], [227, 227, 227], [55, 55, 55], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [214, 214, 214], [213, 213, 213], [20, 20, 20], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [46, 46, 46], [152, 152, 152], [202, 202, 202], [254, 254, 254], [254, 254, 254], [63, 63, 63], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [214, 214, 214], [254, 254, 254], [204, 204, 204], [180, 180, 180], [180, 180, 180], [180, 180, 180], [180, 180, 180], [180, 180, 180], [235, 235, 235], [254, 254, 254], [254, 254, 254], [234, 234, 234], [156, 156, 156], [10, 10, 10], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [81, 81, 81], [205, 205, 205], [254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254], [252, 252, 252], [234, 234, 234], [120, 120, 120], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [26, 26, 26], [210, 210, 210], [254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254], [153, 153, 153], [104, 104, 104], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]])

    # Test the output of the functions
    init()  
    
    print("Result: " + run(input_array))
    
    inputs = {"input_array": SampleDefinition(DataTypes.NUMPY, input_array)}

    # create the outputs folder
    os.makedirs('./outputs', exist_ok=True)

    #Generate the schema
    generate_schema(run_func=run, inputs=inputs, filepath='./outputs/service-schema.json')
    print("Schema generated")


if __name__ == "__main__":
    main()
