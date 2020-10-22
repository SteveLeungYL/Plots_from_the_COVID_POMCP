import pandas as pd
import numpy as np
import re
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib
import matplotlib.ticker as mtick

import scipy.stats

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m+h, m-h


total_population = 89000
total_testing_number = 500

sample_total_run_count = 100
total_time_step = 30




input_folder = "./"
all_files_name = os.listdir(input_folder)
all_files_name.sort()


mean_peak_H_list = []
mean_last_cum_I_list = []
mean_peak_I_list = []
mean_asymptomatic_testing_list = []
mean_symptomatic_testing_list = []

upper_peak_H_list = []
upper_last_cum_I_list = []
upper_peak_I_list = []
upper_asymptomatic_testing_list = []
upper_symptomatic_testing_list = []

lower_peak_H_list = []
lower_last_cum_I_list = []
lower_peak_I_list = []
lower_asymptomatic_testing_list = []
lower_symptomatic_testing_list = []

last_day_active_I_list = []

for group_number in [16, 32, 64]:
    
    data_name = "output_group_number_{}.csv.process_all.csv".format(
        group_number
    )
    current_model_data_all_runs = pd.read_csv(input_folder + data_name)

    I_current = []
    H_current = []
    asymptomatic_testing_current = []
    symptomatic_testing_current = []
    cum_I_current = []

    for sample_run_count in range(sample_total_run_count):
        current_model_data = current_model_data_all_runs[current_model_data_all_runs['Run'] == sample_run_count]

        I1 = current_model_data['I1'].tolist()

        I2 = current_model_data['I2'].tolist()

        I = [x+y for x,y in zip(I1, I2)]

        H = current_model_data['H'].tolist()
    
        R = current_model_data['R'].tolist()

        testing_types = current_model_data['Testing_Types'].tolist()

        asymptomatic_testing = [int(x * total_testing_number) for x in testing_types]
        asymptomatic_testing_current.append(asymptomatic_testing)
        symptomatic_testing_current.append([int(total_testing_number - x) for x in asymptomatic_testing])

        cum_I = [x + y for x, y in zip(I1, I2)]
        # cum_I = [x + y for x, y in zip(cum_I, H)]
        # cum_I = [x + y for x, y in zip(cum_I, R)]
        # cum_I = [x/num_of_population for x in cum_I]
        cum_I_current.append(cum_I)

        # I = [x/num_of_population for x in I]
        I_current.append(I)

        # H = [x/num_of_population for x in H]
        H_current.append(H)

    mean_cum_I_curve = []
    upper_cum_I_curve = []
    lower_cum_I_curve = []
    mean_H_curve = []
    upper_H_curve = []
    lower_H_curve = []
    mean_asymptomatic_testing_curve = []
    upper_asymptomatic_testing_curve = []
    lower_asymptomatic_testing_curve = []
    mean_symptomatic_testing_curve = []
    upper_symptomatic_testing_curve = []
    lower_symptomatic_testing_curve = []
    for i in range(len(cum_I_current[0])):

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

    cum_I_step = [x[-1] for x in cum_I_current]
    mean_cum_I_step, upper_cum_I_step, lower_cum_I_step = mean_confidence_interval(cum_I_step)
    mean_last_cum_I_list.append(mean_cum_I_step)
    upper_last_cum_I_list.append(upper_cum_I_step)
    lower_last_cum_I_list.append(lower_cum_I_step)

    H_step = [max(x) for x in H_current]
    mean_H_step, upper_H_step, lower_H_step = mean_confidence_interval(H_step)
    mean_peak_H_list.append(mean_H_step)
    upper_peak_H_list.append(upper_H_step)
    lower_peak_H_list.append(lower_H_step)

    # mean_last_cum_I_list.append(mean_cum_I_curve)
    # upper_last_cum_I_list.append(upper_cum_I_curve)
    # lower_last_cum_I_list.append(lower_cum_I_curve)

    # mean_peak_H_list.append(mean_H_curve)
    # upper_peak_H_list.append(upper_H_curve)
    # lower_peak_H_list.append(lower_H_curve)

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

    last_day_active_I_list.append(cum_I_step)



for fix_testing_number in [-1, 0, 100, 200]:

    if fix_testing_number == -1:
        data_name = "Random_Action_SEIR.csv"
        current_model_data = pd.read_csv(input_folder + data_name)
    else:
        data_name = "Fix_Action_SEIR_{}.csv".format(
        fix_testing_number
    )

    current_model_data = pd.read_csv(input_folder + data_name)



    for group_number in [16, 32, 64]:

        I_current = []
        H_current = []
        asymptomatic_testing_current = []
        symptomatic_testing_current = []
        cum_I_current = []

        for run_count in range(sample_total_run_count):
            current_sample_data = current_model_data[current_model_data['Run_Count'] == run_count]

            current_sample_data = current_sample_data[current_sample_data['group_number'] == group_number]

            I1 = current_sample_data['I1'].to_list()
            I2 = current_sample_data['I2'].to_list()
            I = [x+y for x,y in zip(I1, I2)]
            

            H = current_sample_data['H'].to_list()

            cum_I = current_sample_data['cum_I'].to_list()

            # cum_I = [x/total_population for x in cum_I]
            cum_I_current.append(cum_I)

            # H = [x/total_population for x in H]
            H_current.append(H)
            # I = [x/total_population for x in I]
            I_current.append(I)

        # mean_cum_I_curve = []
        # upper_cum_I_curve = []
        # lower_cum_I_curve = []
        # mean_H_curve = []
        # upper_H_curve = []
        # lower_H_curve = []
        # for i in range(len(cum_I_current[0])):
        #     cum_I_step = [x[i] for x in cum_I_current]
        #     mean_cum_I_step, upper_cum_I_step, lower_cum_I_step = mean_confidence_interval(cum_I_step)
        #     mean_cum_I_curve.append(mean_cum_I_step)
        #     upper_cum_I_curve.append(upper_cum_I_step)
        #     lower_cum_I_curve.append(lower_cum_I_step)

        #     H_step = [x[i] for x in H_current]
        #     mean_H_step, upper_H_step, lower_H_step = mean_confidence_interval(H_step)
        #     mean_H_curve.append(mean_H_step)
        #     upper_H_curve.append(upper_H_step)
        #     lower_H_curve.append(lower_H_step)

        cum_I_step = [x[-1] for x in cum_I_current]
        mean_cum_I_step, upper_cum_I_step, lower_cum_I_step = mean_confidence_interval(cum_I_step)
        mean_last_cum_I_list.append(mean_cum_I_step)
        upper_last_cum_I_list.append(upper_cum_I_step)
        lower_last_cum_I_list.append(lower_cum_I_step)

        last_day_active_I_list.append(cum_I_step)
 
        H_step = [max(x) for x in H_current]
        mean_H_step, upper_H_step, lower_H_step = mean_confidence_interval(H_step)
        mean_peak_H_list.append(mean_H_step)
        upper_peak_H_list.append(upper_H_step)
        lower_peak_H_list.append(lower_H_step)

        # mean_last_cum_I_list.append(mean_cum_I_curve)
        # upper_last_cum_I_list.append(upper_cum_I_curve)
        # lower_last_cum_I_list.append(lower_cum_I_curve)

        # mean_peak_H_list.append(mean_H_curve)
        # upper_peak_H_list.append(upper_H_curve)
        # lower_peak_H_list.append(lower_H_curve)

        peak_I_list = [max(x) for x in I_current]
        mean_peak_I, upper_peak_I, lower_peak_I = mean_confidence_interval(peak_I_list)

        mean_peak_I_list.append(mean_peak_I)
        upper_peak_I_list.append(upper_peak_I)
        lower_peak_I_list.append(lower_peak_I)

        # mean_cum_I_list.append(mean_cum_I_curve)
        # upper_cum_I_list.append(upper_cum_I_curve)
        # lower_cum_I_list.append(lower_cum_I_curve)

        # mean_H_list.append(mean_H_curve)
        # upper_H_list.append(upper_H_curve)
        # lower_H_list.append(lower_H_curve)

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

    
matplotlib.rcParams.update({'font.size': 27})
plt.rcParams["figure.figsize"] = [9.2,6]
plt.rcParams["font.family"] = "Times New Roman"


# Plot the cumulative I curve.

fig = plt.figure()
_, ax = plt.subplots()
total_width, n = 0.8, 5
width = total_width / n

xlabel = ["16", "32", "64"]

y_upper_error = [x - y for x,y in zip(upper_last_cum_I_list, mean_last_cum_I_list)]



x = list(range(len(mean_last_cum_I_list[0:3])))
plt.bar(x, mean_last_cum_I_list[0:3], width=width, label='POMCP')
ax.errorbar(x, mean_last_cum_I_list[0:3], yerr = y_upper_error[0:3], color = "k", capsize=3, fmt=".", ms = 0.0001)

x = [i + width for i in x]
plt.bar(x, mean_last_cum_I_list[3:6], width=width, label='Random', tick_label = xlabel)
ax.errorbar(x, mean_last_cum_I_list[3:6], yerr = y_upper_error[3:6], color = "k", capsize=3, fmt=".", ms = 0.0001)

x = [i + width for i in x]
plt.bar(x, mean_last_cum_I_list[6:9], width=width, label='Pure Symp')
ax.errorbar(x, mean_last_cum_I_list[6:9], yerr = y_upper_error[6:9], color = "k", capsize=3, fmt=".", ms = 0.0001)

x = [i + width for i in x]
plt.bar(x, mean_last_cum_I_list[9:12], width=width, label='Half Asymp, Half Symp')
ax.errorbar(x, mean_last_cum_I_list[9:12], yerr = y_upper_error[9:12], color = "k", capsize=3, fmt=".", ms = 0.0001)

x = [i + width for i in x]
plt.bar(x, mean_last_cum_I_list[12:15], width=width, label='Pure Asymp')
ax.errorbar(x, mean_last_cum_I_list[12:15], yerr = y_upper_error[12:15], color = "k", capsize=3, fmt=".", ms = 0.0001)

plt.legend(loc = 4)

plt.ylabel("Last Day Cumulative I / Total Population")

plt.savefig("./Plots/cumulative_I_curve.png")
plt.close(fig)

# Plot the advantages

mean_last_cum_I_array = np.array(mean_last_cum_I_list)

advantages_random = (mean_last_cum_I_array[3:6] - mean_last_cum_I_array[0:3]) / mean_last_cum_I_array[3:6] * 100
advantages_pure_symp = (mean_last_cum_I_array[6:9] - mean_last_cum_I_array[0:3]) / mean_last_cum_I_array[6:9] * 100
advantages_half_half = (mean_last_cum_I_array[9:12] - mean_last_cum_I_array[0:3]) / mean_last_cum_I_array[9:12] * 100
advantages_pure_asymp = (mean_last_cum_I_array[12:15] - mean_last_cum_I_array[0:3]) / mean_last_cum_I_array[12:15] * 100

last_day_active_I_array = np.array(last_day_active_I_list)

all_advantages_random = (last_day_active_I_array[3:6] - last_day_active_I_array[0:3]) / last_day_active_I_array[3:6] * 100
all_advantages_pure_symp = (last_day_active_I_array[6:9] - last_day_active_I_array[0:3]) / last_day_active_I_array[6:9] * 100
all_advantages_half = (last_day_active_I_array[9:12] - last_day_active_I_array[0:3]) / last_day_active_I_array[9:12] * 100
all_advantages_pure_asymp = (last_day_active_I_array[12:15] - last_day_active_I_array[0:3]) / last_day_active_I_array[12:15] * 100

upper_advantages_random = []
upper_advantages_symp = []
upper_advantages_half = []
upper_advantages_asymp = []

for i in range(3):
    _, upper_advantages_ran, _ = mean_confidence_interval(all_advantages_random[i])
    _, upper_advantages_sy, _ = mean_confidence_interval(all_advantages_pure_symp[i])
    _, upper_advantages_ha, _ = mean_confidence_interval(all_advantages_half[i])
    _, upper_advantages_as, _ = mean_confidence_interval(all_advantages_pure_asymp[i])

    upper_advantages_random.append(upper_advantages_ran)
    upper_advantages_symp.append(upper_advantages_sy)
    upper_advantages_half.append(upper_advantages_ha)
    upper_advantages_asymp.append(upper_advantages_as)

upper_advantages_random = upper_advantages_random - advantages_random
upper_advantages_symp = upper_advantages_symp - advantages_pure_symp
upper_advantages_half = upper_advantages_half - advantages_half_half
upper_advantages_asymp = upper_advantages_asymp - advantages_pure_asymp

fig = plt.figure()
_, ax = plt.subplots()
total_width, n = 0.8, 4
width = total_width / n

ax.yaxis.set_major_formatter(mtick.PercentFormatter())

patterns = [ "|" , "\\" , "/" , "+" , "-", ".", "*","x", "o", "O" ]


x = list(range(len(advantages_pure_symp)))
plt.bar(x, advantages_random, width=width, label='Random', hatch = patterns[9])
ax.errorbar(x, advantages_random, yerr = upper_advantages_random, color = "k", capsize=9, fmt=".", ms = 0.0001, elinewidth=5, capthick = 2)

x = [i + width for i in x]
plt.bar(x, advantages_pure_symp, width=width, label='SY', hatch = patterns[1])
ax.errorbar(x, advantages_pure_symp, yerr = upper_advantages_symp, color = "k", capsize=9, fmt=".", ms = 0.0001, elinewidth=5, capthick = 2)

x = [i + width for i in x]
plt.bar(x, advantages_half_half, width=width, label='50-ASY', tick_label = xlabel, hatch = patterns[5])
ax.errorbar(x, advantages_half_half, yerr = upper_advantages_half, color = "k", capsize=9, fmt=".", ms = 0.0001, elinewidth=5, capthick = 2)

x = [i + width for i in x]
plt.bar(x, advantages_pure_asymp, width=width, label='ASY', hatch = patterns[3])
ax.errorbar(x, advantages_pure_asymp, yerr = upper_advantages_asymp, color = "k", capsize=9, fmt=".", ms = 0.0001, elinewidth=5, capthick = 2)

plt.legend(loc = 1, ncol = 2)

plt.xlabel(r'Testing Pooling $\bf{\rho}$', fontsize=35)
plt.ylabel(r'% improvements', fontsize=35)

plt.tight_layout()

plt.savefig("./Plots/active_I_advantages.png", dpi=400)
plt.close(fig)




# Plot the Hospitalization

fig = plt.figure()
_, ax = plt.subplots()
total_width, n = 0.8, 4
width = total_width / n

xlabel = ["Testing Pool: \n16", "Testing Pool: \n32", "Testing Pool: \n64"]

y_upper_error = [x - y for x,y in zip(upper_peak_H_list, mean_peak_H_list)]


x = list(range(len(mean_peak_H_list[0:3])))
plt.bar(x, mean_peak_H_list[0:3], width=width, label='POMCP')
ax.errorbar(x, mean_peak_H_list[0:3], yerr = y_upper_error[0:3], color = "k", capsize=3, fmt=".", ms = 0.0001)

x = [i + width for i in x]
plt.bar(x, mean_peak_H_list[3:6], width=width, label='Pure Symp', tick_label = xlabel)
ax.errorbar(x, mean_peak_H_list[3:6], yerr = y_upper_error[3:6], color = "k", capsize=3, fmt=".", ms = 0.0001)

x = [i + width for i in x]
plt.bar(x, mean_peak_H_list[6:9], width=width, label='Half Asymp, Half Symp')
ax.errorbar(x, mean_peak_H_list[6:9], yerr = y_upper_error[6:9], color = "k", capsize=3, fmt=".", ms = 0.0001)

x = [i + width for i in x]
plt.bar(x, mean_peak_H_list[9:12], width=width, label='Pure Asymp')
ax.errorbar(x, mean_peak_H_list[9:12], yerr = y_upper_error[9:12], color = "k", capsize=3, fmt=".", ms = 0.0001)

plt.legend()

plt.ylabel("Peak Hospitalization / Total Population")

plt.savefig("./Plots/Hospitalization.png")
plt.close(fig)




# Plot the Peak Infectious number.

fig = plt.figure()
_, ax = plt.subplots()
total_width, n = 0.8, 4
width = total_width / n

xlabel = ["Testing Pool: \n16", "Testing Pool: \n32", "Testing Pool: \n64"]

y_upper_error = [x - y for x,y in zip(upper_peak_I_list, mean_peak_I_list)]


x = list(range(len(mean_peak_I_list[0:3])))
plt.bar(x, mean_peak_I_list[0:3], width=width, label='POMCP')
ax.errorbar(x, mean_peak_I_list[0:3], yerr = y_upper_error[0:3], color = "k", capsize=3, fmt=".", ms = 0.0001)

x = [i + width for i in x]
plt.bar(x, mean_peak_I_list[3:6], width=width, label='Pure Symp', tick_label = xlabel)
ax.errorbar(x, mean_peak_I_list[3:6], yerr = y_upper_error[3:6], color = "k", capsize=3, fmt=".", ms = 0.0001)

x = [i + width for i in x]
plt.bar(x, mean_peak_I_list[6:9], width=width, label='Half Asymp, Half Symp')
ax.errorbar(x, mean_peak_I_list[6:9], yerr = y_upper_error[6:9], color = "k", capsize=3, fmt=".", ms = 0.0001)

x = [i + width for i in x]
plt.bar(x, mean_peak_I_list[9:12], width=width, label='Pure Asymp')
ax.errorbar(x, mean_peak_I_list[9:12], yerr = y_upper_error[9:12], color = "k", capsize=3, fmt=".", ms = 0.0001)

plt.legend(loc = 4)

plt.ylabel("Peak I / Total Population")
plt.savefig("./Plots/Peak_I.png")
plt.close(fig)



# Plot the asymptomatic testing rate.

fig = plt.figure()
_, ax = plt.subplots()

x = list(range(len(mean_asymptomatic_testing_list)))
mean_sum_asymptomatic_testing_list = []
mean_sum_symptomatic_testing_list = []
upper_sum_asymptomatic_testing_list = []
upper_sum_symptomatic_testing_list = []

for i in range(len(mean_asymptomatic_testing_list)):
    mean_sum_asymptomatic_testing_list.append(sum(mean_asymptomatic_testing_list[i]))
    mean_sum_symptomatic_testing_list.append(sum(mean_symptomatic_testing_list[i]))

    upper_sum_asymptomatic_testing_list.append(sum(upper_asymptomatic_testing_list[i]))
    upper_sum_symptomatic_testing_list.append(sum(upper_symptomatic_testing_list[i]))

plt.bar(x, mean_sum_asymptomatic_testing_list, label='Asymptomatic Testing Number')
plt.bar(x, mean_sum_symptomatic_testing_list, bottom= mean_sum_asymptomatic_testing_list, label='Symptomatic Testing Number')
plt.legend(loc=4)


y_upper_error = [ x-y for x,y in zip(upper_sum_asymptomatic_testing_list, mean_sum_asymptomatic_testing_list)]
ax.errorbar(x, mean_sum_asymptomatic_testing_list, yerr = y_upper_error, color = "k", capsize=3, fmt=".", ms = 0.0001)

plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(2))

# plt.xlabel('Time Step(Days)')

plt.xticks(x, xlabel)

plt.ylabel('Testing Number')

plt.savefig("./Plots/Asymptomatic_Testing_Number.png")
plt.close(fig)




