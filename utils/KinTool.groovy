package utils
import org.jlab.clas.physics.LorentzVector
import org.jlab.clas.pdg.PDGDatabase


class KinTool{

    //move somplace else

    static def Q2(){
	return 0
    }

    static def delta_meas_energy( Double beam,  LorentzVector measured_el ){
	def calc_e = beam/(1+ (beam/PDGDatabase.getParticleMass(2212))*(1-Math.cos(measured_el.theta())) );
	return (calc_e  - measured_el.e() )
    }

    static def delta_meas_theta( Double beam,  LorentzVector measured_el ){
	def calc_theta = Math.toDegrees(Math.acos( 1 + (PDGDatabase.getParticleMass(2212)/beam)*( 1 - beam/measured_el.e()) ))
	return Math.toDegrees((calc_theta  - measured_el.theta() ))
    }

    

}


