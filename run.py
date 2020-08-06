import ROOT, math
from array import array

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetEndErrorSize(10)

ff =  ROOT.TFile('q2w_hs.root')#sys.argv[1])

def fitf( x, par):
  return par[0]*math.exp(-0.5*((x[0]-par[1])/par[2])**2)+par[3]+par[4]*x[0]+par[5]*(x[0]**2)
def background(x, par):
  return par[0]+par[1]*x[0]+par[2]*(x[0]**2)#+par[3]*(x[0]**3)
def gaussian(x, par):
  return par[0]*math.exp(-0.5*((x[0]-par[1])/par[2])**2)
def BinFloor(x, bin_conv):
  return int(math.floor(x*bin_conv))
hW = [ff.Get("hq2w_sec"+str(i+1)+"_q2bin"+str(j)) for i in range(6) for j in range(10)]

def draw(hists, fits, pros, bgs, ls, dist):
  line_width = 2
  axis = hists[-1].GetXaxis()
  min_b, max_b = axis.GetXmin(), axis.GetXmax()
  bc = axis.GetNbins()/(max_b-min_b)
  axis.SetRange(BinFloor(0.7,bc),BinFloor(1.1,bc))
  if dist is "proton":
    #hists[-1].GetXaxis().SetRangeUser(0.7, 1.1)
    line_width = 4
  else:#Run fit only once per dataset
    hnum = len(hists)
    fits.append(ROOT.TF1("fit"+str(hnum), fitf, 0.7, 1.1, 6))

    pros.append(ROOT.TF1("pFit"+str(hnum), gaussian, 0.7, 1.1, 3))
    pros[-1].SetLineColor(ROOT.kMagenta)
    bgs.append(ROOT.TF1("bgFit"+str(hnum), background, 0.7, 1.1, 3))
    bgs[-1].SetLineColor(ROOT.kGreen)

    #if hnum > 16:
    #ls.append(ROOT.TLegend(.1,.6,.4,.9))
    #else:
    ls.append(ROOT.TLegend(.1,.6,.5,.9))
    ls[-1].SetTextFont(72)
    ls[-1].SetTextSize(0.04)

    hists[-1].GetXaxis().SetTitle("W (GeV)")
    hists[-1].SetStats(0)

    lin = (hists[-1].GetBinContent(BinFloor(1.1,bc))-hists[-1].GetBinContent(BinFloor(.7,bc)))/(1.1-0.7)
    cons = hists[-1].GetBinContent(BinFloor(0.7,bc))-(lin*0.7)
    mu = hists[-1].GetMaximumBin()
    s = hists[-1].GetBinContent(mu)
    mu = mu/bc
    val = hists[-1].GetBinContent(BinFloor(mu-0.2,bc)) - lin*(mu/-0.2)-cons
    if val > 0 and s>0:
      sig = math.sqrt(abs(-1/2*(mu-0.5)*1/math.log(val/s)))
    else:
      sig = 0.055
    print "s="+str(s)+", mu="+str(mu)+", sig="+str(sig)+", cons="+str(cons)+", lin="+str(lin)
    
    axis.SetRange(BinFloor(min_b,bc), BinFloor(max_b,bc))
    fits[-1].SetParameters(s, mu, sig, cons, lin, 0, 0) 
    #fits[-1].SetParameters(100,.9,.1,0,0,0)
    #fits[-1].SetParLimits(0, 0, 10e6)
    fits[-1].SetParLimits(1, 0.7, 1.1)
    #fits[-1].SetParLimits(2, 0.0001, 10e6)
    hists[-1].Fit(fits[-1], "R")

    #fits.append(best_fit)
    pars = fits[-1].GetParameters()
    errs = fits[-1].GetParErrors()
    pros[-1].SetParameters(pars[0],pars[1],pars[2])
    bgs[-1].SetParameters(pars[3],pars[4],pars[5], pars[6])

    ls[-1].AddEntry(hists[-1],"Data",           "l")
    ls[-1].AddEntry(fits[-1], "Global Fit",     "l")
    ls[-1].AddEntry(bgs[-1],  "Background Fit", "l")
    ls[-1].AddEntry(pros[-1], "Proton Fit",     "l") 
    ls[-1].AddEntry(None,     "\mu {:.5f}".format(pars[1]), "")
    ls[-1].AddEntry(None,     " \pm{:.5f} GeV".format(errs[1]), "")
    ls[-1].AddEntry(None,     "\sigma {:.5f}".format(pars[2]), "")
    ls[-1].AddEntry(None,     " \pm{:.5f} GeV".format(errs[2]), "")
  
  fits[-1].SetLineWidth(line_width)
  pros[-1].SetLineWidth(line_width)
  bgs[-1].SetLineWidth(line_width)
  hists[-1].SetLineWidth(line_width-1)
  hists[-1].SetMinimum(0)
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

entries = array("d")
for i in range(10):
  axis = hists[-10+i].GetXaxis()
  bc = axis.GetNbins()/(axis.GetXmax()-axis.GetXmin())
  mu, sig = fits[-10+i].GetParameter(1), fits[-10+i].GetParameter(2)
  lowb, highb = BinFloor(mu-2*sig,bc), BinFloor(mu+2*sig, bc) 
  entries.append((hists[-10+i].Integral(lowb,highb)-bgs[-10+i].Integral(lowb,highb))*bc)
draw_graph("hists/graphs/out10_Nentries_Q2.pdf","Entries in Proton vs Q^{2}", "Q^{2} (GeV^{2})", \
  "N Entries", array("d",[x+0.5 for x in range(10)]), entries)

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
  draw([hists[-6+sec]], [fits[-6+sec]], [pros[-6+sec]], [bgs[-6+sec]], [ls[-6+sec]], "proton")
c.Print("hists/out6_proton.pdf")

entries = array("d")
for sec in range(6):
  axis = hists[-6+sec].GetXaxis()
  bc = axis.GetNbins()/(axis.GetXmax()-axis.GetXmin())
  mu, sig = fits[-6+sec].GetParameter(1), fits[-6+sec].GetParameter(2)
  lowb, highb = BinFloor(mu-2*sig,bc), BinFloor(mu+2*sig, bc)
  entries.append((hists[-6+sec].Integral(lowb,highb)-bgs[-6+sec].Integral(lowb,highb))*bc)
draw_graph("hists/graphs/out6_Nentries_sec.pdf","Entries in Proton vs Sector", "Sector", \
  "N Entries", array("d",range(1,7)), entries)

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
mg, mg_entries = ROOT.TMultiGraph(), ROOT.TMultiGraph()
g = []
for sec in range(6):
  x, x_err, y, y_err = array("d"), array("d"), array("d"), array("d")
  y_entries = array("d")
  for i in range(10):
    hists.append(hW[sec*10+i])
    axis = hists[-1].GetXaxis()
    bc = axis.GetNbins()/(axis.GetXmax()-axis.GetXmin())
    draw(hists, fits, pros, bgs, ls, "total")
    
    mu, sig = fits[-1].GetParameter(1), fits[-1].GetParameter(2)
    
    y_entries.append((hists[-1].Integral(BinFloor((mu-sig*2),bc), BinFloor((mu+sig*2),bc)) - \
      bgs[-1].Integral(BinFloor((mu-sig*2),bc), BinFloor((mu+sig*2),bc)))*bc)
    if abs(fits[-1].GetParError(1))<3:
      x.append(i+0.5)
      x_err.append(0)
      y.append(fits[-1].GetParameter(1))
      y_err.append(fits[-1].GetParError(1))
    else:
      print "Error with Q^2 "+str(i+0.5)+" , Sector "+str(sec+1)+" :"
      print "\ty  = "+str(fits[-1].GetParameter(1))
      print "\tey = "+str(fits[-1].GetParError(1))

  g.append(ROOT.TGraphErrors(len(x), x, y, x_err, y_err))
  g[-1].SetLineWidth(2)
  g[-1].SetLineColor(sec+1)
  g[-1].SetMarkerStyle(8)
  g[-1].SetMarkerSize(3)
  g[-1].SetTitle("Sector "+str(sec+1))
  mg.Add(g[-1])
  
  g.append(ROOT.TGraphErrors(10, array("d", [x+0.5 for x in range(10)]), y_entries, array("d",[0]*10), array("d",[0]*10)))
  g[-1].SetLineWidth(2)
  g[-1].SetLineColor(sec+1)
  g[-1].SetMarkerStyle(8)
  g[-1].SetMarkerSize(3)
  g[-1].SetTitle("Sector "+str(sec+1))
  mg_entries.Add(g[-1])

c.Divide(10,6)
for sec in range(6):
  for i in range(10):
    c.cd(sec*10+i+1)
    draw([hists[-60+sec*10+i]], [fits[-60+sec*10+i]], [pros[-60+sec*10+i]], [bgs[-60+sec*10+i]], [ls[-60+sec*10+i]], "proton")
c.Print("hists/out60.pdf")

c.Clear()
mg.SetTitle("Proton Peak vs Q^{2} for each sector")
mg.GetYaxis().SetTitle("Proton Peak (GeV)")
mg.GetXaxis().SetTitle("Q^{2} (GeV^{2})")
mg.Draw("ALP")
c.BuildLegend()
c.Print("hists/graphs/out60_peaks.pdf")

mg_entries.SetTitle("Entries vs Q^{2} for each sector")
mg_entries.GetYaxis().SetTitle("Entries")
mg_entries.GetXaxis().SetTitle("Q^{2} (GeV^{2})")
mg_entries.Draw("ALP")
c.BuildLegend(0.75, 0.6, .9,.9)
c.Print("hists/graphs/out60_entries.pdf")

# 6 2D
hQ2W2D = [ff.Get("H2F_sec"+str(sec)+"_q2w") for sec in range(1,7)]
for zoom in ["total", "proton"]:
  for sec in range(6):
    c.Clear()
    if zoom == "proton":
      hQ2W2D[sec].GetXaxis().SetRangeUser(0.7, 1.1)
    hQ2W2D[sec].GetXaxis().SetTitle("W (GeV)")
    hQ2W2D[sec].GetYaxis().SetTitle("Q^{2} (GeV^{2})")
    #h2D[-1].SetStats(0)
    hQ2W2D[sec].Draw("COLZ")
    c.Print("hists/new/out2D_Q2W_"+zoom+"_sec"+str(sec+1)+".pdf")

c.Clear()
hTotal2D = hQ2W2D[0]
hTotal2D.SetTitle("Q^{2} vs W")
for sec in range(1,6):
  hTotal2D.Add(hQ2W2D[sec])
hTotal2D.Draw("COLZ")
hTotal2D.GetXaxis().SetTitle("W (GeV)")
hTotal2D.GetYaxis().SetTitle("Q^{2} (GeV^{2})")
c.Print("hists/new/out2D_Q2W_total.pdf")

c.Clear()
hTotal2D.GetXaxis().SetRangeUser(0.7, 1.1)
hTotal2D.GetXaxis().SetTitle("W (GeV)")
hTotal2D.GetYaxis().SetTitle("Q^{2} (GeV^{2})")
hTotal2D.Draw("COLZ")
c.Print("hists/new/out2D_Q2W_proton.pdf")


# Theta vs P
hThetaP2D = [ff.Get("H2F_sec"+str(sec)+"_ThetaP") for sec in range(1,7)]
c.Clear()
c.Divide(3,2)
for sec in range(6):
  c.cd(sec+1)
  hThetaP2D[sec].GetXaxis().SetTitle("#theta")
  hThetaP2D[sec].GetYaxis().SetTitle("P (GeV)")
  #h2D[-1].SetStats(0)
  hThetaP2D[sec].Draw("COLZ")

c.Print("hists/new/out2D_ThetaP_6.pdf")

c.Clear()
hTotal2D = hThetaP2D[0]
hTotal2D.SetTitle("#theta vs P")
for sec in range(1,6):
  hTotal2D.Add(hThetaP2D[sec])
hTotal2D.Draw("COLZ")
c.Print("hists/new/out2D_ThetaP_total.pdf")


#Theta vs Phi
hThetaPhi = ff.Get("H2F_ThetaPhi")
c.Clear()
hThetaPhi.GetXaxis().SetTitle("#theta")
hThetaPhi.GetYaxis().SetTitle("#phi")
hThetaPhi.Draw("COLZ")
c.Print("hists/new/out_ThetaPhi.pdf")

