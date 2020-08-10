import ROOT, math
from array import array

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetEndErrorSize(10)

ff =  ROOT.TFile('hists.root')#sys.argv[1])

def BinFloor(x, bin_conv):
  return int(math.floor(x*bin_conv))

c = ROOT.TCanvas("c","c",2200,1600)
c.SetGrid()

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

# Phi vs P
hPhiP2D = [ff.Get("H2F_sec"+str(sec)+"_PhiP") for sec in range(1,7)]
c.Clear()
c.Divide(3,2)
for sec in range(6):
  c.cd(sec+1)
  hPhiP2D[sec].GetXaxis().SetTitle("#phi")
  hPhiP2D[sec].GetYaxis().SetTitle("P (GeV)")
  #h2D[-1].SetStats(0)
  hPhiP2D[sec].Draw("COLZ")

c.Print("hists/new/out2D_PhiP_6.pdf")

c.Clear()
hTotal2D = hPhiP2D[0]
hTotal2D.SetTitle("#phi vs P")
for sec in range(1,6):
  hTotal2D.Add(hPhiP2D[sec])
hTotal2D.Draw("COLZ")
c.Print("hists/new/out2D_PhiP_total.pdf")


#Theta vs Phi
hThetaPhi = ff.Get("H2F_ThetaPhi")
c.Clear()
hThetaPhi.GetXaxis().SetTitle("#theta")
hThetaPhi.GetYaxis().SetTitle("#phi")
hThetaPhi.Draw("COLZ")
c.Print("hists/new/out_ThetaPhi.pdf")

