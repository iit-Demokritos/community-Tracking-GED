# -*- coding: utf-8 -*-
import json
import networkx as nx
import preprocessing,config
import sys
import time
from inclusion import *
from event import Event
from hypergraph import Hypergraph

trueEvents = {'merging':0,'splitting':0,'growing':0,'shrinking':0,
              'continuing':0,'dissolving':0,'forming':0,'No_event':0}
		
class Tracker():

	def __init__(self, graphs):
		self.graphs = graphs
		self.communities = 	[]
		self.results = 		[]
		self.inclusions = 	{}
		self.Dcandidates = {}
		self.Fcandidates = {}
		self.hypergraphs = 	[]

	def compare_communities(self,):
		for index, interval in enumerate(self.graphs):
			if index < len(self.graphs) - 1:
				self.inclusions = {}
				window_id = 'TF%s -> TF%s' % (index,index+1)
				Dhypergraph = nx.DiGraph(window=window_id)
				print ('Initialize inclusions dict start...')
				Dhypergraph = self.initialize_inclusions(index,Dhypergraph)
				print ('Initialize inclusions dict finish...')
				
				for ic,community_t in enumerate(interval):
					
					for ic2, community_t1 in enumerate(self.graphs[index + 1]):

						inclusion = self.inclusions[community_t.graph['cid']][community_t1.graph['cid']]['inclusion']
						inversed = self.inclusions[community_t.graph['cid']][community_t1.graph['cid']]['inversed_inclusion']
						
						event = Event(community_t,community_t1,inclusion,inversed,self.inclusions)
						result = event.classify()
						if result in ['growing','shrinking','continuing']:
							Dhypergraph.add_edge(community_t,community_t1,event_type=result)
						self.results.append({ 'network_t': community_t.graph['cid'],
											 'network_t1': community_t1.graph['cid'],
											 'resulted_event': result})

				hypergraph = Hypergraph(Dhypergraph)
				self.hypergraphs.append(hypergraph)
				

	def initialize_inclusions(self,index,Dhypergraph):
		self.Dcandidates = {}
		self.Fcandidates = {}
		pastTFcommunities = self.graphs[index]
		futureTFcommunities = self.graphs[index+1]
		for ic,community_t in enumerate(pastTFcommunities):
			Dhypergraph.add_node(community_t)
			key1 = community_t.graph['cid']
			self.Dcandidates[key1] = community_t
			self.inclusions[key1]={}
			for ic2, community_t1 in enumerate(futureTFcommunities):
				key2 = community_t1.graph['cid']
				if ic==0:
							Dhypergraph.add_node(community_t1)
							self.Fcandidates[key2] = community_t1
							self.inclusions[key2] = {}
				inclusions = CentralityInclusion(community_t, community_t1)
				inclusion, inversed = inclusions.compute_inclusion()
				if inclusion >0.1 or inversed > 0.1:
					if key1 in self.Dcandidates:
						del self.Dcandidates[key1]
					if key2 in self.Fcandidates:
						del self.Fcandidates[key2]
				self.inclusions[key1].update({key2:{'inclusion':inclusion,'inversed_inclusion':inversed}})

		for key in self.Dcandidates.keys():
			Dhypergraph.add_edge(self.Dcandidates[key],futureTFcommunities[-1],event_type='dissolving')
		for key in self.Fcandidates.keys():
			Dhypergraph.add_edge(pastTFcommunities[-1],self.Fcandidates[key],event_type='forming')
		return Dhypergraph

	def analyze_results(self,):
		events_names = ['merging', 'splitting', 'growing',
						'shrinking', 'continuing', 'dissolving',
						'forming', 'no_event']
		events = [e['resulted_event'] for e in self.results]
		for name in events_names:
			print (name, events.count(name))

if __name__=='__main__':
	if len(sys.argv) !=	2:
		print ('Usage: Tracker.py <inputfile.json>')
		print ('Exiting with code 1')
		exit(1)
	start_time = time.time()
	graphs = preprocessing.getGraphs(sys.argv[1])
	tracker = Tracker(graphs)
	tracker.compare_communities()
	with open('ged_results.csv','w')as f:
		for hypergraph in tracker.hypergraphs:
			hypergraph.calculateEvents(f)
	print ("--- %s seconds ---" %(time.time() - start_time))
			

