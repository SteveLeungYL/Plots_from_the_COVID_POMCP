#include <iostream>
#include <fstream>
#include <random>
using namespace std;

int total_population = 89000;

double R0 = 2.0;
double theta = 1.0/5.0;
double gamma_I1_R = 1.0/14.0; // 2 days asymptomatic period.
double gamma_I2_R = 1.0/14.0;

double testing_sensitivity = 0.90;
double testing_specificity = 0.998;

double beta = R0 * (gamma_I1_R + gamma_I2_R) / 2.0 ;

double proportion_of_I2_get_symptomatic_testing = 0.3;
double asymptomatic_rate = 0.7;

double I_class_ratio = 0.00637;
double R_class_ratio = 0.0162;

double hospital_recovery_rate = 1.0 / 14.0;

int total_time_step = 30;
int total_run_count = 100;

int total_testing_number = 500;
int testing_group_number = 32;

double symptomatic_testing_positive_rate = 0.76;

int fix_action = 0;

void create_start_state(double &S, double &E, double &I1, double &I2, double &R, double &H){

    double I = (double)total_population * I_class_ratio;
    I1 = I * asymptomatic_rate;
    I2 = I - I1;
    E = 6.0/14.0 * I;

    R = total_population * R_class_ratio;

    S = total_population - E - I - R;

    H = 0.0;

    return;
}

void update_SEIR(double& S, double& E, double& I1, double& I2, double& R, double& H, double delta_t = 1.0){
    double ori_S, ori_E, ori_I1, ori_I2, ori_R, ori_H;
    ori_S = S;
    ori_E = E;
    ori_I1 = I1;
    ori_I2 = I2;
    ori_R = R;
    ori_H = H;

    double alpha_1 = asymptomatic_rate;
    double alpha_2 = 1.0 - alpha_1;
    double omega = hospital_recovery_rate;


    S = ori_S - (beta * (ori_I1 + ori_I2) * ori_S) / total_population;
    E = ori_E - theta * ori_E +  (beta * (ori_I1 + ori_I2) * ori_S) / total_population;
    I1 = ori_I1 - ori_I1 * gamma_I1_R + alpha_1 * theta * ori_E;
    I2 = ori_I2 - ori_I2 * gamma_I2_R + alpha_2 * theta * ori_E;

    H = ori_H - ori_H * omega;
    R = R + ori_I1 * gamma_I1_R + ori_I2 * gamma_I2_R + ori_H * omega;
}

void asymptomatic_testing(int testing_number, int testing_group_number, double &S, double &E, double &I1, double &I2,
                          double &R, double &H){

    random_device rd;
    mt19937_64 gen(rd());
    uniform_real_distribution<> rand_dis(0.0, 1.0);

    for (int i = 0; i < testing_number; i++){


        double current_tested_I1 = 0;
        double current_tested_I2 = 0;

        double current_tested_I1_pos = 0; // True_positive.
        double current_tested_I2_pos = 0; // True_positive.

        if (S < 0.0) S = 0.0;
        if (E < 0.0) S = 0.0;
        if (I1 < 0.0) S = 0.0;
        if (I2 < 0.0) S = 0.0;
        if (R < 0.0) S = 0.0;
        if (H < 0.0) H = 0.0;

        double proportion_of_I1 = I1 / (S + E + I1 + I2 + R);
        double proportion_of_I2 = I2 / (S + E + I1 + I2 + R);

        for (int j = 0; j < testing_group_number; j++){

            double temp_random = (double)rand_dis(gen);

            if (temp_random < proportion_of_I1){
                double temp_random_2 = (double)rand_dis(gen);
                if (temp_random_2 <= testing_sensitivity) {
                    current_tested_I1 += 1.0;
                    current_tested_I1_pos += 1.0;
                }
                else current_tested_I1 += 1.0;
            }

            else if (temp_random < proportion_of_I1 + proportion_of_I2){
                double temp_random_2 = (double)rand_dis(gen);
                if (temp_random_2 <= testing_sensitivity) {
                    current_tested_I2+=1.0;
                    current_tested_I2_pos += 1.0;
                }
                else current_tested_I2 += 1.0;
            }
        }

        if(current_tested_I1_pos || current_tested_I2_pos){

            I1 -= current_tested_I1_pos;
            if (I1 <0) I1 = 0.0;

            I2 -= current_tested_I2_pos;
            if (I2 < 0) I2 = 0.0;

            H += current_tested_I1_pos + current_tested_I2_pos;
            //            observation += (int) (current_tested_I1_pos + current_tested_I2_pos);
        }
        testing_number -= (current_tested_I1_pos + current_tested_I2_pos) * log(testing_group_number) / log(2.0);
    }
}

void symptomatic_testing(int testing_number, double &I2, double &H){

    double ori_I2 = I2;
    int current_tested_I2_pos = 0;

    testing_number = int(double(testing_number) * symptomatic_testing_positive_rate);

    random_device rd;
    mt19937_64 gen(rd());
    uniform_real_distribution<> rand_dis(0.0, 1.0);

    for (int i = 0; i < (int)ori_I2; i++){
        double temp_random = (double)rand_dis(gen);
        if ( temp_random <= (proportion_of_I2_get_symptomatic_testing * testing_sensitivity)){
            if (I2 > 0) {
                I2 -= 1;
                H += 1;
                current_tested_I2_pos += 1;
            } else{ // If I2 <= 0;
                I2 = 0;
                break;
            }
        }
        --testing_number;
        if (testing_number <= 0) break;
    }
    return;
}


int main() {
    //    ofstream outputfile;
    //    outputfile.open("./output.csv");
    //    outputfile << "cumulative_I"<<endl;

    ofstream SEIRoutputfile;
    SEIRoutputfile.open("./Fix_Action_SEIR.csv");
    SEIRoutputfile << "S,E,I1,I2,H,R,cum_I,Run_Count,total_population,R0_value,initial_I_ratio,total_testing_number" << endl;

    //    double I_class_ratio_array[4] = {0.0001, 0.0005, 0.005, 0.05};
    int total_population_list[4] = {50000, 100000, 150000, 200000};

    for (int total_population_index = 0; total_population_index < 4; total_population_index++ ) {

        //        I_class_ratio = I_class_ratio_array[I_class_ratio_index];
        //        R_class_ratio = I_class_ratio * 3.0;
        total_population = total_population_list[total_population_index];

        total_testing_number = int((double)total_population * 0.004);
        random_device rd;
        mt19937_64 gen(rd());
        uniform_int_distribution<int> rand_dis(1, total_testing_number);
        beta = R0 * (gamma_I1_R + gamma_I2_R) / 2.0;
        for (int i = 0; i < total_run_count; ++i) {

            double S = 50000.0, E = 0.0, I1 = 0.0, I2 = 0.0, H = 0.0, R = 0.0;

            int temp_random = 0;
            create_start_state(S, E, I1, I2, R, H);

            for (int j = 0; j < total_time_step; ++j) {

                update_SEIR(S, E, I1, I2, R, H);

//                int asymptomatic_testing_number = rand_dis(gen);
                int asymptomatic_testing_number = total_testing_number;
//                int asymptomatic_testing_number = total_testing_number/2;
//            int asymptomatic_testing_number = 0;

                int symptomatic_testing_number = total_testing_number - asymptomatic_testing_number;
                asymptomatic_testing(asymptomatic_testing_number, testing_group_number, S, E, I1, I2, R, H);
                symptomatic_testing(symptomatic_testing_number, I2, H);

                double current_cum_I = I1 + I2;

                cout << "Asymptomatic testing number: " << asymptomatic_testing_number << endl;

                //            if (i == 0)
                SEIRoutputfile << S << ", " << E << ", " << I1 << ", " << I2 << ", " << H << ", " << R << ", "
                               << current_cum_I << ", " << i <<
                               ", " << total_population << ", " << R0 << ", " << I_class_ratio << ", "
                               << total_testing_number << endl;
            }

            //        SEIRoutputfile << S << ", " << E << ", " << I1 << ", " << I2 << ", " << H << ", " << R << ", " << i  << endl;


            //            double cum_I = I1 + I2 + R;

            //        double mean_testing_number = total_testing_number / total_time_step;

            //            outputfile << cum_I << endl;

        }
    }


    //    outputfile.close();
    SEIRoutputfile.close();
    return 0;
}
