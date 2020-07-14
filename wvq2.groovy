import org.jlab.io.hipo.HipoDataSource
import org.jlab.detector.base.DetectorType
import org.jlab.clas.physics.Particle
import org.jlab.clas.physics.LorentzVector
import org.jlab.clas.physics.Vector3
import org.jlab.groot.data.H2F
import org.jlab.groot.data.TDirectory
import javax.swing.JFrame
import org.jlab.groot.graphics.EmbeddedCanvas
import utils.KinTool
import my.Sugar

Sugar.enable()


//import pid.electron.Electron
println "starting"
def frame = new JFrame("WvQ2 Groovy Analysis")
def canvas = new EmbeddedCanvas()//("Canvas", "Canvas",1000,1000)
frame.setSize(1000,1000)
println "made canvas"

def hW = []
for(int i = 0; i < 1 /*6*/; i++ ) {
   for(int j = 0; j < 10; j+=1) {
      hW.add(new H2F("h-${i}-${j}",
         "WvQ^{2} Sector ${i};Q^{2} (GeV);W (GeV/c^{2}?)",10,j,j+1,10,0,10))
   }
}

println "made hists"
def beam    = LorentzVector.withPID(11,0,0,10.6)
def target  = LorentzVector.withPID(2212,0,0,0)

canvas.divide(5, 2)
println "divided"
for(fname in args) {
   def skipped = 0
   def reader = new HipoDataSource()
   reader.open(fname)
   println "open"
   while(reader.hasEvent()) {
      def event = reader.getNextEvent()
      if(event.hasBank("REC::Particle") && event.hasBank("REC::Calorimeter")) {
         def partb = event.getBank("REC::Particle")
         //def calb  = event.getBank("REC::Calorimeter")
         def my_ele = (0..<partb.rows()
            ).findAll{partb.getInt('pid',it)==11 && partb.getShort('status',it)<0//TODO: Vaguely remember this means only trigger electron, if so I should remove
            }.each{iele->//findResults{iele->
               def ele = LorentzVector.withPID(11,*['px','py','pz'].collect{partb.getFloat(it,iele)})
               def eX  = beam+target-ele
               //def Q2  = (beam.p()-eX.p())**2
               def Q2 = KinTool.calcQ2(beam, ele)
               //println Q2
               if (Q2<10){ 
                  hW[Math.floor(Q2)].fill(Q2,eX.mass())//Not sure if this is what W & Q2 are
               } else {
                  println Q2
                  skipped++
               }
               //hW[Math.floor(Q2)].fill(Q2,eX.mass())//Not sure if this is what W & Q2 are
               //TODO: Need to figure out how to split based on azimuthal sector
               
              // return ele.e()>1.5 ? ele : null
            }
         //print my_ele
         //hW.fill(my_ele.mass())

      }  
   }
   reader.close()
   println "Skipped ${skipped} events from ${fname}"
}


def out = new TDirectory()
hW.eachWithIndex{it,index->
   canvas.cd(index)
   //it.getXaxis().SetTitle("Q^{2} (GeV)"
   canvas.draw(it)
   out.addDataset(it)
   println "draw"
}
frame.add(canvas)
frame.setLocationRelativeTo(null)
frame.setVisible(true)
//out.add(canvas)
//out.addDataset(hW)
out.writeFile('wvq2.hipo')

