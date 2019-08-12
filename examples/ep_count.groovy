import org.jlab.io.hipo.HipoDataSource
import org.jlab.detector.base.DetectorType
import org.jlab.clas.physics.Particle
import org.jlab.clas.physics.Vector3
import org.jlab.groot.data.H2F
import org.jlab.groot.data.TDirectory
import exclusive.EP
import groovy.sql.Sql

def beam = new Particle(11, 0,0,10.6)//7.546)
def target = new Particle(2212, 0,0,0)

for(fname in args) {
def hemm2fi = [:].withDefault{new H2F("hemm2fi_$it", "MM2 vs phi", 250,140,190, 250,0,5)}

int run = fname.split("/")[-1].split('\\.')[0][-4..-1].toInteger()
int fnum = fname.split(".evio.")[-1].split('-')[0].toInteger()

def reader = new HipoDataSource()
reader.open(fname)

float fcmin = Float.MAX_VALUE, fcmax = 0
int counts = 0
while(reader.hasEvent()) {
  def event = reader.getNextEvent()
  if (event.hasBank("RUN::scaler")) {
    def scalerBank = event.getBank("RUN::scaler")
    def fc = scalerBank.getFloat('fcupgated', 0)
    if (fc<fcmin) fcmin = fc
    if (fc>fcmax) fcmax = fc
  }

  if (event.hasBank("REC::Particle") && event.hasBank("REC::Calorimeter")) {
    def (ele, pro) = EP.getEP(event)
    if(ele!=null) {
      def eX = new Particle(beam)
      eX.combine(target, 1)
      eX.combine(ele.particle, -1)

      //angle between electron and proton planes (should be close to 180)
      def zaxis = new Vector3(0,0,1)
      def enorm = ele.particle.vector().vect().cross(zaxis)
      def pnorm = pro.particle.vector().vect().cross(zaxis)
      def phi = enorm.theta(pnorm)
      hemm2fi['before'].fill(phi, eX.mass2())
      if(phi>176 && eX.mass2()<1.5) {
        counts++
        hemm2fi['after'].fill(phi, eX.mass2())
      }
    }
  }
}

reader.close()

def out = new TDirectory()
out.mkdir('/epcounts')
out.cd('/epcounts')
hemm2fi.values().each{out.addDataSet(it)}
out.writeFile('ep_count_hists_'+fname.split("/")[-1])

def sql = Sql.newInstance("jdbc:sqlite:/home/kenjo/elastic_mondb.db", "org.sqlite.JDBC")
//sql.execute("drop table if exists elastic")
//sql.execute("create table elastic (run integer, file integer, fcmin float, fcmax float, counts integer, primary key (run, file))")
sql.execute("insert or replace into elastic values ($run, $fnum, $fcmin, $fcmax, $counts)")
}
