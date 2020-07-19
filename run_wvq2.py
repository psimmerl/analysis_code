import ROOT, sys, os

#os.system("run-groovy wvq2.groovy /cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v0/dst/train/skim4/skim4_005032.hipo")
#os.system("run-groovy wvq2.groovy /cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v0/dst/train/skim4/skim4_005038.hipo")

ff =  ROOT.TFile('q2w_hs.root')#sys.argv[1])

c1 = ROOT.TCanvas("c1","c1",2200,1600)
h1s = [ff.Get("hq2w_sec"+str(sec)+"_q2bin"+str(q2bin)) for sec in range(1,7) for q2bin in range(10)]
c1.Divide(5,2)
for sec in range(6):
   for i in range(10):
      c1.cd(i+1)
      h1s[sec*10+i].Draw("same")


c2 = ROOT.TCanvas("c2","c2",2200,1600)
h1s = [ff.Get("hq2w_q2bin"+str(q2bin)) for q2bin in range(10)]
c2.Divide(5,2)
for i in range(10):
  c2.cd(i+1)
  h1s[i].Draw()


c3 = ROOT.TCanvas("c3","c3",2200,1600)
h1s = [ff.Get("hq2w_sec"+str(sec)) for sec in range(1,7)]
c3.Divide(3,2)
for sec in range(6):
  c3.cd(sec+1)
  h1s[sec].Draw()


c4 = ROOT.TCanvas("c4","c4",2200,1600)
h1s = [ff.Get("hq2w_complete")]
c4.cd()
h1s[0].Draw()


c1.Print("out10h6s.pdf")
c2.Print("out10h.pdf")
c3.Print("out6s.pdf")
c4.Print("out1h.pdf")
