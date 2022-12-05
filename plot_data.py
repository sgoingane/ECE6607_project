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


def get_movement_matrix(pre, post):
    categories = pre[0]
    pre_data = pre[2]
    post_data = post[2]

    movement = np.zeros((len(categories), len(categories)))

    for cc in range(pre_data.shape[0]):
        for rr in range(pre_data.shape[1]):
            if pre_data[cc, rr] != '':
                found = np.where(post_data == pre_data[cc, rr])

                if found:
                    for f in range(len(found[0])):
                        movement[cc, found[0][f]] += 1
    print(movement)
    return movement


def plot_pie(pre, post):
    # plot the percentage of categories before and after networking
    fig = plt.figure(figsize=(12, 5))

    fig.add_subplot(121)
    plt.title("Percentage before networking")
    plt.pie(pre[1], wedgeprops={"linewidth": 2, "edgecolor": "white"}, labels=pre[0], autopct="%3.1f%%")

    fig.add_subplot(122)
    plt.title("Percentage after networking")
    plt.pie(post[1], wedgeprops={"linewidth": 2, "edgecolor": "white"}, labels=post[0], autopct="%3.1f%%")

    plt.show()
    fig.savefig('./media/pie_chart.png')


def plot_bar(pre, post):
    # plot the range and atd deviation before and after networking
    cat = ["pre-networking", "post-networking"]
    pre_data_bar = pre[1]
    post_data_bar = post[1]

    std_dev = [np.std(pre_data_bar / np.sum(pre_data_bar)) * 100, np.std(post_data_bar / np.sum(post_data_bar)) * 100]
    range_ = [(np.max(pre_data_bar / np.sum(pre_data_bar)) - np.min(pre_data_bar / np.sum(pre_data_bar))) * 100,
              (np.max(post_data_bar / np.sum(post_data_bar)) - np.min(post_data_bar / np.sum(post_data_bar))) * 100]

    # plot:
    fig, ax = plt.subplots(figsize=(5, 5))
    width = 0.3
    x = np.arange(len(cat))
    rects1 = ax.bar(x - width / 2, std_dev, width, label='Std')
    rects2 = ax.bar(x + width / 2, range_, width, label='Range')

    ax.set_xticks(x, cat)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.show()
    fig.savefig('./media/bar_chart.png')


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
    p.save(filename='./media/rank_chart.png', format="png", width=15, height=10, verbose=False)


def plot_heatmap(pre, post):
    move = get_movement_matrix(pre, post)

    fig = plt.figure(figsize=(5, 5))
    plt.xlabel('To'), plt.ylabel('From')
    plt.xticks(ticks=np.arange(len(pre[0])), labels=pre[0], rotation=90)
    plt.yticks(ticks=np.arange(len(pre[0])), labels=pre[0])

    hm = plt.imshow(move, cmap='inferno')
    plt.colorbar(hm)

    plt.tight_layout()
    plt.show()
    fig.savefig('./media/heatmap.png')


if __name__ == '__main__':
    pre_data = read_csv(path_pre_net)
    post_data = read_csv(path_post_net)

    plot_heatmap(pre_data, post_data)
    plot_pie(pre_data, post_data)
    plot_rank(pre_data, post_data)
    plot_bar(pre_data, post_data)
