import numpy as np
import time
import os
import torch
import _pickle as cPickle
from src.RL import RL
from src.toric_model import Toric_code

from NN import NN_11, NN_17
from ResNet import ResNet18, ResNet34, ResNet50, ResNet101, ResNet152

##########################################################################

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# valid network names: 
#   NN_11
#   NN_17
#   ResNet18
#   ResNet34
#   ResNet50
#   ResNet101
#   ResNet152
NETWORK = NN_17

# common system sizes are 3,5,7 and 9 
# grid size must be odd! 
SYSTEM_SIZE = 5

# For continuing the training of an agent
continue_training = False
# this file is stored in the network folder and contains the trained agent.  
NETWORK_FILE_NAME = 'Test1_NN17_Size_5'

# initialize RL class and training parameters 
rl = RL(Network=NETWORK,
        Network_name=NETWORK_FILE_NAME,
        system_size=SYSTEM_SIZE,
        p_error=0.1,
        replay_memory_capacity=20000, 
        learning_rate=0.00025,
        discount_factor=0.95,
        max_nbr_actions_per_episode=10,  # [50], max steps allowed during training
        device=device,
        replay_memory='proportional')   # proportional  
                                        # uniform


# generate folder structure 
timestamp = time.strftime("%y_%m_%d__%H_%M_%S__")
PATH = 'data/training__' +str(NETWORK_FILE_NAME) +'_'+str(SYSTEM_SIZE)+'__' + timestamp
PATH_epoch = PATH + '/network_epoch'
if not os.path.exists(PATH):
    os.makedirs(PATH)
    os.makedirs(PATH_epoch)

# load the network for continue training 
if continue_training == True:
    print('continue training')
    PATH2 = 'network/'+str(NETWORK_FILE_NAME)+'.pt'
    rl.load_network(PATH2)

# train for n epochs the agent (test parameters)
rl.train_for_n_epochs(training_steps=5000, # [-], number of episodes per epoch
                    num_of_predictions=100, # [100], number of predicions when evaluating
                    num_of_steps_prediction=10, # [50], number of allowed steps when evaluating
                    epochs=20,  # [-], "epochs", how many times to do training_steps episodes
                    target_update=100,  # [100], how often to update target net
                    optimizer='Adam',  # ['Adam'], 'Adam' or 'RMSprop'
                    batch_size=32, # [32], how many episodes to batch together (during training?)
                    directory_path = PATH, # where to save
                    prediction_list_p_error=[0.06,0.10,0.14],  # [[0.1]],  list of p_error to use when evaluating
                    replay_start_size=32) # [32] 


""" rl.train_for_n_epochs(training_steps=10000,
                            num_of_predictions=100,
                            epochs=100,
                            target_update=1000,
                            optimizer='Adam',
                            batch_size=32,
                            directory_path = PATH,
                            prediction_list_p_error=[0.1],
                            minimum_nbr_of_qubit_errors=0)   """
               
