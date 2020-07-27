import ROOT, math
from array import array

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
  else:#Run fit only once per dataset
    hnum = len(hists)
    fits.append(ROOT.TF1("fit"+str(hnum), fitf, 0.7, 1.1, 6))

    pros.append(ROOT.TF1("pFit"+str(hnum), gaussian, 0.7, 1.1, 3))
    pros[-1].SetLineColor(ROOT.kMagenta)
    bgs.append(ROOT.TF1("bgFit"+str(hnum), background, 0.7, 1.1, 3))
    bgs[-1].SetLineColor(ROOT.kGreen)

    if hnum > 16:
      ls.append(ROOT.TLegend(.1,.6,.4,.9))
    else:
      ls.append(ROOT.TLegend(.1,.6,.5,.9))
    ls[-1].SetTextFont(72)
    ls[-1].SetTextSize(0.04)

    hists[-1].GetXaxis().SetTitle("W (GeV)")
    hists[-1].SetStats(0)

    fits[-1].SetParameters(50, 0.9, 0.1, 100, 1, 0) 
    hists[-1].Fit(fits[-1], "R")

    pars = fits[-1].GetParameters()
    errs = fits[-1].GetParErrors()
    pros[-1].SetParameters(pars[0],pars[1],pars[2])
    bgs[-1].SetParameters(pars[3],pars[4],pars[5])

    ls[-1].AddEntry(hists[-1],           "Data",           "l")
    ls[-1].AddEntry(fits[-1],            "Global Fit",     "l")
    ls[-1].AddEntry(bgs[-1],         "Background Fit", "l")
    ls[-1].AddEntry(pros[-1],     "Proton Fit",     "l") 
    ls[-1].AddEntry(None,"\mu {:.5f}".format(pars[1]), "")
    ls[-1].AddEntry(None," \pm{:.5f} GeV".format(errs[1]), "")
    ls[-1].AddEntry(None,"\sigma {:.5f}".format(pars[2]), "")
    ls[-1].AddEntry(None," \pm{:.5f} GeV".format(errs[2]), "")
  
  fits[-1].SetLineWidth(line_width)
  pros[-1].SetLineWidth(line_width)
  bgs[-1].SetLineWidth(line_width)
  hists[-1].SetLineWidth(line_width-1)
  hists[-1].Draw()
  fits[-1].Draw("same")
  bgs[-1].Draw("same")
  pros[-1].Draw("same")
  ls[-1].Draw()  

def draw_graph(fname, title, x_name, y_name, x_entries, y_entries, x_err=None, y_err=None):
  if x_err is None:
    x_err = array("d", [0]*len(x_entries))
  if y_err is None:
    y_err = array("d", [0]*len(x_entries))
  c = ROOT.TCanvas("c","c",2200,1600)
  c.SetGrid()
  graph = ROOT.TGraphErrors(len(x_entries), x_entries, y_entries, x_err, y_err)
  graph.SetLineWidth(3)
  graph.SetTitle(title)
  graph.SetLineColor(ROOT.kRed)
  graph.GetXaxis().SetTitle(x_name)
  graph.GetYaxis().SetTitle(y_name)
  graph.SetMarkerStyle(8)
  graph.SetMarkerSize(3)
  graph.Draw("ALP")
  c.Print(fname)

hists, fits, pros, bgs, ls = [], [], [], [], []
min_lim, max_lim, bins = hW[0].GetXaxis().GetXmin(), hW[0].GetXaxis().GetXmax(), hW[0].GetXaxis().GetNbins()
ct = ROOT.TCanvas("ct","ct",2200,1600)
ct.SetGrid()
cp = ROOT.TCanvas("cp","cp",2200,1600)
cp.SetGrid()
  
#TODO: 60
  
# 10
ct.Clear()
cp.Clear()
ct.Divide(5,2)
cp.Divide(5,2)

g10_x = array("d")

for i in range(10):
  hists.append(ROOT.TH1F("h"+str(len(hists)), \
    "W (GeV) (Q^{2} "+str(i)+"-"+str(i+1)+" GeV^{2})",bins,min_lim,max_lim))
  for sec in range(6):
    hists[-1].Add(hW[sec*10+i])
  if i >= 5: 
    hists[-1].Rebin(5)

  ct.cd(i+1)
  draw(hists, fits, pros, bgs, ls, "total")
  cp.cd(i+1)
  draw(hists, fits, pros, bgs, ls, "proton")

  g10_x.append(i+0.5)

ct.Print("hists/out10_total.pdf")
cp.Print("hists/out10_proton.pdf")

draw_graph("hists/out10_Nentries_Q2.pdf","Entries in Proton vs Q^{2}", "Q^{2} (GeV^{2})", \
  "N Entries", g10_x, array("d", [pro.Integral(0.7,1.1) for pro in pros]))

draw_graph("hists/out10_muerr_Q2.pdf","Proton Peak (w/ fit errors) vs Q^{2}", "Q^{2} (GeV^{2})", \
  "Peak (Gev)", g10_x, array("d", [pro.GetParameter(1) for pro in pros]), None, \
  array("d", [pro.GetParError(1) for pro in pros]))

draw_graph("hists/out10_musig_Q2.pdf","Proton Peak (w/ \sigma as error) vs Q^{2}", \
  "Q^{2} (GeV^{2})", "Peak (GeV)", g10_x, array("d", [pro.GetParameter(1) for pro in pros]), None, \
  array("d", [pro.GetParameter(2) for pro in pros]))

# 6
ct.Clear()
cp.Clear()
ct.Divide(3,2)
cp.Divide(3,2)
for sec in range(6):
  hists.append(ROOT.TH1F("h"+str(len(hists)),"Sector "+str(sec)+" W (GeV)",bins,min_lim,max_lim))
  for i in range(10):
    hists[-1].Add(hW[sec*10+i])
  ct.cd(sec+1)
  draw(hists, fits, pros, bgs, ls, "total")
  cp.cd(sec+1)
  draw(hists, fits, pros, bgs, ls, "proton")
ct.Print("hists/out6_total.pdf")
cp.Print("hists/out6_proton.pdf")

# 1
ct.Clear()
cp.Clear()
hists.append(ROOT.TH1F("h"+str(len(hists)),"Total Response of W (Gev)",bins,min_lim,max_lim))
for i in range(60):
  hists[-1].Add(hW[i])
ct.cd()
draw(hists, fits, pros, bgs, ls, "total")
cp.cd()
draw(hists, fits, pros, bgs, ls, "proton")
ct.Print("hists/out1_total.pdf")
cp.Print("hists/out1_proton.pdf")


