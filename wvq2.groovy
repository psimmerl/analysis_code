import org.jlab.io.hipo.HipoDataSource
import org.jlab.detector.base.DetectorType
import org.jlab.clas.physics.Particle
import org.jlab.clas.physics.LorentzVector
import org.jlab.clas.physics.Vector3
import org.jlab.groot.data.H1F
//import org.jlab.groot.data.TDirectory
//import javax.swing.JFrame
//import org.jlab.groot.graphics.EmbeddedCanvas
import org.jlab.jroot.ROOTFile
import utils.KinTool
import my.Sugar

Sugar.enable()

//TODO: IN ONE BIG HISTOGRAM WITH NO SECTOR MODE fix: hist for i j loop, hist x dim, canvas.divide(..), hW[floor(..)].fill(..)
//import pid.electron.Electron
println "starting"
//def frame = new JFrame("WvQ2 Groovy Analysis")
//def canvas = new EmbeddedCanvas()//("Canvas", "Canvas",1000,1000)
//frame.setSize(3840,2160)

def hW = []
for(int i = 1; i < 7; i++ ) {
   for(int j = 0; j < 10; j++) {
      hW.add(new H1F("hq2w_sec${i}_q2bin${j}","W (Q^2 bin of ${j} to ${j+1})",100,0,4.5))
   }
}

def beam    = LorentzVector.withPID(11,0,0,10.6)
def target  = LorentzVector.withPID(2212,0,0,0)

//canvas.divide(5, 2)
for(fname in args) {
   def skipped = 0
   def reader = new HipoDataSource()
   reader.open(fname)
   //def max = 0;
   while(reader.hasEvent()) {
      def event = reader.getNextEvent()
      if(event.hasBank("REC::Particle") && event.hasBank("REC::Calorimeter")) {
         def partb = event.getBank("REC::Particle")
         def calb  = event.getBank("REC::Calorimeter")
         def my_ele = (0..<partb.rows()
            ).findAll{partb.getInt('pid',it)==11 && partb.getShort('status',it)<0//TODO: Vaguely remember this means only trigger electron, if so I should remove
            }.each{iele->//findResults{iele->
               def ele = LorentzVector.withPID(11,*['px','py','pz'].collect{partb.getFloat(it,iele)})
               def eX  = beam+target-ele
               //def Q2  = (beam.p()-eX.p())**2
               def Q2 = KinTool.calcQ2(beam, ele)
               //if (eX.mass()>max) { max = eX.mass() }
               if (Q2<10){
                  def sector = calb.getByte('sector',iele)
                  hW[(sector-1)*10+Math.floor(Q2)].fill(eX.mass())//Not sure if this is what W & Q2 are
               } else {
                  //println Q2
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
   //println max
}


def ff = new ROOTFile('q2w_hs.root')
hW.each{ ff.addDataSet(it) }//Test with addDataSet and whole Array?
ff.close()
/*def out = new TDirectory()
canvas.setTitleSize(56)
canvas.setAxisTitleSize(48)
canvas.setAxisLabelSize(48)
canvas.setStatBoxFontSize(36)
hW.eachWithIndex{it,index->
   //canvas.cd(index)
   //canvas.draw(it)
   out.addDataset(it)
}
frame.add(canvas)
frame.setLocationRelativeTo(null)
frame.setVisible(true)
//out.add(canvas)
//out.addDataset(hW)
out.writeFile('wvq2.hipo')
//canvas.save("wvq2.png")*/
