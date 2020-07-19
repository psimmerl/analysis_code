import org.jlab.io.hipo.HipoDataSource
import org.jlab.detector.base.DetectorType
import org.jlab.clas.physics.Particle
import org.jlab.clas.physics.LorentzVector
import org.jlab.clas.physics.Vector3
import org.jlab.groot.data.H1F
import org.jlab.jroot.ROOTFile
import utils.KinTool
import my.Sugar

Sugar.enable()

println "starting"

def hW = []
for(int i = 1; i < 7; i++ ) {
  for(int j = 0; j < 10; j++) {
    hW.add(new H1F("hq2w_sec${i}_q2bin${j}","W (Q^2 ${j}-${j+1})",100,0,4.5))
  }
}
for(int i = 1; i < 7; i++ ) { 
  hW.add(new H1F("hq2w_sec${i}","Sector ${i} W (Q^2 1-10})",100,0,4.5)) 
}
hW.add(new H1F("hq2w_complete","W (Q^2 1-10)",100,0,4.5))


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
          def eX  = beam+target-ele
          //def Q2  = (beam.p()-eX.p())**2
          def Q2 = KinTool.calcQ2(beam, ele)
          if (Q2<10){
            def sector = calb.getByte('sector',iele)
            //hW[(sector-1)*10+Math.floor(Q2)].fill(eX.mass())//Not sure if this is what W & Q2 are
            h.fill(eX.mass())
          } else {
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
