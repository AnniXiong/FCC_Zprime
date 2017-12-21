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

#sys.path.append('/afs/cern.ch/work/h/helsens/public/FCCDicts/')
#sys.path.append('/afs/cern.ch/work/a/axiong/public/FCCsoft/FCCSW/output')
sys.path.append('afs/cern.ch/work/a/axiong/public/FCCsoft/')

comp = cfg.Component(
    'example',
     files = ["root://eospublic.cern.ch///eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v01/pp_jj012j_5f_HT_0_500/events0.root",
     "root://eospublic.cern.ch///eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v01/pp_jj012j_5f_HT_0_500/events1.root"
     ]
     #files = ["/afs/cern.ch/work/a/axiong/public/FCCsoft/FCCSW/output/sig/"]

)

from sample_dict import *

#from heppySampleList_fcc_v01 import *
#from heppySampleList_cms import *


selectedComponents = [
  
   #pp_Zprime_10TeV_ttbar
   pp_jj_HT_0_500,
   #pp_jj_HT_500_1000,
   #pp_jj_HT_1000_2000,
                       
                       
                 ]

#selectedComponents = [comp]
pp_jj_HT_0_500.splitFactor = 5
#pp_jj_HT_500_1000.splitFactor = 5
#pp_jj_HT_1000_2000.splitFactor = 5



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

# select jet above 50 GeV
from heppy.analyzers.Selector import Selector
jets_30 = cfg.Analyzer(
    Selector,
    'jets_30',
    output = 'jets_30',
    input_objects = 'jets',
    filter_func = lambda ptc: ptc.pt()>30 and np.absolute(ptc.eta())<2.5
)


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
    
    jets='jets_30',
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
    jets_30,
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
