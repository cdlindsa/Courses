# Cameron Lindsay

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lifelines.statistics import multivariate_logrank_test
from lifelines import KaplanMeierFitter
from lifelines.utils import median_survival_times
from sklearn.preprocessing import LabelBinarizer


if __name__ == "__main__":
    # Database is to be kept locally
    dataset = pd.read_csv("KMdatabase.csv", sep=',')
    ax = plt.subplot(111)

    med_75k_plus = (dataset["Median household income inflation adj to 2018"] == "$75,000+")
    med_70k = (dataset["Median household income inflation adj to 2018"] == "$70,000 - $74,999")
    med_65k = (dataset["Median household income inflation adj to 2018"] == "$65,000 - $69,999")
    med_60k = (dataset["Median household income inflation adj to 2018"] == "$60,000 - $64,999")
    med_55k = (dataset["Median household income inflation adj to 2018"] == "$55,000 - $59,999")
    med_50k = (dataset["Median household income inflation adj to 2018"] == "$50,000 - $54,999")
    med_45k = (dataset["Median household income inflation adj to 2018"] == "$45,000 - $49,999")
    med_40k = (dataset["Median household income inflation adj to 2018"] == "$40,000 - $44,999")
    med_35k = (dataset["Median household income inflation adj to 2018"] == "$35,000 - $39,999")
    med_35k_minus = (dataset["Median household income inflation adj to 2018"] == "< $35,000")
    obs = dataset["SEER cause-specific death classification"]
    lb = LabelBinarizer()
    obs = lb.fit_transform(obs)  
    durations = dataset['Survival months']

    kmf1 = KaplanMeierFitter()
    kmf1.fit(durations[med_75k_plus], event_observed=obs[med_75k_plus], label="75,000+")
    kmf1.plot(ax=ax)

    kmf2 = KaplanMeierFitter()
    kmf2.fit(durations[med_50k], event_observed=obs[med_50k], label="50,000-55,000")
    kmf2.plot(ax=ax)

    kmf3 = KaplanMeierFitter()
    kmf3.fit(durations[med_35k_minus], event_observed=obs[med_35k_minus], label="<35,000")
    kmf3.plot(ax=ax)
    plt.savefig("KaplanMeier_3_incomes.png")
    plt.show()
    plt.title("Kaplan Meier Observing Median Incomes")
    plt.clr
    
    # Logrank Test 
    # H0:h1(t)=h2(t)=h3(t)=...=hn(t)
    # HA:there exist at least one group that differs from the other.
    result = multivariate_logrank_test(durations, dataset["Median household income inflation adj to 2018"], obs)
    print(result.test_statistic)
    print(result.p_value)
    result.print_summary()
