import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from plotnine import *
from plydata import *
import pandas as pd

path_pre_net = os.getcwd() + "./data/pre_net_sorted.csv"
path_post_net = os.getcwd() + "./data/post_net_sorted.csv"


def read_csv(path):
    categories = []
    data = []

    with open(path, encoding="UTF-8") as data_file:
        data_csv = csv.reader(data_file)

        first = True
        for row in data_csv:
            if first:
                categories = row
                first, second = False, True
            else:
                data.append(row)

        counts = []
        data = np.transpose(np.array(data))

        for cc in range(data.shape[0]):
            cnt = len(data[cc]) - 1
            for rr in range(len(data[cc])):
                if data[cc, rr] == '':
                    cnt = rr
                    break

            counts.append(cnt)

    print("Categories: ", categories)
    print("    Counts: ", counts, '\n')

    return categories, counts, data


def plot_pie(pre, post):
    # plot the percentage of categories before and after networking
    fig = plt.figure(figsize=(8, 3))
    fig.add_subplot(121)
    plt.pie(pre[1], labels=pre[0])

    fig.add_subplot(122)
    plt.pie(post[1], labels=post[0])

    plt.show()


def plot_rank(pre, post):
    # plot the rank before and after networking
    data = []
    for i in range(len(pre[0])):
        data.append((pre[0][i], pre[1][i], post[1][i]))

    df = pd.DataFrame(data, columns=['category', 'pre', 'post'])
    df_ranked = (
            df
            >> define(
                pre_rank='pre.rank(method="min").astype(int)',
                post_rank='post.rank(method="min").astype(int)'
            )
    )

    def get_rank_change(x):
        if x['pre_rank'] > x['post_rank']:
            return 'down'
        elif x['pre_rank'] < x['post_rank']:
            return 'up'
        else:
            return 'same'

    df_ranked['change'] = df_ranked.apply(get_rank_change, axis=1)
    print(df_ranked)
    p = (ggplot(df_ranked)
         + geom_text(aes(1, 'pre_rank', label='category', color='change'), nudge_x=-0.08, ha='right', size=17)
         + geom_text(aes(2, 'post_rank', label='category', color='change'), nudge_x=0.08, ha='left', size=17)
         + geom_point(aes(1, 'pre_rank', color='change'), size=3.5)
         + geom_point(aes(2, 'post_rank', color='change'), size=3.5)
         + geom_segment(aes(x=1, y='pre_rank', xend=2, yend='post_rank', color='change'))
         + annotate('text', x=1.5, y=6, label='Lines show change in rank', size=12, color='gray', fontstyle='italic')
         + annotate('text', x=1, y=10, label='Rank pre-networking', fontweight='bold', ha='right', size=19,
                    color='gray')
         + annotate('text', x=2, y=10, label='Rank post-networking', fontweight='bold', ha='left', size=19,
                    color='gray')

         # Prevent category names from being chopped off
         + lims(x=(0.3, 2.65))
         + labs(color='category')
         # Change colors
         + scale_color_brewer(type='qual', palette=2)
         # Removes all decorations
         + theme_void()
         # Changing the figure size prevents the category names from squishing up
         + theme(figure_size=(15, 10))
         )

    print(p)


if __name__ == '__main__':
    pre_data = read_csv(path_pre_net)
    post_data = read_csv(path_post_net)

    plot_pie(pre_data, post_data)
    plot_rank(pre_data, post_data)
