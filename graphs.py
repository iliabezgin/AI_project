import pandas as pd
from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import seaborn as sns


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
	points_df.columns = ['Agent Type', 'Game score']
	ax = sns.boxplot(data=points_df,
					 x='Agent Type',
					 y='Game score',
					 palette="pastel",
					 width=0.5
					 ).set_title('Game score distribution')
	plt.show()


# ValueError: style must be one of white, dark, whitegrid, darkgrid, ticks


def creat_box_plots():
	output_files = [f for f in listdir("outputs") if isfile(join("outputs", f))]
	full_files_paths = [join("outputs", f) for f in output_files]
	points_lists = []
	speeds_lists = []
	for file in full_files_paths:
		lists = pd.read_csv(file, header=None, index_col=None).values.tolist()
		points_lists.append(lists[0])
		speeds_lists.append(lists[1])
	# with plt.style.context('ggplot'):

	labels = [name.split('.')[0] for name in output_files]
	box_plot_sns(points_lists, labels)
	x = 0


if __name__ == '__main__':
	creat_box_plots()
