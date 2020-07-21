import ROOT, math

ROOT.gROOT.SetBatch()

ff =  ROOT.TFile('q2w_hs.root')#sys.argv[1])

def fitf( x, par):
  return par[0]*math.exp(-0.5*((x[0]-par[1])/par[2])**2)+par[3]+par[4]*x[0]+par[5]*(x[0]**2)
def background(x, par):
  return par[0]+par[1]*x[0]+par[2]*(x[0]**2)
def gaussian(x, par):
  return par[0]*math.exp(-0.5*((x[0]-par[1])/par[2])**2)

hW = [ff.Get("hq2w_sec"+str(i+1)+"_q2bin"+str(j)) for i in range(6) for j in range(10)]

def draw(hists, fits, pros, bgs, ls, dist):
  line_width = 2
  if dist is "proton":
    hists[-1].GetXaxis().SetRangeUser(0.7, 1.1)
    line_width = 4
  
  hnum = len(hists)
  fits.append(ROOT.TF1("fit"+str(hnum), fitf, 0.7, 1.1, 6))
  fits[-1].SetLineWidth(line_width)

  pros.append(ROOT.TF1("pFit"+str(hnum), gaussian, 0.7, 1.1, 3))
  pros[-1].SetLineWidth(line_width)
  pros[-1].SetLineColor(ROOT.kMagenta)
  bgs.append(ROOT.TF1("bgFit"+str(hnum), background, 0.7, 1.1, 3))
  bgs[-1].SetLineWidth(line_width)
  bgs[-1].SetLineColor(ROOT.kGreen)

  if hnum > 16:
    ls.append(ROOT.TLegend(.1,.6,.4,.9))
  else:
    ls.append(ROOT.TLegend(.1,.6,.5,.9))
  ls[-1].SetTextFont(72)
  ls[-1].SetTextSize(0.04)

  hists[-1].GetXaxis().SetTitle("W (GeV)")
  hists[-1].SetStats(0)
  hists[-1].SetLineWidth(line_width-1)

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

for dist in ["total", "proton"]:
  hists, fits, pros, bgs, ls = [], [], [], [], []
  min_lim, max_lim, bins = hW[0].GetXaxis().GetXmin(), hW[0].GetXaxis().GetXmax(), hW[0].GetXaxis().GetNbins()
  c = ROOT.TCanvas("c_"+dist,"c_"+dist,2200,1600)
  c.SetGrid()
  #TODO: 60
  
  # 10
  c.Clear()
  c.Divide(5,2)
  for i in range(10):
    c.cd(i+1)
    hists.append(ROOT.TH1F("h"+str(len(hists)), \
      "W (GeV) (Q^{2} "+str(i)+"-"+str(i+1)+" GeV^{2})",bins,min_lim,max_lim))
    for sec in range(6):
      hists[-1].Add(hW[sec*10+i])
    draw(hists, fits, pros, bgs, ls, dist)
    c.Print("hists/out10_"+dist+".pdf")

  # 6
  c.Clear()
  c.Divide(3,2)
  for sec in range(6):
    c.cd(sec+1)
    hists.append(ROOT.TH1F("h"+str(len(hists)),"Sector "+str(sec)+" W (GeV)",bins,min_lim,max_lim))
    for i in range(10):
      hists[-1].Add(hW[sec*10+i])
    draw(hists, fits, pros, bgs, ls, dist)
    c.Print("hists/out6_"+dist+".pdf")

  # 1
  c.Clear()
  hists.append(ROOT.TH1F("h"+str(len(hists)),"Total Response of W (Gev)",bins,min_lim,max_lim))
  for i in range(60):
    hists[-1].Add(hW[i])
  draw(hists, fits, pros, bgs, ls, dist)
  c.Print("hists/out1_"+dist+".pdf")


