import pandas as pd
import numpy as np
import re
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib

import scipy.stats

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m+h, m-h


total_population = 89000
total_testing_number = 300

sample_total_run_count = 100
total_time_step = 30




input_folder = "./"
all_files_name = os.listdir(input_folder)
all_files_name.sort()


mean_H_list = []
mean_cum_I_list = []
mean_peak_I_list = []
mean_asymptomatic_testing_list = []
mean_symptomatic_testing_list = []
mean_I2_list = []
mean_S_list = []
mean_E_list = []
mean_I1_list = []
mean_R_list = []

upper_H_list = []
upper_cum_I_list = []
upper_peak_I_list = []
upper_asymptomatic_testing_list = []
upper_symptomatic_testing_list = []
upper_I2_list = []
upper_S_list = []
upper_E_list = []
upper_I1_list = []
upper_R_list = []

lower_H_list = []
lower_cum_I_list = []
lower_peak_I_list = []
lower_asymptomatic_testing_list = []
lower_symptomatic_testing_list = []
lower_I2_list = []
lower_S_list = []
lower_E_list = []
lower_I1_list = []
lower_R_list = []


for num_of_simulations in range(10, 11, 3):
    
    data_name = "output_300_num_simulation_{}.csv.process_all.csv".format(
        num_of_simulations
    )
    current_model_data_all_runs = pd.read_csv(input_folder + data_name)

    I_current = []
    H_current = []
    asymptomatic_testing_current = []
    symptomatic_testing_current = []
    cum_I_current = []
    I2_current = []
    S_current = []
    E_current = []
    I1_current = []
    R_current = []

    for sample_run_count in range(sample_total_run_count):
        current_model_data = current_model_data_all_runs[current_model_data_all_runs['Run'] == sample_run_count]

        S = current_model_data['S'].tolist()
        S_current.append(S)

        E = current_model_data['E'].tolist()
        E_current.append(E)

        I1 = current_model_data['I1'].tolist()

        I2 = current_model_data['I2'].tolist()

        I = [x+y for x,y in zip(I1, I2)]
        I_current.append(I)

        I1_current.append(I1)
        I2_current.append(I2)

        H = current_model_data['H'].tolist()
        H_current.append(H)

        R = current_model_data['R'].tolist()
        R_current.append(R)

        testing_types = current_model_data['Testing_Types'].tolist()

        asymptomatic_testing = [int(x * total_testing_number) for x in testing_types]
        asymptomatic_testing_current.append(asymptomatic_testing)
        symptomatic_testing_current.append([int(total_testing_number - x) for x in asymptomatic_testing])

        cum_I = [x + y for x, y in zip(I1, I2)]
        # cum_I = [x + y for x, y in zip(cum_I, H)]
        # cum_I = [x + y for x, y in zip(cum_I, R)]
        cum_I_current.append(cum_I)

    mean_cum_I_curve = []
    upper_cum_I_curve = []
    lower_cum_I_curve = []
    
    mean_asymptomatic_testing_curve = []
    upper_asymptomatic_testing_curve = []
    lower_asymptomatic_testing_curve = []
    mean_symptomatic_testing_curve = []
    upper_symptomatic_testing_curve = []
    lower_symptomatic_testing_curve = []

    mean_S_curve = []
    upper_S_curve = []
    lower_S_curve = []

    mean_E_curve = []
    upper_E_curve = []
    lower_E_curve = []

    mean_I1_curve = []
    upper_I1_curve = []
    lower_I1_curve = []

    mean_I2_curve = []
    upper_I2_curve = []
    lower_I2_curve = []

    mean_R_curve = []
    upper_R_curve = []
    lower_R_curve = []

    mean_H_curve = []
    upper_H_curve = []
    lower_H_curve = []

    for i in range(len(cum_I_current[0])):
        cum_I_step = [x[i] for x in cum_I_current]
        # cum_I_step = cum_I_step[1:]
        mean_cum_I_step, upper_cum_I_step, lower_cum_I_step = mean_confidence_interval(cum_I_step)
        mean_cum_I_curve.append(mean_cum_I_step)
        upper_cum_I_curve.append(upper_cum_I_step)
        lower_cum_I_curve.append(lower_cum_I_step)

        S_step = [x[i] for x in S_current]
        mean_S_step, upper_S_step, lower_S_step = mean_confidence_interval(S_step)
        mean_S_curve.append(mean_S_step)
        upper_S_curve.append(upper_S_step)
        lower_S_curve.append(lower_S_step)

        E_step = [x[i] for x in E_current]
        mean_E_step, upper_E_step, lower_E_step = mean_confidence_interval(E_step)
        mean_E_curve.append(mean_E_step)
        upper_E_curve.append(upper_E_step)
        lower_E_curve.append(lower_E_step)

        I1_step = [x[i] for x in I1_current]
        mean_I1_step, upper_I1_step, lower_I1_step = mean_confidence_interval(I1_step)
        mean_I1_curve.append(mean_I1_step)
        upper_I1_curve.append(upper_I1_step)
        lower_I1_curve.append(lower_I1_step)

        I2_step = [x[i] for x in I2_current]
        mean_I2_step, upper_I2_step, lower_I2_step = mean_confidence_interval(I2_step)
        mean_I2_curve.append(mean_I2_step)
        upper_I2_curve.append(upper_I2_step)
        lower_I2_curve.append(lower_I2_step)

        H_step = [x[i] for x in H_current]
        # H_step = H_step[1:]
        mean_H_step, upper_H_step, lower_H_step = mean_confidence_interval(H_step)
        mean_H_curve.append(mean_H_step)
        upper_H_curve.append(upper_H_step)
        lower_H_curve.append(lower_H_step)

        R_step = [x[i] for x in R_current]
        mean_R_step, upper_R_step, lower_R_step = mean_confidence_interval(R_step)
        mean_R_curve.append(mean_R_step)
        upper_R_curve.append(upper_R_step)
        lower_R_curve.append(lower_R_step)

        asymptomatic_testing_list = [x[i] for x in asymptomatic_testing_current]
        mean_asymp, upper_asymp, lower_asymp = mean_confidence_interval(asymptomatic_testing_list)

        mean_asymptomatic_testing_curve.append(mean_asymp)
        upper_asymptomatic_testing_curve.append(upper_asymp)
        lower_asymptomatic_testing_curve.append(lower_asymp)

        symptomatic_testing_list = [x[i] for x in symptomatic_testing_current]
        mean_symp, upper_symp, lower_symp = mean_confidence_interval(symptomatic_testing_list)

        mean_symptomatic_testing_curve.append(mean_symp)
        upper_symptomatic_testing_curve.append(upper_symp)
        lower_symptomatic_testing_curve.append(lower_symp)

    mean_cum_I_list.append(mean_cum_I_curve)
    upper_cum_I_list.append(upper_cum_I_curve)
    lower_cum_I_list.append(lower_cum_I_curve)

    mean_S_list.append(mean_S_curve)
    upper_S_list.append(upper_S_curve)
    lower_S_list.append(lower_S_curve)

    mean_E_list.append(mean_E_curve)
    upper_E_list.append(upper_E_curve)
    lower_E_list.append(lower_E_curve)

    mean_I1_list.append(mean_I1_curve)
    upper_I1_list.append(upper_I1_curve)
    lower_I1_list.append(lower_I1_curve)

    mean_I2_list.append(mean_I2_curve)
    upper_I2_list.append(upper_I2_curve)
    lower_I2_list.append(lower_I2_curve)

    mean_H_list.append(mean_H_curve)
    upper_H_list.append(upper_H_curve)
    lower_H_list.append(lower_H_curve)

    mean_R_list.append(mean_R_curve)
    upper_R_list.append(upper_R_curve)
    lower_R_list.append(lower_R_curve)

    mean_asymptomatic_testing_list.append(mean_asymptomatic_testing_curve)
    upper_asymptomatic_testing_list.append(upper_asymptomatic_testing_curve)
    lower_asymptomatic_testing_list.append(lower_asymptomatic_testing_curve)

    mean_symptomatic_testing_list.append(mean_symptomatic_testing_curve)
    upper_symptomatic_testing_list.append(upper_symptomatic_testing_curve)
    lower_symptomatic_testing_list.append(lower_symptomatic_testing_curve)

    # last_day_cum_I_list = [x[-1] for x in cum_I_current]
    # mean_last_day_cum_I, upper_last_day_cum_I, lower_last_day_cum_I = mean_confidence_interval(last_day_cum_I_list)

    # mean_last_cum_I_list.append(mean_last_day_cum_I)
    # upper_last_cum_I_list.append(upper_last_day_cum_I)
    # lower_last_cum_I_list.append(lower_last_day_cum_I)

    # peak_H_list = [max(x) for x in H_current]
    # mean_peak_H, upper_peak_H, lower_peak_H = mean_confidence_interval(peak_H_list)

    # mean_peak_H_list.append(mean_peak_H)
    # upper_peak_H_list.append(upper_peak_H)
    # lower_peak_H_list.append(lower_peak_H)

    peak_I_list = [max(x) for x in I_current]
    mean_peak_I, upper_peak_I, lower_peak_I = mean_confidence_interval(peak_I_list)

    mean_peak_I_list.append(mean_peak_I)
    upper_peak_I_list.append(upper_peak_I)
    lower_peak_I_list.append(lower_peak_I)

    



# for fix_testing_number in [-1, 0, 100, 200]:

#     if fix_testing_number == -1:
#         data_name = "Random_Action_SEIR.csv"
#         current_model_data = pd.read_csv(input_folder + data_name)
#     else:
#         data_name = "Fix_Action_SEIR_{}.csv".format(
#         fix_testing_number
#     )

#     current_model_data = pd.read_csv(input_folder + data_name)

#     I_current = []
#     H_current = []
#     cum_I_current = []
#     I2_current = []
#     S_current = []
#     E_current = []
#     I1_current = []
#     R_current = []

#     for run_count in range(sample_total_run_count):
#         current_sample_data = current_model_data[current_model_data['Run_Count'] == run_count]

#         S = current_sample_data['S'].to_list()
#         S_current.append(S)

#         E = current_sample_data['E'].to_list()
#         E_current.append(E)

#         I1 = current_sample_data['I1'].to_list()
#         I2 = current_sample_data['I2'].to_list()
#         I = [x+y for x,y in zip(I1, I2)]
#         I_current.append(I)

#         I1_current.append(I1)
#         I2_current.append(I2)

#         H = current_sample_data['H'].to_list()
#         H_current.append(H)

#         R = current_sample_data['R'].to_list()
#         R_current.append(R)

#         cum_I = current_sample_data['cum_I'].to_list()
#         cum_I_current.append(cum_I)

#     mean_cum_I_curve = []
#     upper_cum_I_curve = []
#     lower_cum_I_curve = []

#     mean_S_curve = []
#     upper_S_curve = []
#     lower_S_curve = []

#     mean_E_curve = []
#     upper_E_curve = []
#     lower_E_curve = []

#     mean_I1_curve = []
#     upper_I1_curve = []
#     lower_I1_curve = []

#     mean_I2_curve = []
#     upper_I2_curve = []
#     lower_I2_curve = []

#     mean_R_curve = []
#     upper_R_curve = []
#     lower_R_curve = []

#     mean_H_curve = []
#     upper_H_curve = []
#     lower_H_curve = []


#     for i in range(len(cum_I_current[0])):
#         cum_I_step = [x[i] for x in cum_I_current]
#         mean_cum_I_step, upper_cum_I_step, lower_cum_I_step = mean_confidence_interval(cum_I_step)
#         mean_cum_I_curve.append(mean_cum_I_step)
#         upper_cum_I_curve.append(upper_cum_I_step)
#         lower_cum_I_curve.append(lower_cum_I_step)

#         S_step = [x[i] for x in S_current]
#         mean_S_step, upper_S_step, lower_S_step = mean_confidence_interval(S_step)
#         mean_S_curve.append(mean_S_step)
#         upper_S_curve.append(upper_S_step)
#         lower_S_curve.append(lower_S_step)

#         E_step = [x[i] for x in E_current]
#         mean_E_step, upper_E_step, lower_E_step = mean_confidence_interval(E_step)
#         mean_E_curve.append(mean_E_step)
#         upper_E_curve.append(upper_E_step)
#         lower_E_curve.append(lower_E_step)

#         I1_step = [x[i] for x in I1_current]
#         mean_I1_step, upper_I1_step, lower_I1_step = mean_confidence_interval(I1_step)
#         mean_I1_curve.append(mean_I1_step)
#         upper_I1_curve.append(upper_I1_step)
#         lower_I1_curve.append(lower_I1_step)

#         I2_step = [x[i] for x in I2_current]
#         mean_I2_step, upper_I2_step, lower_I2_step = mean_confidence_interval(I2_step)
#         mean_I2_curve.append(mean_I2_step)
#         upper_I2_curve.append(upper_I2_step)
#         lower_I2_curve.append(lower_I2_step)

#         H_step = [x[i] for x in H_current]
#         # H_step = H_step[1:]
#         mean_H_step, upper_H_step, lower_H_step = mean_confidence_interval(H_step)
#         mean_H_curve.append(mean_H_step)
#         upper_H_curve.append(upper_H_step)
#         lower_H_curve.append(lower_H_step)

#         R_step = [x[i] for x in R_current]
#         mean_R_step, upper_R_step, lower_R_step = mean_confidence_interval(R_step)
#         mean_R_curve.append(mean_R_step)
#         upper_R_curve.append(upper_R_step)
#         lower_R_curve.append(lower_R_step)

#     mean_cum_I_list.append(mean_cum_I_curve)
#     upper_cum_I_list.append(upper_cum_I_curve)
#     lower_cum_I_list.append(lower_cum_I_curve)

#     mean_S_list.append(mean_S_curve)
#     upper_S_list.append(upper_S_curve)
#     lower_S_list.append(lower_S_curve)

#     mean_E_list.append(mean_E_curve)
#     upper_E_list.append(upper_E_curve)
#     lower_E_list.append(lower_E_curve)

#     mean_I1_list.append(mean_I1_curve)
#     upper_I1_list.append(upper_I1_curve)
#     lower_I1_list.append(lower_I1_curve)

#     mean_I2_list.append(mean_I2_curve)
#     upper_I2_list.append(upper_I2_curve)
#     lower_I2_list.append(lower_I2_curve)

#     mean_H_list.append(mean_H_curve)
#     upper_H_list.append(upper_H_curve)
#     lower_H_list.append(lower_H_curve)

#     mean_R_list.append(mean_R_curve)
#     upper_R_list.append(upper_R_curve)
#     lower_R_list.append(lower_R_curve)


#     # last_day_cum_I_list = [x[-1] for x in cum_I_current]
#     # mean_last_day_cum_I, upper_last_day_cum_I, lower_last_day_cum_I = mean_confidence_interval(last_day_cum_I_list)

#     # mean_last_cum_I_list.append(mean_last_day_cum_I)
#     # upper_last_cum_I_list.append(upper_last_day_cum_I)
#     # lower_last_cum_I_list.append(lower_last_day_cum_I)

#     # peak_H_list = [max(x) for x in H_current]
#     # mean_peak_H, upper_peak_H, lower_peak_H = mean_confidence_interval(peak_H_list)

#     # mean_peak_H_list.append(mean_peak_H)
#     # upper_peak_H_list.append(upper_peak_H)
#     # lower_peak_H_list.append(lower_peak_H)

#     peak_I_list = [max(x) for x in I_current]
#     mean_peak_I, upper_peak_I, lower_peak_I = mean_confidence_interval(peak_I_list)

#     mean_peak_I_list.append(mean_peak_I)
#     upper_peak_I_list.append(upper_peak_I)
#     lower_peak_I_list.append(lower_peak_I)

    


# matplotlib.rcParams.update({'font.size': 17})
# plt.rcParams["figure.figsize"] = [9.2,6]

# legend = ['POMCP. Sim: $2^6$', 'POMCP. Sim: $2^9$', 'POMCP. Sim: $2^{12}$', 'Random_Action', 'Pure Symp', 'Half Public, Half Symp', 'Pure Public']


# # Plot the active I curve.

# fig = plt.figure()
# for cum_I_index in range(len(mean_cum_I_list)):
#     mean_cum_I = mean_cum_I_list[cum_I_index]
#     time_step = list(range(len(mean_cum_I)))
#     plt.plot(time_step, mean_cum_I)

#     upper_cum_I = upper_cum_I_list[cum_I_index]
#     lower_cum_I = lower_cum_I_list[cum_I_index]
#     plt.fill_between(time_step, lower_cum_I, upper_cum_I, alpha = 0.10)

# plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(2))

# plt.legend(legend)
# plt.xlabel("Time Step(Days)")
# plt.ylabel("Active I progress")

# plt.savefig("./Plots/active_I_curve.png")
# plt.close(fig)


# # Plot the active S curve.

# fig = plt.figure()
# for S_index in range(len(mean_S_list)):
#     mean_S = mean_S_list[S_index]
#     time_step = list(range(len(mean_S)))
#     plt.plot(time_step, mean_S)

#     upper_S = upper_S_list[S_index]
#     lower_S = lower_S_list[S_index]
#     plt.fill_between(time_step, lower_S, upper_S, alpha = 0.10)

# plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(10))

# plt.legend(legend)
# plt.xlabel("Time Step(Days)")
# plt.ylabel("Susceptible (S) number")

# plt.savefig("./Plots/S_curve.png")
# plt.close(fig)

# # Plot the active E curve.

# fig = plt.figure()
# for E_index in range(len(mean_E_list)):
#     mean_E = mean_E_list[E_index]
#     time_step = list(range(len(mean_E)))
#     plt.plot(time_step, mean_E)

#     upper_E = upper_E_list[E_index]
#     lower_E = lower_E_list[E_index]
#     plt.fill_between(time_step, lower_E, upper_E, alpha = 0.10)

# plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(10))

# plt.legend(legend)
# plt.xlabel("Time Step(Days)")
# plt.ylabel("Exposed (E) number")

# plt.savefig("./Plots/E_curve.png")
# plt.close(fig)

# # Plot the active I_1 curve.

# fig = plt.figure()
# for I1_index in range(len(mean_I1_list)):
#     mean_I1 = mean_I1_list[I1_index]
#     time_step = list(range(len(mean_I1)))
#     plt.plot(time_step, mean_I1)

#     upper_I1 = upper_I1_list[I1_index]
#     lower_I1 = lower_I1_list[I1_index]
#     plt.fill_between(time_step, lower_I1, upper_I1, alpha = 0.10)

# plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(10))

# plt.legend(legend)
# plt.xlabel("Time Step(Days)")
# plt.ylabel("Asymp Patients (I$_1$) number")

# plt.savefig("./Plots/I1_curve.png")
# plt.close(fig)


# # Plot the active I_2 curve.

# fig = plt.figure()
# for I2_index in range(len(mean_I2_list)):
#     mean_I2 = mean_I2_list[I2_index]
#     time_step = list(range(len(mean_I2)))
#     plt.plot(time_step, mean_I2)

#     upper_I2 = upper_I2_list[I2_index]
#     lower_I2 = lower_I2_list[I2_index]
#     plt.fill_between(time_step, lower_I2, upper_I2, alpha = 0.10)

# plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(10))

# plt.legend(legend)
# plt.xlabel("Time Step(Days)")
# plt.ylabel("Symp Patients (I$_2$) number")

# plt.savefig("./Plots/I2_curve.png")
# plt.close(fig)




# # Plot the Hospitalization

# fig = plt.figure()
# for H_index in range(len(mean_H_list)):
#     mean_H = mean_H_list[H_index]
#     time_step = list(range(len(mean_H)))
#     plot, = plt.plot(time_step, mean_H)

#     upper_H = upper_H_list[H_index]
#     lower_H = lower_H_list[H_index]
#     plt.fill_between(time_step, lower_H, upper_H, alpha=0.10)

# plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(2))

# plt.legend(legend)
# plt.xlabel("Time Step(Days)")
# plt.ylabel("Active Hospitalization (H) number")

# plt.savefig("./Plots/Hospitalization.png")
# plt.close(fig)


# # Plot the active R curve.

# fig = plt.figure()
# for R_index in range(len(mean_R_list)):
#     mean_R = mean_R_list[R_index]
#     time_step = list(range(len(mean_R)))
#     plt.plot(time_step, mean_R)

#     upper_R = upper_R_list[R_index]
#     lower_R = lower_R_list[R_index]
#     plt.fill_between(time_step, lower_R, upper_R, alpha = 0.10)

# plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(10))

# plt.legend(legend)
# plt.xlabel("Time Step(Days)")
# plt.ylabel("Recovery (R) number")

# plt.savefig("./Plots/R_curve.png")
# plt.close(fig)

# # # Plot the Peak Infectious number.

# # fig = plt.figure()
# # _, ax = plt.subplots()

# # x = list(range(len(mean_peak_I_list)))
# # plt.bar(x, mean_peak_I_list)


# # y_upper_error = [ x-y for x,y in zip(upper_peak_I_list, mean_peak_I_list)]
# # # y_lower_error = [ x-y for x,y in zip(lower_peak_I_list, mean_peak_I_list)]
# # # y_error = [y_upper_error, y_lower_error]

# # ax.errorbar(x, mean_peak_I_list, yerr = y_upper_error, color = "k", capsize=3, fmt=".", ms = 0.0001)

# # my_xticks = ['POMCP. \nSim: 2**6', 'POMCP. \nSim: 2**9', 'POMCP. \nSim: 2**12', 'Random \nAction', 'Pure \nSymp', 'Half \nAsymp, Half \nSymp', 'Pure \nAsymp']
# # plt.xticks(x, my_xticks, fontsize=8)
# # plt.ylabel("Peak I number")
# # plt.savefig("./Plots/Peak_I.png")
# # plt.close(fig)



# Plot the asymptomatic testing rate.


matplotlib.rcParams.update({'font.size': 27})
plt.rcParams["figure.figsize"] = [9.2,6]
plt.rcParams["font.family"] = "Times New Roman"

fig = plt.figure()
_, ax = plt.subplots()

patterns = [ "|" , "\\" , "/" , "+" , "-", ".", "*","x", "o", "O" ]


x = list(range(1, len(mean_asymptomatic_testing_list[0])))

plt.bar(x, mean_asymptomatic_testing_list[0][1:], label='ASY Testing', hatch = patterns[2])
plt.bar(x, mean_symptomatic_testing_list[0][1:], bottom= mean_asymptomatic_testing_list[0][1:], label='SY Testing', hatch = patterns[1])
plt.legend(loc=4)


y_upper_error = [ x-y for x,y in zip(upper_asymptomatic_testing_list[0][1:], mean_asymptomatic_testing_list[0][1:])]
ax.errorbar(x, mean_asymptomatic_testing_list[0][1:], yerr = y_upper_error, color = "k", capsize=6, fmt=".", ms = 0.0001, elinewidth=2, capthick = 2)

plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(10))

plt.xlabel(r'Decision points $\bf{d}$', fontsize=35) 
plt.ylabel("POMDP action", fontsize=35)

plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(150))

plt.tight_layout()

plt.savefig("./Plots/Asymptomatic_Testing_Number.png", dpi = 400)
plt.close(fig)




