import org.jlab.io.hipo.HipoDataSource
import org.jlab.detector.base.DetectorType
import org.jlab.clas.physics.Particle
import org.jlab.clas.physics.Vector3
import org.jlab.groot.data.H2F
import org.jlab.groot.data.TDirectory

def hemm2th = [:].withDefault{new H2F("hemm2th_$it", "MM2 vs theta", 250,5,30, 250,0,5)}
def hemm1fi = [:].withDefault{new H2F("hemm2fi_$it", "MM2 vs phi", 250,140,190, 250,0,5)}

def beam = new Particle(11, 0,0,10.6)//7.546)
def target = new Particle(2212, 0,0,0)


def electronPIDStrategies = [   
    { partb , iele -> partb.getInt('pid',iele) == 11 },
    { partb , iele -> partb.getInt('status',iele)<0 }

]

def electronPIDStrategies3 = [   
    { banks , iele -> partb.getInt('pid',iele) == 11 },
    { banks , iele -> partb.getInt('status',iele)<0 }

]

def electronPIDStrategies2 = [   
    { partb -> partb.getInt('pid').collect{ it==11 } },
    { partb -> partb.getInt('status').collect{ it<0 } }
]

//electron = new Electron();

//def myElectronCutStrategies = [
//    electron.isElectronEBPIDCut
//]

reqBanks = [ 
    part : "REC::Particle",
    ec   : "REC::Calorimeter",
    cc   : "REC::Cherenkov"
]


for(fname in args) {
    def reader = new HipoDataSource()
    reader.open(fname)
    
    def cc = 0
    
    while(reader.hasEvent() && cc < 20) {
	
	def event = reader.getNextEvent()

	def banks  = reqBanks.collect{name, bank -> [name, event.getBank(bank)] }.collectEntries()
	def banks_pres = reqBanks.every{name, bank -> event.hasBank(bank) }
	println(" are all banks present ")
	println(banks_pres)

	
	if (event.hasBank("REC::Particle") && event.hasBank("REC::Calorimeter") && event.hasBank("REC::Cherenkov") ) {
	    cc+=1
	    // -method 1 we can directly loop over the banks here the same old way
	    // -method 2 loop over objects in banks 
	    def partb = event.getBank("REC::Particle")
	    def calb = event.getBank("REC::Calorimeter")
	    def chb = event.getBank("REC::Cherenkov")

	    //get rows in bank pass to findAll, a closure, iterate over rec bank status and print it 
	    println( ' get stat ' )
	    def my_el_stat = (0..<partb.rows()).findAll{println(partb.getShort('status',it)) }
	    println( ' print findall ' )
	    println(my_el_stat)

 	    //findAll returns list of indices satisfying the closure
	    //send to findResults
	    //use each whn iterating over list
	    //reserve findAll and findResults  find all elements matching critieria
	    def my_el_pid  =  (0..<partb.rows()).each{partb.getInt('pid',it) == 11 && partb.getInt('status',it)<0}.each{ ii -> println( ['px','py','pz'].collect{partb.getFloat(it,ii) } ) }
	    println( my_el_pid )

	    println(" trying closure " )
	    //def test_el = (0..<partb.rows()).findAll{ electronPIDStrategies.each{ el_test -> el_test(partb,it) }.findResults{ii -> println(ii) }  
	    //loop over rec particle bank -> use findAll to return list of indices to loop over with 'it' -> pass the rec.particle index to method electronPIDStrategies -> find all instances with true and return the index
	    //def test_el = (0..<partb.rows()).findAll{ electronPIDStrategies.findResults{ el_test -> el_test(partb,it) }.findAll{println(it) } }//Result{ii= -> if(ii== true) }  }
	    def test_el2 = (0..<partb.rows()).findAll{ println(electronPIDStrategies.findResults{ el_test -> el_test(partb,it) }) }//findResult{ii= -> if(ii== true) }  }
	    println(test_el2)

	    //important note: when making dict do not put ':', or it will literally take the object as the key
	    def test_el_map = (0..<partb.rows()).collect{ ii -> [ii , electronPIDStrategies.collect{ el_test -> el_test(partb,ii) } ] }.collectEntries()
	    println(test_el_map)
	    println(test_el_map.getClass())
	    
	    
	    def test_el_final = (0..<partb.rows()).findIndexValues{ electronPIDStrategies.every{ el_test -> el_test(partb,it) }  }
	    
	    //def test_el_final = (0..<partb.rows()).findIndexValues{ electronPIDStrategies.every{ el_test -> el_test(partb,it) }  }
	    println(' test final list of indices ')
	    println( test_el_final)
	    

	    // 3rd method - no loop	  
	    def test_no_loop = electronPIDStrategies2.collect{ el_strat2 -> el_strat2(partb) }.transpose()
	    
	    
	    //test how to get the sector from cal bank for correct particle
	    partb.show()
	    calb.show()
	    def sect  = (0..<partb.rows()).each{ ii -> (calb.getShort('pindex')*.toInteger()).findResults{ println(it) == ii  } }//calb.getShort('pindex',ii) ) 


	    // now lets try to get the nphe for events 
	    //map nphe[pindex] = nphe
	    def nphe = [chb.getShort('pindex'), chb.getFloat('nphe')].transpose().collectEntries{pind,nph-> [(pind.toInteger()):nph] }
	    println( ' nphe ')
	    println( nphe )

	    //can we get it without invoking map
	    //put the index that you want the number of photoelect for.
	    //def phe = (0..<banks.cc.rows()).find{ pindex -> banks.cc.getFloat("nphe", pindex) > 2 && banks.cc.getInt("pindex", pindex) == index }
	    //	    def nphe = (0..<partb.rows()).find{cher.getByte('detector',it)==7}
	    //		.collectEntries{(cherb.guODetShort('pindex',it)):cherb.getFloat('energy',it) }
	    //	    nphe[0]>5
	    
	    
	    //def nphe  = (0..<partb.rows()).findResult{ chb.getInt('nphe') 
	    
	    //println(' sector ' )
	    //println( sect  )
	    //println( calb.getShort('pindex')*.toInteger().getClass() )
	    
	    //nice way to check range conditions
	    //banks.part.getFloat('vz',0).with{println(it)}// < max_vz && it > min_vz}
	    println((0..<banks.part.rows()).findAll{ banks.part.getFloat('vz',0).with{it < 10 && it > -10} })
	    
	    println(' testing no loop method ')
	    println(test_no_loop)
	    	    
	    //println( ' test object type ' )
	    //println( my_el_pid.getClass() )






	}
    }
    reader.close();
}
