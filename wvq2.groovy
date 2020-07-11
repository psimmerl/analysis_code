import org.jlab.io.hipo.HipoDataSource
import org.jlab.detector.base.DetectorType
import org.jlab.clas.physics.Particle
import org.jlab.clas.physics.LorentzVector
import org.jlab.clas.physics.Vector3
import org.jlab.groot.data.H1F
import org.jlab.groot.data.TDirectory

//import pid.electron.Electron

def hW = new H1F("W","W",100,1,4)

def beam    = LorentzVector.withPID(11,0,0,10.6)
def target  = LorentzVector.withPID(2212,0,0,0)


for(fname in args) {
   def reader = new HipoDataSource()
   reader.open(fname)
   
   while(reader.hasEvent()) {
      def event = reader.getNextEvent()
      if(event.hasBank("REC::Particle") && event.hasBank("REC::Calorimeter")) {
         def partb = event.getBank("REC::Particle")
         //def calb  = event.getBank("REC::Calorimeter")
         def my_ele = (0..<partb.rows()
            ).findAll{partb.getInt('pid',it)==11 && partb.getShort('status',it)<0
            }.findResults{iele->
               //def ele = 
               return LorentzVector.withPID(11,*['px','py','pz'].collect{partb.getFloat(it,iele)})
               //return ele.e()>1.5 ? ele : null
            }
         //print my_ele
         //hW.fill(my_ele.mass())

      }  
   }
   reader.close()
}

def out = new TDirectory()
out.addDataset(hW)
out.writeFile('wvq2.hipo')



