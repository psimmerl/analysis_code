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

fit = ROOT.TF1("fit", fitf, 0.7, 1.1, 6)
fit.SetLineWidth(4)

proton_fit = ROOT.TF1("pFit", gaussian, 0.7, 1.1, 3)
proton_fit.SetLineWidth(4)
proton_fit.SetLineColor(ROOT.kMagenta)
bg_fit = ROOT.TF1("bgFit", background, 0.7, 1.1, 3)
bg_fit.SetLineWidth(4)
bg_fit.SetLineColor(ROOT.kGreen)

legend = ROOT.TLegend(0.1,0.7,0.4,0.9)
legend.SetTextFont(72)
legend.SetTextSize(0.04)

def my_draw(hist):
  hist.GetXaxis().SetTitle("W (GeV)")
  hist.SetStats(0)
  hist.SetLineWidth(3)

  fit.SetParameters(500, 1, 0.1, 0, 0, 0) 
  hist.Fit(fit, "R")
  hist.Draw()

  pars = fit.GetParameters()
  errs = fit.GetParErrors()
  proton_fit.SetParameters(pars[0],pars[1],pars[2])
  proton_fit.Draw("same")
  bg_fit.SetParameters(pars[3],pars[4],pars[5])
  bg_fit.Draw("same")

  legend.Clear()
  legend.AddEntry(hist,           "Data",           "l")
  legend.AddEntry(fit,            "Global Fit",     "l")
  legend.AddEntry(bg_fit,         "Background Fit", "l")
  legend.AddEntry(proton_fit,     "Proton Fit",     "l") 
  legend.AddEntry(None,"\mu {:.5f}\pm{:.5f} GeV".format(pars[1],errs[1]), "")
  legend.AddEntry(None,"\sigma {:.5f}\pm{:.5f} GeV".format(pars[2],errs[2]), "")
  legend.Draw()


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
  c2.SetGrid()
  c2.Divide(5,2)
  h1s = [ff.Get("hq2w_q2bin"+str(q2bin)) for q2bin in range(10)]
  for i in range(10):
    c2.cd(i+1)
    my_draw(h1s[i])
  c2.Print("hists/out10h.pdf")

if 3 in target: #len(h1s) > 0:
  c3 = ROOT.TCanvas("c3","c3",2200,1600)
  c3.Divide(3,2)
  h1 = [ff.Get("hq2w_sec"+str(sec)) for sec in range(1,7)]
  for sec in range(6):
    c3.cd(sec+1)
    c3.SetGrid()
    my_draw(h1s[sec])

  c3.Print("hists/out6s.pdf")
  
if 4 in target: #len(h1s) > 0:
  c4 = ROOT.TCanvas("c4","c4",2750,2000)
  c4.cd()
  c4.SetGrid()

  h1s = [ff.Get("hq2w_complete")] 
  my_draw(h1s[0])  
  c4.Print("hists/out1h.pdf")

if 5 in target: #len(h1s) > 0:
  c5 = ROOT.TCanvas("c5","c5",2750,2000)
  c5.cd()
  c5.SetGrid()
  
  h1s = [ff.Get("hq2w_proton")]
  my_draw(h1s[0]) 
  c5.Print("hists/out_proton.pdf")


#raw_input("Waiting for key")
