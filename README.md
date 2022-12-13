# ECE6607 Project 
 Computer Communication Networks 2022 Fall

**Team Members:** Jordan Hawkes, Ghaly Jules, Matthew Pleskow, Yinuo Wang, Renjie Yao, Xiaocheng Chen

## Topic
Topic 2: Focus on developing visualization for the impact of networking

## Dataset
* 5 suggestions each person before and after networking (reviewing others' suggestions)
* Initial data: `/data/data.xlsx`
* Automatically processed & clustered data: `/data/*_net.csv`
* Manually processed & clustered data (used in visualization): `/data/*_net_sorted.csv`

## Visualization
* Pie chart of different categories' percentage
* Ranking chart of different categories
* Bar chart for max-min range and standard deviation of category percentage

## Dependency
### Python Library
* csv
* numpy
* matplotlib
* plotnine
* plydata
* pandas
* openpyxl


## Run
* To visualize above charts, run `plot_data.py`
* To play with automatically word-matching based clustering, run `data_preprocessing.py`

