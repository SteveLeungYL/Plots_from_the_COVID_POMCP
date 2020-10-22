### Before running this code, please place the pomcp binary executable to the current working directory.

import pandas as pd
import numpy as np
import time
import subprocess
import matplotlib.pyplot as plt

def run_program_from_shell_command(total_population = 50000, num_of_simulation = 2 ** 8, output_file_name = "output.csv", horizon = 30, testing_number = 200, testing_action_step = 100):
    # Shell command space.
    shell_command = "./pomcp --problem covid --outputfile {} --total_population {} --horizon {} --maximum_testing_number {} " \
                    " --testing_group_number 32 --testing_action_step {} --runs 100 --mindoubles {} --maxdoubles {} --time_step 1 --I_class_ratio 0.00637 --R_class_ratio 0.0162 " \
                    "--accuracy 0.1 --verbose 0 --autoexploration false --timeout 999999 --userave false " \
                    "--ravediscount 1.0 --raveconstant 0.01 --disabletree false --exploration 1 --usetransforms true --debug_mode 1".format(
        output_file_name,
        total_population,
        horizon,
        testing_number,
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
            # Process has finished, read rest of the output
            # for output in process.stdout.readlines():
            #     print(output.strip())
            if return_code != 0:
                # raise RuntimeError("Shell script return code is not 0.")
                return 1
            return 0
            
            

if __name__=="__main__":

    fixed_num_of_simulation = 10
    fixed_horizon = 30
    # fixed_testing_action_step = 10
    # fixed_population = 50000 

    for num_of_population in range(125000, 170000, 25000):

        num_of_testing = int(0.004 * num_of_population)
        testing_action_step = int(num_of_testing / 20)

        print("Running on population: {}, num_simulation: {}, horizon: {}, testing_number: {}, testing_action_step: {}.".format(
            num_of_population,
            2**fixed_num_of_simulation,
            fixed_horizon,
            num_of_testing,
            testing_action_step
        ))

        output_file_name = "output_num_population_{}.csv".format(num_of_population)

        run_program_from_shell_command(total_population=num_of_population, num_of_simulation=fixed_num_of_simulation,
                                       output_file_name=output_file_name, horizon=fixed_horizon, testing_number= num_of_testing, testing_action_step=testing_action_step)

