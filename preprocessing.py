import json
import networkx as nx


def createGraphs(data):
	graphs=[]
	for timeIdx,window in enumerate(data['windows']):
		interval_graphs=[]
		for com_index,community in enumerate(window['communities']):
			com_id = 'TF'+str(timeIdx)+'_c'+str(com_index)
			G = nx.MultiDiGraph(cid=com_id)
			G.add_edges_from(community)
			interval_graphs.append(G)
		graphs.append(interval_graphs)
	return graphs
	

def getGraphs(communitiesfile):
	try:
		with open(communitiesfile) as f:
			data = json.load(f)
	except:
		print ("Cannot load %s file. Expecting <input>.json file" % communitiesfile)
		print ("Exiting with code 1\n")
		exit(1)
	graphs = createGraphs(data)
	return graphs
		

