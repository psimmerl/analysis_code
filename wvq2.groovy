import org.jlab.io.hipo.HipoDataSource
import org.jlab.detector.base.DetectorType
import org.jlab.clas.physics.Particle
import org.jlab.clas.physics.LorentzVector
import org.jlab.clas.physics.Vector3
import org.jlab.groot.data.H2F
import org.jlab.groot.data.TDirectory

//import pid.electron.Electron

def hW = [new H2F("h0","WvQ2,(0,1]",10,0,1,10,0,10),new H2F("h1","WvQ2,(1,2]",10,1,2,10,0,10),
          new H2F("h2","WvQ2,(2,3]",10,2,3,10,0,10),new H2F("h3","WvQ2,(3,4]",10,3,4,10,0,10),
          new H2F("h4","WvQ2,(4,5]",10,4,5,10,0,10),new H2F("h5","WvQ2,(5,6]",10,5,6,10,0,10),
          new H2F("h6","WvQ2,(6,7]",10,6,7,10,0,10),new H2F("h7","WvQ2,(7,8]",10,7,8,10,0,10),
          new H2F("h8","WvQ2,(8,9]",10,8,9,10,0,10),new H2F("h9","WvQ2,(9,10]",10,9,10,10,0,10)]

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
               def ele = LorentzVector.withPID(11,*['px','py','pz'].collect{partb.getFloat(it,iele)})
               def eX  = beam+target-ele
               def Q2  = (beam.p()-eX.p())**2
               
               hW[floor(Q2)].fill(Q2,eX.mass())
               
               return ele.e()>1.5 ? ele : null
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



