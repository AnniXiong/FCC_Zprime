//
//  hist_stack.c
//  
//  This program is to combine histograms from different samples
//  Created by Anni Xiong on 12/21/17.
//  The three root files (which contains kinematic variable distributions are present in the current directory before running this
//

#include <stdio.h>
#include <TFile.h>
#include <TCanvas.h>
#include <TH1F.h>

void hist_stack (){
    
    /*
    
     hist = [h1d_mjj, h1d_chi, h1d_delR, h1d_pt1, h1d_pt2, h1d_eta1, h1d_eta2, h1d_deleta, h1d_ht]
     title = ["dijet mass distribution","angular variable distribution","angular seperation","Lead pt distribution","Sublead pt distribution","Rapitity distribution","Rapitity distribution 2", "rapidity difference", "Jet Pt sum"]
    x_title = ["mjj (GeV)","chi",'del_R',"pt(GeV)","pt(GeV)","eta","eta","eta1-eta2","Ht (GeV)"]
    
     */
    
    // subject to change
    string object = "jj_delR";
    string title = "Delta R";
    string x_title = "del_R";
    
    
    THStack *stack = new THStack("hs","");
    TFile* f1 = new TFile ("hist_HT_0_500.root");
    TH1F* h1 = (TH1F*) gDirectory->Get(object.c_str());
    stack->Add(h1);
    
    TFile* f2 = new TFile ("hist_HT_500_1000.root");
    TH1F* h2 = (TH1F*) gDirectory->Get(object.c_str());
    stack->Add(h2);
    
    TFile* f3 = new TFile ("hist_HT_1000_2000.root");
    TH1F* h3 = (TH1F*) gDirectory->Get(object.c_str());
    stack->Add(h3);
    
    TCanvas *canvas = new TCanvas("canvas","canvas",10,10,600,400);
    TText T; T.SetTextFont(42); T.SetTextAlign(21);
    stack->Draw("nostack");
    
    T.DrawTextNDC(.5,.95,title.c_str());
    canvas->SetLogy();
    
    //TLegend *legend2 = new TLegend(0.65,.75,.85,.9,0);
    TLegend *legend2 = new TLegend(0.72,.75,.9,.9,0);
    legend2->AddEntry(h1,"HT_0_500");
    legend2->AddEntry(h2,"HT_500_1000");
    legend2->AddEntry(h3,"HT_1000_2000");
    legend2->Draw();
    
    stack->GetXaxis()->SetTitle(x_title.c_str());
    stack->GetYaxis()->SetTitle("# of events");
    canvas->Modified();
    //TFile* f = new TFile("result", "recreate");
    //cs->Write();
    
}
