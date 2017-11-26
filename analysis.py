# analysis, Anni, Zprime _ jj
import os, sys
import copy
import heppy.framework.config as cfg

import logging
import numpy as np

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

sys.path.append('/afs/cern.ch/work/h/helsens/public/FCCDicts/')
#sys.path.append('/afs/cern.ch/work/a/axiong/public/FCCsoft/FCCSW/output')

comp = cfg.Component(
    'example',
     files = ["root://eospublic.cern.ch///eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v01/pp_jj012j_5f_HT_0_500/events0.root"]
     #files = ["/afs/cern.ch/work/a/axiong/public/FCCsoft/FCCSW/output/sig/"]

)

from heppySampleList_fcc_v01 import *
#from heppySampleList_cms import *


selectedComponents = [
  
   pp_jj012j_5f_HT_0_500,
   #pp_jj012j_5f_HT_500_1000,
   #pp_jj012j_5f_HT_1000_2000,
                       
                       
                       ]

pp_jj012j_5f_HT_0_500.splitFactor = 5
'''
pp_ll012j_5f_HT_200_700.splitFactor = 10
pp_ll012j_5f_HT_700_1500.splitFactor = 10
pp_ll012j_5f_HT_1500_2700.splitFactor = 10
pp_ll012j_5f_HT_2700_4200.splitFactor = 10
pp_ll012j_5f_HT_4200_8000.splitFactor = 10
pp_ll012j_5f_HT_8000_15000.splitFactor = 10
pp_ll012j_5f_HT_15000_25000.splitFactor = 10
pp_ll012j_5f_HT_25000_35000.splitFactor = 10
pp_ll012j_5f_HT_35000_100000.splitFactor = 10
pp_Zprime_5TeV_ll.splitFactor = 10
pp_Zprime_10TeV_ll.splitFactor = 10
pp_Zprime_15TeV_ll.splitFactor = 10
pp_Zprime_20TeV_ll.splitFactor = 10
pp_Zprime_25TeV_ll.splitFactor = 10
pp_Zprime_30TeV_ll.splitFactor = 10
pp_Zprime_35TeV_ll.splitFactor = 10
pp_Zprime_40TeV_ll.splitFactor = 10
pp_Zprime_45TeV_ll.splitFactor = 10
pp_Zprime_50TeV_ll.splitFactor = 10
'''
#selectedComponents = [comp]

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,

    weights = 'mcEventWeights',

    gen_particles = 'skimmedGenParticles',

    electrons = 'electrons',
    electronITags = 'electronITags',
    electronsToMC = 'electronsToMC',

    muons = 'muons',
    muonITags = 'muonITags',
    muonsToMC = 'muonsToMC',

    jets = 'jets',
    bTags = 'bTags',

    photons = 'photons',
    
    pfphotons = 'pfphotons',
    pfcharged = 'pfcharged',
    pfneutrals = 'pfneutrals',

    met = 'met',

)

from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

#############################
##   Reco Level Analysis   ##
#############################


# select isolated muons with pT > 50 GeV and relIso < 0.4
'''

# select electrons with pT > 50 GeV and relIso < 0.4
selected_electrons = cfg.Analyzer(
    Selector,
    'selected_electrons',
    output = 'selected_electrons',
    input_objects = 'electrons',
    filter_func = lambda ptc: ptc.pt()>50 and ptc.iso.sumpt/ptc.pt()<0.4
    #filter_func = lambda ptc: ptc.pt()>5

)


# merge electrons and muons into a single lepton collection
from heppy.analyzers.Merger import Merger
selected_leptons = cfg.Analyzer(
      Merger,
      instance_label = 'selected_leptons', 
      inputs = ['selected_electrons','selected_muons'],
      output = 'selected_leptons'
)
'''
# select jet above 50 GeV
from heppy.analyzers.Selector import Selector
jets_50 = cfg.Analyzer(
    Selector,
    'jets_50',
    output = 'jets_50',
    input_objects = 'jets',
    filter_func = lambda ptc: ptc.pt()>30 and np.absolute(ptc.eta())<2.8
)

'''
from heppy.FCChhAnalyses.Zprime_ll.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# create Z' boson candidates
from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
zprime_ele = cfg.Analyzer(
      ResonanceBuilder,
      output = 'zprime_ele',
      leg_collection = 'selected_electrons',
      pdgid = 32
)

# create Z' boson candidates
from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
zprime_muon = cfg.Analyzer(
      ResonanceBuilder,
      output = 'zprime_muon',
      leg_collection = 'selected_muons',
      pdgid = 32
)
'''

# apply event selection. 
from heppy.FCChhAnalyses.Zprime_jj.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# store interesting quantities into flat ROOT tree
from heppy.FCChhAnalyses.Zprime_jj.TreeProducer import TreeProducer
reco_tree = cfg.Analyzer(
    TreeProducer,
    
    jets='jets_50',
    #leptons='selected_leptons',
    met='met',
    #zprime_ele='zprime_ele',
    #zprime_muon='zprime_muon',

)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    #selected_muons,
    #selected_electrons,
    #selected_leptons,
    jets_50,
    #match_lepton_jets,
    #jets_nolepton,
    selection,
    #zprime_ele,
    #zprime_muon,
    reco_tree,
    ] )


config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper

    def next():
        loop.process(loop.iEvent+1)

    loop = Looper( 'looper', config,
                   nEvents=100,
                   nPrint=0,
                   timeReport=True)
    loop.process(6)
    print loop.event
