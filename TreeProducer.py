#  TreeProducer, Anni, Zprime _ jj
from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *
import numpy as np
from ROOT import TFile

class TreeProducer(Analyzer):

	def beginLoop(self, setup):
        	super(TreeProducer, self).beginLoop(setup)
        	self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        	self.tree = Tree( 'events', '')
        	self.tree.var('weight', float)

        
		#add the Ht variable
        	self.tree.var('Ht', float)
        	self.tree.var('rapd',float)
        	bookParticle(self.tree, 'jet1')
        	bookParticle(self.tree, 'jet2')
        	bookParticle(self.tree, 'jet3')
        

        	bookMet(self.tree, 'met')


	
	def process(self, event):
		self.tree.reset()
                self.tree.fill('weight' , event.weight )
		met = getattr(event, self.cfg_ana.met)
		fillMet(self.tree, 'met', met)
        	# getting the untrimmed jets
		jj = getattr(event,'jets')
     	
		# filling Ht
		ht = 0
		for ijets, j in enumerate(jj):
			ht = ht + j.pt()
     		self.tree.fill('Ht', ht )
     	
     		jets = getattr(event, self.cfg_ana.jets)
		rap = np.absolute( jets[0].eta() - jets[1].eta())
		self.tree.fill('rapd', rap )
		
		
        	for ijet, jet in enumerate(jets):
            		if ijet==3:
                		break
            		fillParticle(self.tree, 'jet{ijet}'.format(ijet=ijet+1), jet)

		self.tree.tree.Fill()

    	def write(self, setup):
        	self.rootfile.Write()
        	self.rootfile.Close()
        
