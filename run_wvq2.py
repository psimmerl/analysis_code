import ROOT, sys, os

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptFit(0011)

ff =  ROOT.TFile('q2w_hs.root')#sys.argv[1])

target = [4]

if 1 in target: #len(h1s) > 0:
  h1s =[ff.Get("hq2w_sec"+str(sec)+"_q2bin"+str(q2bin)) for sec in range(1,7) for q2bin in range(10)]
  c1 = ROOT.TCanvas("c1","c1",2200,1600)
  c1.Divide(5,2)
  for sec in range(6):
    #l1 = ROOT.TLegend(.75,.8,.95,.95)
    for i in range(10):
      #l1.AddEntry(h1s[sec*10+i], "Sector "+str(sec))
      c1.cd(i+1)
      h1s[sec*10+i].Fit("gaus","","",0.75,1.1)
      h1s[sec*10+i].Draw("same")
      #l1.Draw()
      #h1s[sec*10+i].SetLineColor(sec)
  c1.Print("hists/out10h6s.pdf")

if 2 in target: #len(h1s) > 0:
  h1s = [ff.Get("hq2w_q2bin"+str(q2bin)) for q2bin in range(10)]
  c2 = ROOT.TCanvas("c2","c2",2200,1600)
  c2.Divide(5,2)
  for i in range(10):
    c2.cd(i+1)
    h1s[i].Fit("gaus","","",0.75,1.1)
    h1s[i].Draw()
  c2.Print("hists/out10h.pdf")

if 3 in target: #len(h1s) > 0:
  h1s = [ff.Get("hq2w_sec"+str(sec)) for sec in range(1,7)]
  c3 = ROOT.TCanvas("c3","c3",2200,1600)
  c3.Divide(3,2)
  for sec in range(6):
    c3.cd(sec+1)
    h1s[sec].Fit("gaus","","",0.75,1.1)
    h1s[sec].Draw()
  c3.Print("hists/out6s.pdf")
  
if 4 in target: #len(h1s) > 0:
  h1s = [ff.Get("hq2w_complete")]
  c4 = ROOT.TCanvas("c4","c4",2200,1600)
  c4.cd()
  h1s[0].Fit("gaus","","",0.75,1.1)
  h1s[0].Draw()
  c4.Print("hists/out1h.pdf")
