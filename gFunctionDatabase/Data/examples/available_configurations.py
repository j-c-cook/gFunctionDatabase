import gFunctionDatabase as gfdb
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def make_bar_chart(configurations):


    fig, ax = plt.subplots(1, 2, sharex=True, sharey=True)

    fig_count = 0
    row_count = 0
    col_count = 0

    for i in range(len(configurations)):
        configuration = configurations[i]

        db = gfdb.Management.retrieval.Retrieve(configuration)
        boundaries = db.query_database()

        x = []
        y = []

        for key in boundaries:
            first_pair = boundaries[key][0]
            second_pair = boundaries[key][1]
            x.append(first_pair[0])
            y.append(second_pair[1])

        ax[row_count].bar(x, y)
        ax[row_count].set_title(configuration)

        ax[row_count].xaxis.set_minor_locator(MultipleLocator(1))
        ax[row_count].yaxis.set_minor_locator(MultipleLocator(1))

        ax[row_count].grid()
        ax[row_count].set_axisbelow(True)

        row_count += 1

        if row_count == 2:
            row_count = 0
            col_count = 0

            fig.text(0.5, 0.03, 'Number of boreholes in x-direction',
                     ha='center')
            fig.text(0.04, 0.5, 'Number of boreholes in y-direction',
                     va='center', rotation='vertical')

            fig.savefig(str(fig_count) + 'layout_subplots.png')
            plt.close(fig)
            fig_count += 1

            fig, ax = plt.subplots(1, 2, sharex=True, sharey=True)



    # ax.set_xlabel('Number of boreholes in x-direction')
    # ax.set_ylabel('Number of boreholes in y-direction')
    #

def scatter_plot(configurations):

    fig, ax = plt.subplots()

    for configuration in configurations:

        db = gfdb.Management.retrieval.Retrieve(configuration)
        boundaries = db.query_database()

        x = []
        y = []

        for key in boundaries:
            first_pair = boundaries[key][0]
            second_pair = boundaries[key][1]
            x.append(first_pair[0])
            y.append(second_pair[1])

        ax.scatter(x, y, label=configuration, marker=configurations[configuration])

    ax.set_xlabel('Number of boreholes in x-direction')
    ax.set_ylabel('Number of boreholes in y-direction')

    ax.grid()
    ax.set_axisbelow(True)

    fig.legend(loc=1)
    return fig, ax


def main():
    # Available configurations driver function

    configurations = {'U': '$U$', 'Open': '.', 'rectangle': '$r$',
                      'LopU': '^', 'zoned': '*', 'C': '+', 'L': '1'}

    # make_bar_chart(configurations)
    fig, ax = scatter_plot(configurations)

    fig.savefig('available_database.png')


if __name__ == '__main__':
    main()
