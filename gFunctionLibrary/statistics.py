# Jack C. Cook
# Tuesday, February 2, 2021

"""
**statistics.py**

A module for computing statistics of g-functions for comparison.

The g-functions in the library all use Eskilson's original 27 ln(t/ts) points.
"""


def mpe(actual: list, predicted: list) -> float:
    """
    The following mean percentage error formula is used:

    .. math::
        MPE = \dfrac{100\%}{n}\sum_{i=0}^{n-1}\dfrac{a_t-p_t}{a_t}

    Parameters
    ----------
    actual: list
        The actual computed g-function values
    predicted: list
        The predicted g-function values

    Returns
    -------
    **mean_percent_error: float**
        The mean percentage error in percent

    """
    # the lengths of the two lists should be the same
    assert len(actual) == len(predicted)
    # create a summation variable
    summation: float = 0.
    for i in range(len(actual)):
        summation += (actual[i] - predicted[i]) / actual[i]
    mean_percent_error = summation * 100 / len(actual)
    return mean_percent_error
