import ROOT, sys, os

os.system("run-groovy wvq2.groovy skim4_005032.hipo")

ff =  ROOT.TFile('q2w_hs.root')#sys.argv[1])
h1s = [ff.Get("hq2w_sec"+str(isec)+"_q2bin"+str(bins)) for isec in range(1,2) for bins in range(10)]

c1 = ROOT.TCanvas("c1","c1",1100,800)
c1.Divide(5,2)
for i in range(10):
   c1.cd(i+1)
   h1s[i].Draw()
c1.Print("out.pdf")
