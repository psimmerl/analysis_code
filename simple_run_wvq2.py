import ROOT, math
from array import array

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetEndErrorSize(10)

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

    fits[-1].SetParameters(100, 0.9, 0.1, 0, 0, 0) 
    fits[-1].SetParLimits(1, 0.7, 1.1)
    #fits[-1].SetParLimits(0, 0, 10e100)
    hists[-1].Fit(fits[-1], "QR")

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
  c = ROOT.TCanvas("cg","cg",2200,1600)
  c.SetGrid()
  graph = ROOT.TGraphErrors(len(x_entries), x_entries, y_entries, x_err, y_err)
  graph.SetLineWidth(2)
  graph.SetTitle(title)
  graph.SetMarkerColor(ROOT.kRed)
  graph.GetXaxis().SetTitle(x_name)
  graph.GetYaxis().SetTitle(y_name)
  graph.SetMarkerStyle(8)
  graph.SetMarkerSize(3)
  graph.Draw("ALP")
  c.Print(fname)

hists, fits, pros, bgs, ls = [], [], [], [], []
min_lim, max_lim, bins = hW[0].GetXaxis().GetXmin(), hW[0].GetXaxis().GetXmax(), hW[0].GetXaxis().GetNbins()
c = ROOT.TCanvas("c","c",2200,1600)
c.SetGrid()
   
# 10
c.Clear()
c.Divide(5,2)
for i in range(10):
  hists.append(ROOT.TH1F("h"+str(len(hists)), \
    "W (GeV) (Q^{2} "+str(i)+"-"+str(i+1)+" GeV^{2})",bins,min_lim,max_lim))
  for sec in range(6):
    hists[-1].Add(hW[sec*10+i])
  if i >= 5: 
    hists[-1].Rebin(5)
  c.cd(i+1)
  draw(hists, fits, pros, bgs, ls, "total")
c.Print("hists/out10_total.pdf")
for i in range(10):
  c.cd(i+1)
  draw([hists[-10+i]], [fits[-10+i]], [pros[-10+i]], [bgs[-10+i]], [ls[-10+i]], "proton")
c.Print("hists/out10_proton.pdf")

draw_graph("hists/graphs/out10_Nentries_Q2.pdf","Entries in Proton vs Q^{2}", "Q^{2} (GeV^{2})", \
  "N Entries", array("d",[x+0.5 for x in range(10)]), array("d", [hist.Integral( \
  int(math.floor(0.7*hist.GetXaxis().GetNbins()/(hist.GetXaxis().GetXmax()-hist.GetXaxis().GetXmin()))), \
  int(math.floor(1.1*hist.GetXaxis().GetNbins()/(hist.GetXaxis().GetXmax()-hist.GetXaxis().GetXmin())))) \
  for hist in hists]))

draw_graph("hists/graphs/out10_muerr_Q2.pdf","Proton Peak (w/ fit errors) vs Q^{2}", \
  "Q^{2} (GeV^{2})", "Peak (Gev)", array("d",[x+0.5 for x in range(10)]), array("d", [pro.GetParameter(1) for pro in \
  pros]), None, array("d", [fit.GetParError(1) for fit in fits]))

draw_graph("hists/graphs/out10_musig_Q2.pdf","Proton Peak (w/ \sigma as error) vs Q^{2}", \
  "Q^{2} (GeV^{2})", "Peak (GeV)", array("d",[x+0.5 for x in range(10)]), array("d", [pro.GetParameter(1) for pro in \
  pros]), None, array("d", [pro.GetParameter(2) for pro in pros]))

# 6
c.Clear()
c.Divide(3,2)
for sec in range(6):
  hists.append(ROOT.TH1F("h"+str(len(hists)),"Sector "+str(sec)+" W (GeV)",bins,min_lim,max_lim))
  for i in range(10):
    hists[-1].Add(hW[sec*10+i])
  c.cd(sec+1)
  draw(hists, fits, pros, bgs, ls, "total")
c.Print("hists/out6_total.pdf")
for sec in range(6):
  c.cd(sec+1)
  draw([hists[-6+i]], [fits[-6+i]], [pros[-6+i]], [bgs[-6+i]], [ls[-6+i]], "proton")
c.Print("hists/out6_proton.pdf")

draw_graph("hists/graphs/out6_Nentries_sec.pdf","Entries in Proton vs Sector", "Sector", \
  "N Entries", array("d",range(1,7)), array("d", [hist.Integral( \
  int(math.floor(0.7*hist.GetXaxis().GetNbins()/(hist.GetXaxis().GetXmax()-hist.GetXaxis().GetXmin()))), \
  int(math.floor(1.1*hist.GetXaxis().GetNbins()/(hist.GetXaxis().GetXmax()-hist.GetXaxis().GetXmin())))) for hist in hists[-6:]]))

draw_graph("hists/graphs/out6_muerr_sec.pdf","Proton Peak (w/ fit errors) vs Sector", "Sector", \
  "Peak (Gev)", array("d",range(1,7)), array("d", [pro.GetParameter(1) for pro in \
  pros[-6:]]), None, array("d", [fit.GetParError(1) for fit in fits[-6:]]))

draw_graph("hists/graphs/out6_musig_sec.pdf","Proton Peak (w/ \sigma as error) vs Sector", "Sector",\
  "Peak (GeV)", array("d",range(1,7)), array("d", [pro.GetParameter(1) for pro in \
  pros[-6:]]), None, array("d", [pro.GetParameter(2) for pro in pros[-6:]]))

# 1
c.Clear()
hists.append(ROOT.TH1F("h"+str(len(hists)),"Total Response of W (Gev)",bins,min_lim,max_lim))
for i in range(60):
  hists[-1].Add(hW[i])
c.cd()
draw(hists, fits, pros, bgs, ls, "total")
c.Print("hists/out1_total.pdf")
draw(hists, fits, pros, bgs, ls, "proton")
c.Print("hists/out1_proton.pdf")

#60 
c.Clear()
mg = ROOT.TMultiGraph()
g = []
for sec in range(6):
  x, x_err, y, y_err = array("d"), array("d"), array("d"), array("d")
  for i in range(10):
    fit = ROOT.TF1("fit"+str(sec+1)+"_"+str(i), fitf, 0.7, 1.1, 6)
    fit.SetParameters(100, 0.9, 0.1, 0, 0, 0) 
    fit.SetParLimits(1, 0.7, 1.1)
    #fit.SetParLimits(0, 0, 10e10)
    hW[sec*10+i].Fit(fit, "QR")
    if abs(fit.GetParError(1))<3:
      x.append(i+0.5)
      x_err.append(0)
      y.append(fit.GetParameter(1))
      y_err.append(fit.GetParError(1))
    else:
      print "Error with Q^2 "+str(i+0.5)+" , Sector "+str(sec+1)+" :"
      print "\ty  = "+str(fit.GetParameter(1))
      print "\tey = "+str(fit.GetParError(1))
  g.append(ROOT.TGraphErrors(len(x), x, y, x_err, y_err))
  g[-1].SetLineWidth(2)
  g[-1].SetLineColor(sec+1)
  g[-1].SetMarkerStyle(8)
  g[-1].SetMarkerSize(3)
  g[-1].SetTitle("Sector "+str(sec+1))
  mg.Add(g[-1])
mg.SetTitle("Proton Peak vs Q^{2} for each sector")
mg.GetYaxis().SetTitle("Proton Peak (GeV)")
mg.GetXaxis().SetTitle("Q^{2} (GeV^{2})")
mg.Draw("ALP")
c.BuildLegend()
c.Print("hists/graphs/out60.pdf")

