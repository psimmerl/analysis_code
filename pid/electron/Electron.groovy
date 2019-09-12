package pid.electron

class Electron {
    
    def ebPID = 11
    def neg_charge = -1
    def nphe = 2
    
    //vertex wide enough for all sectors
    def vz_min = -12;
    def vz_max = 9;
    
    def pcal_dep_max = 0.06;

    //calorimeter fiducial cut
    def min_u = 0;
    def max_u = 420;
    def min_v = 0;
    def max_v = 420;
    def min_w = 0;
    def max_w = 420;

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

    def passElectronEBPIDCut(bank, iele){
	return bank.getInt('pid',iele) == ebPID
    }

    def passElectronNpheCut(bank, iele){
	return bank.getInt('pid',iele) == ebPID
    }

    def passElectronVertexCut(bank, iele){
	return bank.getInt('vz',iele) == ebPID
    }

    def passElectronPCALFiducialCut(bank, iele){		
	return bank.getInt('uv',iele) >= min_u
    }

    def passElectronEIEOCut(bank, iele){
	return bank.getShort('pindex')
    }

    

}
