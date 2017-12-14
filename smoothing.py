"""
SAMPLE USE
----------

numerator = np.array([   16571.27892744,        0.        ,        0.        ,
         133392.67046535,   289459.11764624,  1764017.34071272,
        4461422.23890683,  4972633.30089762,  2650896.19432251,
        1572781.46136745,   448428.84573707,   707640.67186649,
              0.        ,        0.        ,  6600160.58064695,
          25185.9359719 ])
denominator = np.array([  1.80000020e+07,   0.00000000e+00,   0.00000000e+00,
         1.29791626e+08,   2.85763974e+08,   8.17653651e+08,
         1.28900565e+09,   1.23902606e+09,   3.51914316e+08,
         1.12286109e+08,   3.99555295e+07,   2.13156040e+07,
         0.00000000e+00,   0.00000000e+00,   6.73040159e+07,
         5.65351265e+06])

r = numerator/denominator



vec, tracker = smoothVectorRatio(
    numerator=numerator,
    denominator=denominator,
    debug=True,
    plot=True
)

"""
import copy
import numpy as np
import math
import matplotlib.pyplot as plt

def isMonotonic(arr) -> bool:
    for i in range(1,len(arr)):
        if arr[i] < arr[i-1]:
            return(False)
    return(True)


def preProcess(arr: (list, tuple, np.ndarray), min_value: (int, float)= 0.0003) -> (list, tuple):
    pre_processed = copy.deepcopy(arr)
    for i in range(1,len(pre_processed)):
        if pre_processed[i] == 0.0:
            pre_processed[i] = min_value
    return(pre_processed)


def smoothVectorRatio(
    numerator: (list, tuple, np.ndarray),
    denominator: (list, tuple, np.ndarray),
    min_value: (int, float) = 0.0003,
    debug: bool = True,
    plot: bool= True
) -> (np.ndarray, np.ndarray):
    with np.errstate(divide='ignore', invalid='ignore'):
        raw = np.divide(numerator, denominator)
        raw[denominator == 0.] = 0
        raw = raw
    vec = preProcess(raw)
    tracker = copy.deepcopy(vec)

    while (isMonotonic(vec) == False):
        # BEGIN LOOP
        i = 0
        while (i < len(vec) - 1):
            if debug: print(">>> i : {}".format(str(i)))
            # CASE 1
            if (vec[i] == vec[i + 1] and vec[i] != min_value):
                if debug: print("\t>>> CASE 1")
                # LOOP TO COUNT HOW MANY TIMES current-item-ratio == next-item-ratio
                cnt = 0
                while(vec[i] == vec[i + cnt] and (i+cnt+1)<len(vec)):
                    cnt += 1
                    if debug: print("\t\t>>> COUNT LOOP : i = {} | i+cnt = {}".format(
                        str(i),
                        str(i + cnt)
                    ))
                if (vec[i] > vec[i + cnt]):
                    # CALCULATE RATIO FOR RANGE
                    numerator_range_sum = numerator[i:(i + cnt + 1)].sum()
                    denominator_range_sum = denominator[i:(i + cnt + 1)].sum()
                    if debug: print("\t\t>>> numerator_sum : {} | denominator_sum : {}".format(
                        str(numerator_range_sum),
                        str(denominator_range_sum)
                    ))
                    with np.errstate(divide='ignore', invalid='ignore'):
                        if denominator_range_sum == 0.0:
                            ratio = 0
                        else:
                            ratio = np.divide(numerator_range_sum, denominator_range_sum)
                    if debug: print("\t\t>>> ratio : {}".format(str(ratio)))
                    vec[i:(i + cnt + 1)] = ratio

                    # SKIP TO THE NEXT VECTOR ITEM
                    i = i + cnt
                else:
                    # DO NOTHING
                    vec[i:(i + cnt + 1)] = vec[i:(i + cnt + 1)]
            # CASE 2
            else:
                if (vec[i] > vec[i + 1] and vec[i] != min_value):
                    if debug: print("\t>>> CASE 2")
                    # CALCULATE RATIO FOR RANGE
                    numerator_range_sum = numerator[i:(i + 2)].sum()
                    denominator_range_sum = denominator[i:(i + 2)].sum()
                    if debug: print("\t\t>>> numerator_sum : {} | denominator_sum : {}".format(
                        str(numerator_range_sum),
                        str(denominator_range_sum)
                    ))
                    with np.errstate(divide='ignore', invalid='ignore'):
                        if denominator_range_sum == 0.0:
                            ratio = 0
                        else:
                            ratio = np.divide(numerator_range_sum, denominator_range_sum)
                    if debug: print("\t\t>>> ratio : {}".format(str(ratio)))
                    vec[i:(i + 2)] = ratio

                    # SKIP TO THE NEXT VECTOR ITEM
                    i += 1
                # CASE 3
                else:
                    if debug: print("\t>>> CASE 3")
                    # DO NOTHING
                    #vec[i] = vec[i]
                    pass

            # UPDATE COUNTER
            i = i + 1
        if debug: print("\n>>> CONCLUSION : vec is {}".format(("monotonic" if isMonotonic(vec) else "not monotonic")))
        if debug: print(vec)

        # ADD RESULT TO TRACKER
        tracker = np.vstack((tracker, vec))

    # PLOT
    if plot:
        idx = np.arange(len(vec))
        plt.plot(
            idx,
            tracker[0],
            'r--',
            idx,
            vec,
            'b-'
        )

    # RETURN RESULTS
    return vec, tracker

    # ans = input("Do you want to continue? [Y/N] ")
    # if ans == 'Y':
    #
    #     continue
    # else:
    #     break



