# -*- coding: utf-8 -*-
import config

class Event():

    def __init__(self, g1, g2, inclusion, inversed_inclusion, inclusions):
        self.alpha = config.ALPHA
        self.beta = config.BETA
        self.g1 = g1
        self.g2 = g2
        self.g1_size = len(g1)
        self.g2_size = len(g2)
        self.inclusion = inclusion
        self.inversed_inclusion = inversed_inclusion
        self.inclusions = inclusions
        self.events = {1:'merging',
                       2:'splitting',
                       3:'growing',
                       4:'shrinking',
                       5:'continuing',
                       6:'dissolving',
                       7:'forming',
                       0:'no_event'}

    def is_merging(self,):
        if ((self.inclusion >= self.alpha) and
            (self.inversed_inclusion < self.beta) and
            (self.g1_size <= self.g2_size) and
            (self.check_matchings(self.g1, 'network_t0') == 'more')):
            return True

    def is_splitting(self,):
        if ((self.inclusion < self.alpha) and
            (self.inversed_inclusion >= self.beta) and
            (self.g1_size >= self.g2_size) and
            (self.check_matchings(self.g2, 'network_t1') == 'more')):
            return True

    def is_growing(self,):
        if ((self.inclusion >= self.alpha) and
            (self.inversed_inclusion >= self.beta) and
            (self.g1_size < self.g2_size)):
            #~ print "Growing from",self.g1.graph,"to",self.g2.graph
            return True

    def is_shrinking(self,):
        if ((self.inclusion >= self.alpha) and
            (self.inversed_inclusion >= self.beta) and
            (self.g1_size > self.g2_size)):
            #~ print "Shrinking",self.g1.graph,"to",self.g2.graph
            return True

    def is_continuing(self,):
        if ((self.inclusion >= self.alpha) and
            (self.inversed_inclusion >= self.beta) and
            (self.g1_size == self.g2_size)):
            #~ print "Continue",self.g1.graph,"to",self.g2.graph
            return True

    def is_dissolving(self,):
        g1_id = self.g1.graph['cid']
        g2_id = self.g2.graph['cid'].split('_')[0]
        coms = [group for group in self.inclusions if (g1_id == group.split('_')[0]+'_'+group.split('_')[1] and
                                                       g2_id in group)]
	
        for tupel in coms:
            if (self.inclusions[tupel]['inclusion'] > 0.1 and
                self.inclusions[tupel]['inversed_inclusion'] > 0.1):
                    return False
        comm = [c.split('_')[3] for c in coms]
        comm.sort(key=lambda x: int(filter(str.isdigit,x)))
        
        if not (self.g2.graph['cid'].split('_')[1] == comm[-1]):
            return False
        #~ print "Dissolving: past",self.g1.graph,"future",self.g2.graph
        return True

    def is_forming(self,):
        g2_id = self.g2.graph['cid']
        g1_id = self.g1.graph['cid'].split('_')[0]
        coms = [group for group in self.inclusions if (g1_id in group and
                                                       g2_id == group.split('_')[2]+'_'+group.split('_')[3])]
        
        for tupel in coms:
            if (self.inclusions[tupel]['inclusion'] > 0.1 and
                self.inclusions[tupel]['inversed_inclusion'] > 0.1):
                    return False
        comm = [c.split('_')[1] for c in coms]                                                                  #keep the all community ids of past TF
        comm.sort(key=lambda x: int(filter(str.isdigit,x)))
	
        if not (self.g1.graph['cid'].split('_')[1] == comm[-1]):                                                #to avoid multiple formation of the same community
            return False
        #~ print "Forming: past",self.g1.graph,"future",self.g2.graph
        return True

    def check_matchings(self, network, window):
        matches = 0
        events = [m for m in self.results if m[window]==network.graph['cid']]
        for e in events:
            if not e['resulted_event'] == 'no_event':
                matches += 1
        if matches == 1:
            return 'one'
        elif matches > 1:
            return 'more'
        else:
            return 'none'

    def check(self,):
        #~ if self.is_merging():
            #~ return 1
        #~ elif self.is_splitting():
            #~ return 2
        if self.is_growing():
            return 3
        elif self.is_shrinking():
            return 4
        elif self.is_continuing():
            return 5
        #~ elif self.is_dissolving():
            #~ return 6
        #~ elif self.is_forming():
            #~ return 7
        else:
            return 0

    def classify(self,):
        return self.events[self.check()]
