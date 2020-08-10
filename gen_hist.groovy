System.setProperty("java.awt.headless", "true")
import org.jlab.io.hipo.HipoDataSource
import org.jlab.clas.physics.LorentzVector
import org.jlab.groot.data.H1F
import org.jlab.groot.data.H2F
import org.jlab.jroot.ROOTFile
import utils.KinTool
import my.Sugar
Sugar.enable()

def hW = []
for(int i = 1; i < 7; i++ ) {
  for(int j = 0; j < 10; j++) {
    hW.add(new H1F("hq2w_sec${i}_q2bin${j}","W (Q^{2} ${j}-${j+1} GeV^{2})",1000,0,4.5))
  }
}

def hThetaP = []
def hPhiP = []
def hW2D = []
for(int i = 1; i < 7; i++) {
  hW2D.add(new H2F("H2F_sec${i}_q2w", "Q^{2} vs W (sector ${i})", 1000, 0, 4.5, 1000, 0, 10))
  hThetaP.add(new H2F("H2F_sec${i}_ThetaP", "#theta vs Momentum (sector ${i})", 1000, 0, 35, 1000, 0, 10))
  //hPhiP.add(new H2F("H2F_sec${i}_PhiP", "#Phi vs Momentum (sector ${i})", 1000, -180, 180, 1000, 0, 10))
  hPhiP.add(new H2F("H2F_sec${i}_PhiP", "#Phi vs Momentum (sector ${i}, centered at ${(i-1)*60-(i>4 ? 1 : 0)*360})", 1000, -30, 30, 1000, 0, 10))
  
}
hThetaPhi = new H2F("H2F_ThetaPhi", "#theta vs #phi", 1000, 0, 35, 1000, -180, 180)

def beam    = LorentzVector.withPID(11,0,0,10.6)
def target  = LorentzVector.withPID(2212,0,0,0)

for(fname in args) {
  def skipped = 0
  def reader = new HipoDataSource()
  reader.open(fname)
  while(reader.hasEvent()) {
    def event = reader.getNextEvent()
    if(event.hasBank("REC::Particle") && event.hasBank("REC::Calorimeter")) {
      def partb = event.getBank("REC::Particle")
      def calb  = event.getBank("REC::Calorimeter")
      (0..<partb.rows()).findAll{partb.getInt('pid',it)==11 && partb.getShort('status',it)<0
        }.each{iele->
          def ele = LorentzVector.withPID(11,*['px','py','pz'].collect{partb.getFloat(it,iele)})
          def Q2 = KinTool.calcQ2(beam, ele) //def Q2  = (beam.p()-eX.p())**2
          def sector = calb.getByte('sector',iele)
          def path = calb.getFloat('path',iele)
          def x = calb.getFloat('x', iele)
          def y = calb.getFloat('y', iele)
          def theta = Math.asin(Math.sqrt(x**2+y**2)/path)*180/Math.PI
          def phi = Math.atan2(y,x)*180/Math.PI/1
          def eX  = beam+target-ele
          /*println "mome=${ele.p()}"
          println "x   =${x}"
          println "y   =${y}"
          println "path=${path}"
          println "thet=${theta}"
          println "phi =${phi}"*/
          hThetaP[sector-1].fill(theta, ele.p())
          hPhiP[sector-1].fill(phi-((sector-1)*60-(sector>4 ? 1 : 0)*360)+(sector==4 ? 1 : 0)*360*(phi<0 ? 1 : 0), ele.p())
          hThetaPhi.fill(theta, phi)
          if (Q2<10){
            hW[(sector-1)*10+Math.floor(Q2)].fill(eX.mass())
            hW2D[sector-1].fill(eX.mass(), Q2)
          } else {
            skipped++
          }
        }
      }  
   }
   reader.close()
   println "Skipped ${skipped} events from ${fname}"
}

def ff = new ROOTFile('hists.root')
hW.each{ 
  def NBinsX = it.getXaxis().getNBins()
  for(X = 0; X < NBinsX; X++) {
    it.setBinError(X, Math.sqrt(it.getBinContent(X)))
  }
  ff.addDataSet(it) 
}//Test with addDataSet and whole Array?
hW2D.each{ 
/*  def NBinsX = it.getXAxis().getNBins()
  def NBinsY = it.getYAxis().getNBins()
  for(X = 0; X < NBinsX; X++) {
    for(Y = 0; Y < NBinsY; Y++) {
      it.setBinError(X, Y, Math.sqrt(it.getBinContent(X, Y)))
    } 
  }
*/
  ff.addDataSet(it) 
}
hThetaP.each{ 
/*  def NBinsX = it.getXAxis().getNBins()
  def NBinsY = it.getYAxis().getNBins()
  for(X = 0; X < NBinsX; X++) {
    for(Y = 0; Y < NBinsY; Y++) {
      it.setBinError(X, Y, Math.sqrt(it.getBinContent(X, Y)))
    }
  }
*/  ff.addDataSet(it) 
}
hPhiP.each { ff.addDataSet(it) }
/*def NBinsX = hThetaPhi.getXAxis().getNBins()
def NBinsY = hThetaPhi.getYAxis().getNBins()
 for(X = 0; X < NBinsX; X++) {
  for(Y = 0; Y < NBinsY; Y++) {
    hThetaPhi.setBinError(X, Y, Math.sqrt(hThetaPhi.getBinContent(X, Y)))
  }
}*/
ff.addDataSet(hThetaPhi)
ff.close()
