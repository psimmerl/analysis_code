package pid.electron
import org.jlab.detector.base.DetectorType

class Electron {
    
    def ebPID = 11
    def neg_charge = 0
    def min_nphe = 2
    
    //vertex wide enough for all sectors
    def min_vz = -12
    def max_vz = 9
    
    def max_pcal_dep = 0.06

    //calorimeter fiducial cut
    def min_u = 0
    def max_u = 420
    def min_v = 0
    def max_v = 420
    def min_w = 0
    def max_w = 420

    //dcr1,2,3 fiducial cut
    //require functional form
    def heightR1 = 29
    def radiusR1 = 29

    def heightR2 = 35
    def radiusR2 = 40

    def heightR3 = 48
    def radiusR3 = 49



    //sampling fraction cut
    //require functional form
    
    //in future require that electron class takes constructor arguments to set the cut values
    
    static def findElectron = { event ->
	def pbank = event.getBank("REC::Particle")
	return (0..<pbank.rows())
	    .find{pbank.getInt('pid',it)==11 && pbank.getShort('status',it)<0}
    }

    def passElectronEBPIDCut(bank, index){
	return (bank.part.getInt('pid',index) == ebPID)
    }

    def passElectronChargeCut(bank, index){
	return (bank.part.getInt('charge',index) < neg_charge)
    }

    def passElectronNpheCut(bank, index){
	return (0..<bank.cc.rows()).any{bank.cc.getInt('pindex',it) == index &&
					bank.cc.getFloat('nphe',it) > min_nphe}
    }

    def passElectronVertexCut(bank, index){
	return (bank.part.getFloat('vz',index).with{it < max_vz && it > min_vz})
    }

    def passElectronPCALFiducialCut(bank, index){		
	// can probably be changed to a find like closure to avoid looping over all indices
	return (0..<bank.ec.rows()).any{bank.ec.getByte('detector',it) == DetectorType.ECAL.getDetectorId() &&
					bank.ec.getInt('pindex',it) == index &&
					bank.ec.getFloat('lu',it).with{it < max_u && it > min_u} &&
					bank.ec.getFloat('lv',it).with{it < max_v && it > min_v} &&
					bank.ec.getFloat('lw',it).with{it < max_w && it > min_w} 
	}	
    }

    def passElectronEIEOCut(bank, index){
	return (0..<bank.ec.rows()).any{(bank.ec.getByte('detector',it) == DetectorType.HTCC.getDetectorId() &&
					 bank.ec.getFloat('energy',it) > min_pcal_dep &&
					 bank.ec.getInt('pindex',it) == index)
	}
    }

    //detector layer r1-12, r2-24, r3-36
    def passElectronDCR1(bank, index){
	def hit_pos = (0..<bank.traj.rows()).find{(bank.traj.getInt('pindex',it) == index && 
						    bank.traj.getByte('detector',it) == DetectorType.DC.getDetectorId() &&
						    bank.traj.getByte('layer',it) == 12 )}.collect{ ['x','y','z'].collect{ii-> bank.traj.getFloat(ii,it) } }
	if( (hit_pos.size() == 0) ){
	    return false
	    //hit_pos = hit_pos.get(0)
	}
	hit_pos=hit_pos.get(0)
	println(" getting hit position elements in electorn class ")
	println(hit_pos)

	//get the sector for the track as defined in the REC::Track bank
	def sec = (0..<bank.trck.rows()).find{ bank.trck.getInt('pindex',it) == index && 
					      bank.trck.getByte('detector',it) == DetectorType.DC.getDetectorId() }.collect{bank.trck.getByte('sector',it)}.get(0)

	//x - 0
	//y - 1 
	//z - 2
	println( 'sector in electron class ')
	println(sec)
	def ang = sec*60.0*Math.PI/180.0
	def x1_rot = hit_pos.get(1) * Math.sin(ang) + hit_pos.get(0) * Math.cos(ang)
	def y1_rot = hit_pos.get(1) * Math.cos(ang) - hit_pos.get(0) * Math.sin(ang)

	println(" x1 rot $x1_rot  and y1rot $y1_rot")

	
	def slope = 1/Math.tan(0.5*60.0*Math.PI/180.0)
	def left  = (heightR1 - slope * y1_rot)
	def right = (heightR1 + slope * y1_rot)
	
	println("left $left and right $right ")
	def radius2_DCr1 = radiusR1**2 - y1_rot**2;    // cut out the inner circle
	println(" radius2 $radius2_DCr1" )
	if (x1_rot > left && x1_rot > right ) {return true }// && x1_rot**2 > radius2_DCr1){ return true }
	else{ return false }
		
    }

    def passElectronDCR2(bank, index){
	//this returns list of list 
	def hit_pos = (0..<bank.traj.rows()).find{(bank.traj.getInt('pindex',it) == index && 
						    bank.traj.getByte('detector',it) == DetectorType.DC.getDetectorId() &&
						    bank.traj.getByte('layer',it) == 24 )}.collect{ ['x','y','z'].collect{ii-> bank.traj.getFloat(ii,it) }}.get(0)

	//get the sector for the track as defined in the REC::Track bank
	def sec = (0..<bank.trck.rows()).find{ bank.trck.getInt('pindex',it) == index && 
					      bank.trck.getByte('detector',it) == DetectorType.DC.getDetectorId() }.collect{bank.trck.getByte('sector',it)}.get(0)

	//x - 0
	//y - 1 
	//z - 2
	def ang = sec*60.0*Math.PI/180.0
	def x1_rot = hit_pos.get(1) * Math.sin(ang) + hit_pos.get(0) * Math.cos(ang);
	def y1_rot = hit_pos.get(0) * Math.cos(ang) - hit_pos.get(0) * Math.sin(ang);
	
	def slope = 1/Math.tan(0.5*ang);
	def left  = (heightR2 - slope * y1_rot);
	def right = (heightR2 + slope * y1_rot);
	
	def radius2_DCr2 = radiusR2**2 - y1_rot**2;    // cut out the inner circle
	if (x1_rot > left && x1_rot > right && x1_rot**2 > radius2_DCr2) return true;
		
    }

    def passElectronDCR3(bank, index){
	def hit_pos = (0..<bank.traj.rows()).find{(bank.traj.getInt('pindex',it) == index && 
						    bank.traj.getByte('detector',it) == DetectorType.DC.getDetectorId() &&
						    bank.traj.getByte('layer',it) == 36 )}.collect{ ['x','y','z'].collect{ii-> bank.traj.getFloat(ii,it) }}.get(0)

	//get the sector for the track as defined in the REC::Track bank
	def sec = (0..<bank.trck.rows()).find{ bank.trck.getInt('pindex',it) == index && 
					      bank.trck.getByte('detector',it) == DetectorType.DC.getDetectorId() }.collect{bank.trck.getByte('sector',it)}.get(0)

	//x - 0
	//y - 1 
	//z - 2
	def ang = sec*60.0*Math.PI/180.0
	def x1_rot = hit_pos.get(1) * Math.sin(ang) + hit_pos.get(0) * Math.cos(ang);
	def y1_rot = hit_pos.get(1) * Math.cos(ang) - hit_pos.get(0) * Math.sin(ang);
	
	def slope = 1/Math.tan(0.5*ang);
	def left  = (heightR3 - slope * y1_rot);
	def right = (heightR3 + slope * y1_rot);
	
	def radius2_DCr3 = radiusR3**2 - y1_rot**2;    // cut out the inner circle
	if (x1_rot > left && x1_rot > right && x1_rot**2 > radius2_DCr3) return true;
		
    }



    //still need
    // SF cut
    // DC R1 R2 R3 cut
    // Require EC , HTCC, DC have sector > 0
    

    // using the static def approach in the main code we do not need to instantiate the electron class -> use Electron.isElectronEBPIDCut
    //    static def isElectronEBPIDCut(bank, iele){/
    //	return partb.getInt('pid',iele) == 11 	
    //   }

}
