import ROOT, sys, os, math

ROOT.gROOT.SetBatch()
#ROOT.gStyle.SetOptStat("")
#ROOT.gStyle.SetOptFit(0111)

ff =  ROOT.TFile('q2w_hs.root')#sys.argv[1])

target = [2,3,4,5]

def fitf( x, par):
  return par[0]*math.exp(-0.5*((x[0]-par[1])/par[2])**2)+par[3]+par[4]*x[0]+par[5]*(x[0]**2)
  #return self.background(x, par[3:])+self.gaussian(x, par[:3])
    
def background(x, par):
  return par[0]+par[1]*x[0]+par[2]*(x[0]**2)

def gaussian(x, par):
  return par[0]*math.exp(-0.5*((x[0]-par[1])/par[2])**2)
  #return par[0]/(par[2]*math.sqrt(2*math.pi))*math.exp(-0.5*((x[0]-par[1])/par[2])**2)

legend = ROOT.TLegend(0.1,0.6,0.5,0.9)
legend.SetTextFont(72)
legend.SetTextSize(0.04)

hists = []
fits = []
pros = []
bgs = []
ls = []

def my_draw(hists, fits, pros, bgs):
  hnum = len(hists)
  fits.append(ROOT.TF1("fit"+str(hnum), fitf, 0.7, 1.1, 6))
  fits[-1].SetLineWidth(4)

  pros.append(ROOT.TF1("pFit"+str(hnum), gaussian, 0.7, 1.1, 3))
  pros[-1].SetLineWidth(4)
  pros[-1].SetLineColor(ROOT.kMagenta)
  bgs.append(ROOT.TF1("bgFit"+str(hnum), background, 0.7, 1.1, 3))
  bgs[-1].SetLineWidth(4)
  bgs[-1].SetLineColor(ROOT.kGreen)

  if hnum > 16:
    ls.append(ROOT.TLegend(.1,.6,.4,.9))
  else:
    ls.append(ROOT.TLegend(.1,.6,.5,.9))
  ls[-1].SetTextFont(72)
  ls[-1].SetTextSize(0.04)

  hists[-1].GetXaxis().SetTitle("W (GeV)")
  hists[-1].SetStats(0)
  hists[-1].SetLineWidth(3)

  fits[-1].SetParameters(100, 0.94, 0.1, 100, 1, 0) 
  hists[-1].Fit(fits[-1], "R")
  hists[-1].Draw()

  pars = fits[-1].GetParameters()
  errs = fits[-1].GetParErrors()
  pros[-1].SetParameters(pars[0],pars[1],pars[2])
  pros[-1].Draw("same")
  bgs[-1].SetParameters(pars[3],pars[4],pars[5])
  bgs[-1].Draw("same")

  ls[-1].AddEntry(hists[-1],           "Data",           "l")
  ls[-1].AddEntry(fits[-1],            "Global Fit",     "l")
  ls[-1].AddEntry(bgs[-1],         "Background Fit", "l")
  ls[-1].AddEntry(pros[-1],     "Proton Fit",     "l") 
  ls[-1].AddEntry(None,"\mu {:.5f}".format(pars[1]), "")
  ls[-1].AddEntry(None," \pm{:.5f} GeV".format(errs[1]), "")
  ls[-1].AddEntry(None,"\sigma {:.5f}".format(pars[2]), "")
  ls[-1].AddEntry(None," \pm{:.5f} GeV".format(errs[2]), "")
  ls[-1].Draw()
  

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
  c2 = ROOT.TCanvas("c2","c2",2200,1600)
  c2p = ROOT.TCanvas("c2p","c2p",2200,1600)
  c2.Divide(5,2)
  c2p.Divide(5,2)
  for i in range(10):
    hists.append(ff.Get("hq2w_q2bin"+str(i)))
    c2.cd(i+1)
    c2.SetGrid()
    my_draw(hists, fits, pros, bgs)
    
    hists.append(ff.Get("hq2w_q2bin"+str(i)+"_proton"))
    c2p.cd(i+1)
    c2p.SetGrid()
    my_draw(hists, fits, pros, bgs)
  c2.Print("hists/out10h.pdf")
  c2p.Print("hists/out10h_proton.pdf")

if 3 in target: #len(h1s) > 0:
  c3 = ROOT.TCanvas("c3","c3",2200,1600)
  c3p = ROOT.TCanvas("c3p","c3p",2200,1600)
  c3.Divide(3,2)
  c3p.Divide(3,2)
  for sec in range(6):
    hists.append(ff.Get("hq2w_sec"+str(sec+1)))
    c3.cd(sec+1)
    c3.SetGrid()
    my_draw(hists, fits, pros, bgs)
    
    hists.append(ff.Get("hq2w_sec"+str(sec+1)+"_proton"))
    c3p.cd(sec+1)
    c3p.SetGrid()
    my_draw(hists, fits, pros, bgs)
  c3.Print("hists/out6s.pdf")
  c3p.Print("hists/out6s_proton.pdf")

if 4 in target: #len(h1s) > 0:
  c4 = ROOT.TCanvas("c4","c4",2750,2000)
  c4.cd()
  c4.SetGrid()

  hists.append(ff.Get("hq2w_complete"))
  my_draw(hists, fits, pros, bgs)  
  c4.Print("hists/out1h.pdf")

if 5 in target: #len(h1s) > 0:
  c5 = ROOT.TCanvas("c5","c5",2750,2000)
  c5.cd()
  c5.SetGrid()
  
  hists.append(ff.Get("hq2w_proton"))
  my_draw(hists, fits, pros, bgs) 
  c5.Print("hists/out_proton.pdf")


#raw_input("Waiting for key")
