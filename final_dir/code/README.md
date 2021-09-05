AI final project. 1010! Game Agents

The program can be runned by execution of the following command: 
main.py [--agent={HumanAgent, GreedyBFSSingleAgent, GreedyBFSTripleAgent, AlphaBetaAgent}]
[--sleep] [--gui] [--repeat=REPEAT] [--output=OUTPUT] [--version=VERSION] [--depth=DEPTH]


--agent: Agent type (choose one of the given options). The default is HumanAgent;
--sleep: A boolean flag, if mentioned, then after each turn there will be a little pause (works only for computer agents and helps to follow the game flow);
--gui: A boolean flag, if mentioned, then the GUI will be shown;
--repeat: Choose a natural number of game repetitions. The default value is 1;
--output: Path to the existing output directory (with “/” at the end for unix platform and “\” for a windows one). If not mentioned, then output will be only printed, but not saved.
--version: If the chosen agent is alpha-beta, then this argument clarifies its version (1, 2 or 3). The default value is 2.
--depth: If the chosen agent is alpha-beta, then this argument sets the depth for the agent’s run. The default value is 0.

An example of input:
main.py --agent=GreedySingleAgent --sleep --gui --repeat=3 --output=output_dir/

