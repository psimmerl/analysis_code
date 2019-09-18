package event
import org.jlab.detector.base.DetectorType
import event.DCHit

class Event {

    // Scalars
    Short npart, helicity
    Long event_number
    Float start_time, rf_time

    // All detector status variables collected together
    HashSet<Integer> cherenkov_status, ecal_inner_status, ecal_outer_status, pcal_status
    HashSet<Integer> dc1_status, dc2_status, dc3_status, tof_status

    // REC::Cherenkov
    HashMap<Integer,Float> nphe, cherenkov_time, cherenkov_path
    HashMap<Integer,Short> cherenkov_sector

    // REC::Particle
    HashMap<Integer, Short> pid, status, charge
    HashMap<Integer, Float> px, py, pz, p, vx, vy, vz, vt, beta

    // REC::Calorimeter
    HashMap<Integer, Short> ecal_inner_sector, ecal_outer_sector, pcal_sector
    HashMap<Integer, Float> ecal_inner_energy, ecal_outer_energy, pcal_energy
    HashMap<Integer, Float> ecal_inner_time, ecal_outer_time, pcal_time
    HashMap<Integer, Float> ecal_inner_path, ecal_outer_path, pcal_path

    // REC::Scintillator
    HashMap<Integer, Short> tof_sector, tof_paddle
    HashMap<Integer, Float> tof_time, tof_path, tof_energy

    // REC::Track and REC::Traj
    HashMap<Integer, ArrayList<DCHit>> dc1, dc2, dc3
    HashMap<Integer, Float> dc_chi2
    HashMap<Integer, Short> dc_sector, dc_ndf

    def Event(){

        cherenkov_status = new HashSet<Integer>()
        ecal_inner_status = new HashSet<Integer>()
        ecal_outer_status = new HashSet<Integer>()
        pcal_status = new HashSet<Integer>()
        dc1_status = new HashSet<Integer>()
        dc2_status = new HashSet<Integer>()
        dc3_status = new HashSet<Integer>()
        tof_status = new HashSet<Integer>()

        // REC::Particle
        px = new HashMap<Integer, Float>()
        py = new HashMap<Integer, Float>()
        pz = new HashMap<Integer, Float>()
        p = new HashMap<Integer, Float>()
        vx = new HashMap<Integer, Float>()
        vy = new HashMap<Integer, Float>()
        vz = new HashMap<Integer, Float>()
        vt = new HashMap<Integer, Float>()
        beta = new HashMap<Integer, Float>()
        pid = new HashMap<Integer, Integer>()
        charge = new HashMap<Integer, Short>()
        status = new HashMap<Integer, Short>()

        // REC::Cherenkov
        nphe = new HashMap<Integer, Float>()
        cherenkov_time = new HashMap<Integer, Float>()
        cherenkov_path = new HashMap<Integer, Float>()
        cherenkov_sector = new HashMap<Integer, Short>()

        // REC::Calorimeter
        ecal_inner_sector = new HashMap<Integer, Short>()
        ecal_inner_energy = new HashMap<Integer, Float>()
        ecal_inner_time = new HashMap<Integer, Float>()
        ecal_inner_path = new HashMap<Integer, Float>()
        ecal_outer_sector = new HashMap<Integer, Short>()
        ecal_outer_energy = new HashMap<Integer, Float>()
        ecal_outer_time = new HashMap<Integer, Float>()
        ecal_outer_path = new HashMap<Integer, Float>()
        pcal_sector = new HashMap<Integer, Short>()
        pcal_energy = new HashMap<Integer, Float>()
        pcal_time = new HashMap<Integer, Float>()
        pcal_path = new HashMap<Integer, Float>()

        // REC::Scintillator
        tof_time = new HashMap<Integer, Float>()
        tof_path = new HashMap<Integer, Float>()
        tof_energy = new HashMap<Integer, Float>()
        tof_paddle = new HashMap<Integer, Short>()
        tof_sector = new HashMap<Integer, Short>()

        // REC::Traj and REC::Track
        dc1 = new HashMap<Integer, ArrayList<DCHit>>()
        dc2 = new HashMap<Integer, ArrayList<DCHit>>()
        dc3 = new HashMap<Integer, ArrayList<DCHit>>()
        dc_sector = new HashMap<Integer, Short>()
        dc_ndf = new HashMap<Integer, Short>()
        dc_chi2 = new HashMap<Integer, Float>()
    }
}

