# HistogramProducer
# Anni
# Used Darshan's code for reference: https://cds.cern.ch/record/2288326

from ROOT import TFile, gDirectory, TH1F,TCanvas, TF1, TPaveLabel, TPad, TText, TLorentzVector,TColor, TChain
import ROOT.TColor
import numpy as np

#------------------------------------------------------------
# Expected number of events calculated                      #|
#expected_Nevets_3ab = 1.955100E+17                         #|
#expected_Nevets_10ab = 6.517000E+17                        #|
# HT_500_1000
#expected_Nevets_3ab = 4.926000E+14                         #|
#expected_Nevets_10ab = 1.642000E+15                        #|
#HT_1000_2000
#expected_Nevets_3ab = 5.019000E+13                         #|
#expected_Nevets_10ab = 1.673000E+14                        #|
# expected number of events actually used by histograms     #|
expected_Nevets = 1.955100E+17                              
#-----------------------------------------------------------

chain = TChain("events") 

#files = glob("/afs/cern.ch/work/a/axiong/public/FCCsoft/heppy/FCChhAnalyses/Zprime_jj/out_0_500/*.root")
homedirectory = "/afs/cern.ch/work/a/axiong/public/FCCsoft/heppy/FCChhAnalyses/"

#-------------------------------------------------------------------------
# Use one of the directories to change different sample                    #|
chunkdirectoty = "Zprime_jj/out1/pp_jj_HT_0_500_Chunk"        #|
#chunkdirectoty = "Zprime_jj1/out_500_1000/pp_jj012j_5f_HT_500_1000_Chunk"  #|
#chunkdirectoty = "Zprime_jj2/out_1000_2000/pp_jj012j_5f_HT_0_500_Chunk"   #|
#-------------------------------------------------------------------------

# ...Zprime_jj... depends on the location of TreeProducer.py used
rootfile = "/heppy.FCChhAnalyses.Zprime_jj.TreeProducer2.TreeProducer_1/tree.root"

# Add all files to TChain
for i in range(5):
	filename = homedirectory + chunkdirectoty + str(i) + rootfile
	file = TFile(filename)
	chain.AddFile(filename)
	print ("root file from chunk" + str(i) + " is added")


# declare histograms
h1d_mjj = TH1F( 'jj_mass', '', 100, 0, 1200)
h1d_pt1 = TH1F( 'jj_pt1', '', 100, 0, 1200)
h1d_pt2 = TH1F( 'jj_pt2', '', 100, 0, 1200)
h1d_eta1 = TH1F( 'jj_eta1', '', 5, -5.0, 5.0 )
h1d_eta2 = TH1F( 'jj_eta2', '', 5, -5.0, 5.0 )
h1d_chi = TH1F( 'jj_chi', '', 20, 0, 30 )
h1d_delR = TH1F('jj_delR','', 20,0,30)
h1d_deleta = TH1F('jj_deleta','',20,0,40)
h1d_ht = TH1F("Ht",'',100,0,1000)

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
  
  	#chi = np.exp(2*(np.absolute(jet1_eta-jet2_eta))
  	h1d_chi.Fill( np.exp(2*(np.absolute(chain.jet1_eta-chain.jet2_eta)) )  )
    	h1d_deleta.Fill( np.absolute(chain.jet1_eta-chain.jet2_eta))
    	h1d_ht.Fill(chain.Ht)

h1d_mjj.SetTitle("dijet mass distribution")
h1d_mjj.GetXaxis().SetTitle("mjj (GeV)")
h1d_mjj.GetYaxis().SetTitle("# of events")
scale = expected_Nevets/h1d_mjj.Integral()  # normalizing histogram
#h1d_mjj.SetLineColor(ROOT.kBlack+3);
h1d_mjj.SetFillColor(1)
h1d_mjj.Scale(scale)

h1d_chi.SetTitle("angular variable distribution")
h1d_chi.GetXaxis().SetTitle("chi")
h1d_chi.GetYaxis().SetTitle("# of events")
scale = expected_Nevets/h1d_chi.Integral()  # normalizing histogram
h1d_chi.SetLineColor(1);
h1d_chi.Scale(scale)

h1d_delR.SetTitle("angular seperation")
h1d_delR.GetXaxis().SetTitle("del_R")
h1d_delR.GetYaxis().SetTitle(" # of events")
scale = expected_Nevets/h1d_delR.Integral()  # normalizing histogram
h1d_delR.SetLineColor(1);
h1d_delR.Scale(scale)

# pt plot
h1d_pt1.SetTitle("pt distribution")
h1d_pt1.GetXaxis().SetTitle("pt (GeV)")
h1d_pt1.GetYaxis().SetTitle("# of events")
scale = expected_Nevets/h1d_pt1.Integral()  # normalizing histogram
h1d_pt1.SetLineColor(1);
h1d_pt1.Scale(scale)

h1d_pt2.SetTitle("angular variable distribution")
h1d_pt2.GetXaxis().SetTitle("chi")
h1d_pt2.GetYaxis().SetTitle("# of events")
scale = expected_Nevets/h1d_pt2.Integral()  # normalizing histogram
h1d_pt2.SetLineColor(7);
h1d_pt2.Scale(scale)

c1 = TCanvas( 'c1', 'pt', 600, 400 )
h1d_pt1.Draw("C")
h1d_pt2.Draw("same")
c1.Update()
#c1.SaveAs("pt.png")

h1d_eta1.SetTitle("rapitity distribution")
h1d_eta1.GetXaxis().SetTitle("eta")
h1d_eta1.GetYaxis().SetTitle("# of events")
scale = expected_Nevets/h1d_eta1.Integral()  # normalizing histogram
h1d_eta1.SetLineColor(1);
h1d_eta1.Scale(scale)

h1d_eta2.SetTitle("rapitity distribution")
h1d_eta2.GetXaxis().SetTitle("eta")
h1d_eta2.GetYaxis().SetTitle("# of events")
scale = expected_Nevets/h1d_eta2.Integral()  # normalizing histogram
h1d_eta2.SetLineColor(7);
h1d_eta2.Scale(scale)

h1d_deleta.SetTitle("rapitity difference")
h1d_deleta.GetXaxis().SetTitle("eta1-eta2")
h1d_deleta.GetYaxis().SetTitle("# of events")
scale = expected_Nevets/h1d_deleta.Integral()  # normalizing histogram
h1d_deleta.SetLineColor(7);
h1d_deleta.Scale(scale)

h1d_ht.SetTitle("Jet Pt sum")
h1d_ht.GetXaxis().SetTitle("eta")
h1d_ht.GetYaxis().SetTitle("# of events")
scale = expected_Nevets/h1d_ht.Integral()  # normalizing histogram
h1d_ht.SetLineColor(7);
h1d_ht.Scale(scale)



c2 = TCanvas( "c2","eta", 600, 400 )
h1d_eta1.Draw()
h1d_eta2.Draw("same")
c2.Update()


# write resulting histogram objects into a root file
f = TFile("hist_HT_0500.root", "recreate")
h1d_mjj.Write()
#h1d_pt1.Write()
#h1d_pt2.Write()
#h1d_eta1.Write()
h1d_delR.Write()
h1d_chi.Write()
c1.Write()
c2.Write()
