System.setProperty("java.awt.headless", "true")
import org.jlab.io.hipo.HipoDataSource
import org.jlab.clas.physics.LorentzVector
import org.jlab.groot.data.H1F
import org.jlab.jroot.ROOTFile
import utils.KinTool
import my.Sugar

Sugar.enable()

def hW = []
for(int i = 1; i < 7; i++ ) {
  for(int j = 0; j < 10; j++) {
    hW.add(new H1F("hq2w_sec${i}_q2bin${j}","W (Q^{2} ${j}-${j+1} GeV^{2})",500,0,4.5))
  }
}
for(int i = 0; i < 10; i++) {
  hW.add(new H1F("hq2w_q2bin${i}","W (Q^{2} ${i}-${i+1} GeV^{2})",500,0,4.5))
}
for(int i = 1; i < 7; i++ ) { 
  hW.add(new H1F("hq2w_sec${i}","Sector ${i} W (Q^{2} 1-10 GeV^{2})",500,0,4.5)) 
}
for(int i = 1; i < 7; i++ ) { 
  for(int j = 0; j < 10; j++) {
    hW.add(new H1F("hq2w_sec${i}_q2bin${j}_proton","W (Q^{2} ${j}-${j+1} GeV^{2})",500,0.7,1.1))
  }
}
for(int i = 0; i < 10; i++) {
  hW.add(new H1F("hq2w_q2bin${i}_proton","W (Q^{2} ${i}-${i+1} GeV^{2})",500,0.7,1.1))
}
for(int i = 1; i < 7; i++ ) { 
  hW.add(new H1F("hq2w_sec${i}_proton","Sector ${i} W (Q^{2} 1-10 GeV^{2})",500,0.7,1.1)) 
}

hW.add(new H1F("hq2w_complete","W (Q^{2} 1-10 GeV^{2})",500,0,4.5))
hW.add(new H1F("hq2w_proton", "W (Q^{2} 1-10 GeV^{2})", 500, 0.7, 1.1))

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
          if (Q2<10){
            def sector = calb.getByte('sector',iele)
            def eX  = beam+target-ele
            
            hW[(sector-1)*10+Math.floor(Q2)].fill(eX.mass())
            hW[Math.floor(Q2)+60].fill(eX.mass())
            hW[(sector-1)+70].fill(eX.mass())

            hW[(sector-1)*10+Math.floor(Q2)+76].fill(eX.mass())
            hW[Math.floor(Q2)+60+76].fill(eX.mass())
            hW[(sector-1)+70+76].fill(eX.mass())
            
            hW[-2].fill(eX.mass())
            hW[-1].fill(eX.mass())
          } else {
            //println Q2
            skipped++
          }
        }
      }  
   }
   reader.close()
   println "Skipped ${skipped} events from ${fname}"
}

def ff = new ROOTFile('q2w_hs.root')
hW.each{ ff.addDataSet(it) }//Test with addDataSet and whole Array?
ff.close()
