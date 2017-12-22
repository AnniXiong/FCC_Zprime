# HistogramProducer
# Anni
# Used Darshan's code for reference: https://cds.cern.ch/record/2288326

from ROOT import TFile, gDirectory, TH1F,TCanvas, TF1, TPaveLabel, TPad, TText, TLorentzVector,TColor, TChain
import ROOT.TColor
import numpy as np

#------------------------------------------------------------
# Expected number of events calculated                      #|
expected_Nevets_3ab_0_500 = 2.737140E+16                    #|
#expected_Nevets_10ab = 9.123800E+16                        #|
# HT_500_1000
expected_Nevets_3ab_500_1000 = 4.531920E+13                 #|
#expected_Nevets_10ab = 1.510640E+14                        #|
#HT_1000_2000
expected_Nevets_3ab_1000_2000 = 3.513300E+12                #|
#expected_Nevets_10ab = 1.171100E+13                        #|
# expected number of events actually used by histograms     #|
#expected_Nevets = 3.513300E+12                             
#-----------------------------------------------------------

#-------------------------------------------------------------------------
# Use one of the directories to change different sample                    #|
chunkdirectoty_0_500 = "Zprime_jj/out_0_500/pp_jj_HT_0_500_Chunk"        #|
chunkdirectoty_500_1000 = "Zprime_jj/out_500_1000/pp_jj_HT_500_1000_Chunk" #|
chunkdirectoty_1000_2000 = "Zprime_jj/out_1000_2000/pp_jj_HT_1000_2000_Chunk"#|
#chunkdirectory = "Zprime_sig/out_sig/example"
#-------------------------------------------------------------------------

def hist(sample,color, output, expected_Nevets):
	chain = TChain("events") 

	#files = glob("/afs/cern.ch/work/a/axiong/public/FCCsoft/heppy/FCChhAnalyses/Zprime_jj/out_0_500/*.root")
	homedirectory = "/afs/cern.ch/work/a/axiong/public/FCCsoft/heppy/FCChhAnalyses/"
	# ...Zprime_jj... depends on the location of TreeProducer.py used, subject to change
	rootfile = "/heppy.FCChhAnalyses.Zprime_jj.TreeProducer.TreeProducer_1/tree.root"


	# Add all files to TChain
	for i in range(5):
		filename = homedirectory + sample + str(i) + rootfile
		file = TFile(filename)
		chain.AddFile(filename)
		print ("root file from chunk" + str(i) + " is added")


	# declare histograms
	h1d_mjj = TH1F( 'jj_mass', '', 130, 0, 2000)
	h1d_pt1 = TH1F( 'jj_pt1', '', 130, 0, 1500)
	h1d_pt2 = TH1F( 'jj_pt2', '', 130, 0, 1000)
	h1d_eta1 = TH1F( 'jj_eta1', '', 25, -5.0, 5.0 )
	h1d_eta2 = TH1F( 'jj_eta2', '', 25, -5.0, 5.0 )
	h1d_chi = TH1F( 'jj_chi', '', 25, 0, 18)
	h1d_delR = TH1F('jj_delR','', 25,-1,6)
	h1d_ht = TH1F("ht",'',100,0,3000)
	h1d_deleta = TH1F('deleta','',20,-4,4)
	#mychain = chain.Get( 'events' )
	entries = chain.GetEntries()

	# Event loop
	for jentry in xrange(entries):
		ientry = chain.LoadTree(jentry)
		if ientry < 0:
			break
		nb = chain.GetEntry( jentry )
		if nb <= 0:
			continue
    
  		# feed data of two leading jets into TLorentzVector
  		jet1 = TLorentzVector()
  		jet1.SetPtEtaPhiE(chain.jet1_pt, chain.jet1_eta, chain.jet1_phi, chain.jet1_e)
  		jet2 = TLorentzVector()
  		jet2.SetPtEtaPhiE(chain.jet2_pt, chain.jet2_eta, chain.jet2_phi, chain.jet2_e)
  		jet12 = jet1 +jet2
  
  		# Fill the histograms
  		h1d_mjj.Fill(jet12.M())
  		h1d_pt1.Fill(chain.jet1_pt)
  		h1d_pt2.Fill(chain.jet2_pt)
  		h1d_eta1.Fill(chain.jet1_eta)
  		h1d_eta2.Fill(chain.jet2_eta)
  	
  		dr = jet1.DeltaR(jet2)
  		h1d_delR.Fill(dr)
  
  		h1d_chi.Fill( np.exp(2*(np.absolute(chain.jet1_eta-chain.jet2_eta)) )  )
	    	h1d_deleta.Fill(chain.jet1_eta-chain.jet2_eta)
    		h1d_ht.Fill(chain.Ht)

	hist = [h1d_mjj, h1d_chi, h1d_delR, h1d_pt1, h1d_pt2, h1d_eta1, h1d_eta2, h1d_deleta, h1d_ht]
	title = ["dijet mass distribution","angular variable distribution","angular seperation","Lead pt distribution","Sublead pt distribution",
	"Rapitity distribution","Rapitity distribution 2", "rapidity difference", "Jet Pt sum"]
	x_title = ["mjj (GeV)","chi",'del_R',"pt(GeV)","pt(GeV)","eta","eta","eta1-eta2","Ht (GeV)"]

	color = [color]
	Line_color = color * 9

	f = TFile(output, "recreate")

	for i in range(9):
		hist[i].SetTitle(title[i])
		hist[i].GetXaxis().SetTitle(x_title[i])
		hist[i].GetYaxis().SetTitle('# of events')
		scale = expected_Nevets/hist[i].Integral()
		hist[i].SetLineColor(Line_color[i])
		hist[i].Scale(scale)
		hist[i].Write()
	print "finished processing the sample"
	print ""


hist (chunkdirectoty_0_500,1,"hist_HT_0_500.root",expected_Nevets_3ab_0_500)
hist (chunkdirectoty_500_1000,3,"hist_HT_500_1000.root",expected_Nevets_3ab_500_1000)
hist (chunkdirectoty_1000_2000,7,"hist_HT_1000_2000.root",expected_Nevets_3ab_1000_2000)


