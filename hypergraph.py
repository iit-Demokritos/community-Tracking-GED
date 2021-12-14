# -*- coding: utf-8 -*-
import networkx as nx
import random

class Hypergraph():
	def __init__(self,graph):
		### The hypergraph between 2 consecutive timeframes ###
		self.graph = graph
		self.GED_matched=	[]
		self.GED_dissolved=	[]
		self.GED_formed=	[]
		self.GED_other=		[]
		self.events_count = {'merging':0,'splitting':0,'growing':0,'shrinking':0,
              'continuing':0,'dissolving':0,'forming':0,'No_event':0}
		
	def getWindowId(self,):
		return self.graph.graph['window']
	def getPredictedMatched(self,):
		return self.GED_matched
	def getPredictedFormed(self,):
		return self.GED_formed
	def getPredictedDissolved(self,):
		return self.GED_dissolved
	def getPredictedOther(self,):
		return self.GED_other
	def getCid(self,node):
		return node.graph['cid'].split('_')[1][1:]
	def writeEvent(self,wid,cid,wid2,cid2,event,f):
		string = ','.join([wid,cid,wid2,cid2,event])+'\n'
		f.write(string)
		
		

	def getEventCount(self,):
		return self.events_count
	
	def calculateEvents(self,outfileD):			#file descriptor
		edges = self.graph.edges(data=True)
		TF = self.getWindowId().split()[0]
		past = int(TF[2:])
		pastTF = [node for node in self.graph.nodes() if node.graph['cid'].split('_')[0] == TF]
		lastNodePast = TF+'_c'+str(len(pastTF)-1)
		TF = self.getWindowId().split()[2]
		futureTF = [node for node in self.graph.nodes() if node.graph['cid'].split('_')[0]==TF]
		lastNodeFuture = TF+'_c'+str(len(futureTF)-1)
		outList = [[] for _ in range(5)]
		outList[0] = past
		outList[2] = past+1

		for tup in edges:
			SrcNode = tup[0]
			DstNode = tup[1]
			event = tup[2]['event_type']
			if SrcNode.graph['cid']==lastNodePast and event == 'forming':
				self.events_count[event] +=1
				#self.graph.remove_edge(SrcNode,DstNode)
				self.writeEvent('null','null',str(past+1),self.getCid(DstNode),event,outfileD)
				self.GED_formed.append(DstNode.graph['cid'])
			elif DstNode.graph['cid'] == lastNodeFuture and event == 'dissolving':
				self.events_count[event] +=1
				#self.graph.remove_edge(SrcNode,DstNode)
				self.writeEvent(str(past),self.getCid(SrcNode),'null','null',event,outfileD)
				self.GED_dissolved.append(SrcNode.graph['cid'])
			elif self.graph.in_degree(DstNode)==1 and self.graph.out_degree(SrcNode)==1:
				self.events_count[event] +=1
				self.writeEvent(str(past),self.getCid(SrcNode),str(past+1),self.getCid(DstNode),event,outfileD)
				
		for node in pastTF:
			out_degree = self.graph.out_degree(node)
			if out_degree >1:
				successors = self.graph.successors(node)
				for n in successors:
					self.writeEvent(str(past),self.getCid(node),str(past+1),self.getCid(n),'split',outfileD)
				self.events_count['splitting'] +=1
			elif out_degree ==0 and node.graph['cid'] not in self.GED_dissolved:
				self.events_count['No_event'] +=1
				self.writeEvent(str(past),self.getCid(node),'null','null','No_event',outfileD)
				
		for node in futureTF:
			in_degree = self.graph.in_degree(node)
			if in_degree >1:
				predecessors = self.graph.predecessors(node)
				for n in predecessors:
					self.writeEvent(str(past),self.getCid(n),str(past+1),self.getCid(node),'merge',outfileD)
				self.events_count['merging'] +=1
			elif in_degree==0 and node.graph['cid'] not in self.GED_formed:
				self.events_count['No_event'] +=1
				self.writeEvent('null','null',str(past+1),self.getCid(node),'No_event',outfileD)
