# Jack C. Cook
# Tuesday, February 2, 2021

"""
statistics.py
A module for computing statistics of g-functions for comparison
"""


def mpe(actual: list, predicted: list) -> float:
    """
    Compute the mean percentage error formula

    .. math::
        MPE = \frac{100\%}{n}\sum_{i=0}^{n-1}\frac{a_t-p_t}{a_t}

    :param actual: The actual computed value
    :param predicted: The predicted value
    :return: the mean percentage error in percent
    """
    # the lengths of the two lists should be the same
    assert len(actual) == len(predicted)
    # create a summation variable
    summation: float = 0.
    for i in range(len(actual)):
        summation += (actual[i] - predicted[i]) / actual[i]
    mean_percent_error = summation * 100 / len(actual)
    return mean_percent_error
