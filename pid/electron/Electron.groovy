package pid.electron
import org.jlab.detector.base;

class Electron {
    
    def ebPID = 11
    def neg_charge = -1
    def nphe = 2
    
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

    //sampling fraction cut
    //require functional form
    
    //in future require that electron class takes constructor arguments to set the cut values
    
    static def findElectron = { event ->
	def pbank = event.getBank("REC::Particle")
	return (0..<pbank.rows())
	    .find{pbank.getInt('pid',it)==11 && pbank.getShort('status',it)<0}
    }

// using the static def approach in the main code we do not need to instantiate the electron class -> use Electron.isElectronEBPIDCut
//    static def isElectronEBPIDCut(bank, iele){/
//	return partb.getInt('pid',iele) == 11 	
//   }

    def passElectronEBPIDCut(banks, index){
	return (0..<bank.part.rows()).any{banks.part.getInt('pid',index) == ebPID}
    }

    def passElectronNpheCut(bank, index){
	return (0..<bank.cc.rows()).any{bank.cc.getInt('pindex',it) == index 
					&& bank.cc.getFloat('nphe',it) > min_nphe}
    }

    def passElectronVertexCut(bank, index){
	//return (0..<bank.part.rows()).any{ bank.part.getFloat('vz',it) < max_vz && bank.part.getFloat('vz',it) > min_vz }
	return (0..<bank.part.rows()).any{ bank.part.getFloat('vz',index).with{it < max_vz && it > min_vz} }
    }

    def passElectronPCALFiducialCut(bank, index){		
	return (0..<bank.ec.rows()).any{bank.ec.getFloat('detector',it) == DetectorType.PCAL.getDetectorId()
					&& bank.ec.getInt('pindex',it) == index 
					
					&& bank.ec.getFloat('lu',it).with{it < max_u && it > min_u } 
					&& bank.ec.getFloat('lv',it).with{it < max_v && it > min_v }
					&& bank.ec.getFloat('lw',it).with{it < max_w && it > min_w }
	}	
    }

    def passElectronEIEOCut(bank, index){
	return (0..<bank.ec.rows()).any{ (bank.ec.getFloat('detector',it) == DetectorType.HTCC.getDetectorId()
					 && bank.ec.getFloat('energy',it) > min_pcal_dep
					 && bank.ec.getFloat('pindex',it) == index )
	}
    }


//still need
    // SF cut
    // DC R1 R2 R3 cut
    // Require EC , HTCC, DC have sector > 0
    

}
