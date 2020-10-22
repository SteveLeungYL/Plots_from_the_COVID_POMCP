### Before running this code, please place the pomcp binary executable to the current working directory.

import pandas as pd
import numpy as np
import time
import subprocess
import matplotlib.pyplot as plt

def run_program_from_shell_command(total_population = 89000, num_of_simulation = 2 ** 8, output_file_name = "output.csv", horizon = 30, testing_action_step = 10):
    # Shell command space.
    shell_command = "./pomcp --problem covid --outputfile {} --total_population {} --horizon {} --maximum_testing_number 500 " \
                    " --testing_group_number 32 --testing_action_step {} --runs 100 --mindoubles {} --maxdoubles {} --time_step 1  --I_class_ratio 0.00637 --R_class_ratio 0.0162 " \
                    " --accuracy 0.1 --verbose 0 --autoexploration false --timeout 999999 --userave false " \
                    " --ravediscount 1.0 --raveconstant 0.01 --disabletree false --exploration 1 --usetransforms true --debug_mode 1 ".format(
        output_file_name,
        total_population,
        horizon,
        testing_action_step,
        num_of_simulation,
        num_of_simulation
    )
    print("\n" + shell_command + "\n")
    process = subprocess.Popen(shell_command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True
                               )
    while True:
        output = process.stdout.readline()
        print(output.strip())
        stderr = process.stderr.readline()
        print(stderr.strip())

        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)


            if return_code != 0:

                return 1

            return 0
            
            

if __name__=="__main__":

    # fixed_number_of_simulation = 10
    fixed_horizon = 30
    fixed_testing_action_step = 10
    fixed_population = 89000

    for num_of_simulation in range(11, 12, 1):

        print("Running on population: {}, num_simulation: {}, horizon: {}, testing_action_step: {}.".format(
            fixed_population,
            2**num_of_simulation,
            fixed_horizon,
            fixed_testing_action_step
        ))

        output_file_name = "output_num_simulation_{}.csv".format(num_of_simulation)


        run_program_from_shell_command(total_population=fixed_population, num_of_simulation=num_of_simulation,
                                       output_file_name=output_file_name, horizon=fixed_horizon, testing_action_step=fixed_testing_action_step)

