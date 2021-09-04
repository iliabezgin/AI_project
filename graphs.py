import pandas as pd
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import seaborn as sns
import numpy as np


def box_plot_plt(data_sets, labels):
	plt.style.use('seaborn')
	fig, ax = plt.subplots()
	ax.set_ylabel("Game score")
	ax.set_title('Game score distribution')

	ax.boxplot(data_sets, labels=labels, patch_artist=True)
	plt.show()


def box_plot_sns(data_sets, labels):
	sns.set_style("whitegrid")
	points_df = pd.DataFrame(data_sets)
	points_df = points_df.transpose()
	points_df.columns = labels
	points_df = points_df.melt()
	# x_name = 'Agent Type'
	# x_name = 'Heuristic'
	x_name = 'Agent'

	# y_name = 'Game score'
	y_name = 'Moves per minute'
	points_df.columns = [x_name, y_name]

	my_order = points_df.groupby(by=[x_name])[y_name].median().sort_values(ascending=False).index

	# sns.set(font_scale=1.5)
	# title = 'Greedy BFS single agent score using single heuristic'
	# title = 'Greedy BFS single agent score\nusing single and combined heuristics'
	# title = 'Greedy BFS triple agent speed'
	# title = 'Agents score using combined heuristic'

	title_font_size = 30
	labels_fontsize = 26 #16 for small
	ticks_fontsize = 18

	ax = sns.boxplot(data=points_df,
					 x=x_name,
					 y=y_name,
					 palette="pastel",
					 width = 0.5,
					 order=my_order)
					 # ,).set_title(title, fontsize=title_font_size)
	# plt.yticks(np.arange(0, plt.ylim()[1], 10000), fontsize=ticks_fontsize)
	plt.yticks(fontsize=ticks_fontsize)
	plt.xticks(rotation=10, fontsize=ticks_fontsize)
	plt.tight_layout()
	plt.xlabel(x_name, fontsize=labels_fontsize)
	plt.ylabel(y_name, fontsize=labels_fontsize)

	fig = plt.gcf()
	fig.set_size_inches(12.8, 9.6)

	plt.show()


# ValueError: style must be one of white, dark, whitegrid, darkgrid, ticks


def creat_box_plots(directory):
	output_files = [f for f in listdir(directory) if isfile(join(directory, f)) and f.split('.')[-1] == "csv"]
	full_files_paths = [join(directory, f) for f in output_files]
	points_lists = []
	speeds_lists = []
	for file in full_files_paths:
		lists = pd.read_csv(file, header=None, index_col=None).values.tolist()
		points_lists.append(lists[0])
		speeds_lists.append(lists[1])
	# with plt.style.context('ggplot'):

	labels = [name.split('.')[0][:-3] for name in output_files]
	box_plot_sns(speeds_lists, labels)
	# box_plot_plt(speeds_lists, labels)
	x = 0


if __name__ == '__main__':
	creat_box_plots("outputs/top")
