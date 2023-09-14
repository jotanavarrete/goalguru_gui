import matplotlib.pyplot as plt
import numpy as np
import random

def show_probabilities_bar(prediction, category_names):
    '''
    This function receives a prediction from the API:
    prediction = {
        'outcome': 1,
        'probabilities': [0.56, 0.24, 0.20]
    }
    and returns the figure to be shown
    '''
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-gallery-lines-bars-and-markers-horizontal-barchart-distribution-py
    # https://stackoverflow.com/questions/5306756/how-to-print-a-percentage-value
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_label_demo.html#sphx-glr-gallery-lines-bars-and-markers-bar-label-demo-py

    # category_names = ['local wins', 'teams draw', 'away wins']
    labels = ['probabilities']
    data = np.array(prediction['probabilities'])
    data_cum = data.cumsum()

    colormaps = ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                 'RdYlGn', 'Spectral', 'coolwarm']

    category_colors = plt.colormaps[random.choice(colormaps)](
        np.linspace(0.2, 0.75, data.shape[0]))

    fig, ax = plt.subplots(figsize = (7, 0.75))
    ax.set_xlim(0, np.sum(data, axis=0).max())
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[i]
        starts = data_cum[i] - widths
        rects = ax.barh(labels, widths, left=starts,
                        label=colname, color=color)
        text_color = 'black'
        ax.bar_label(rects, label_type='center', color=text_color, fmt='{:.0%}',
                     fontsize=12, fontweight='demi')
        leg = ax.legend(ncols=len(category_names), bbox_to_anchor=(0., 1.102, 1., .102),
                loc='lower left', fontsize='medium', mode="expand", borderaxespad=0.)
        leg.get_frame().set_alpha(.8)

    fig.patch.set_alpha(0)

    return fig

if __name__ == '__main__':
    prediction = {
        'outcome': 1,
        'probabilities': [0.56, 0.24, 0.20]
    }
    f = show_probabilities_bar(prediction, ['local wins', 'teams draw', 'away wins'])
    f.show()
