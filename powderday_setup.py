#purpose: to set up slurm files and model *.py files from the
#positions written by caesar_cosmology_npzgen.py for a cosmological
#simulation.  This is written for the University of Florida's
#HiPerGator2 cluster.

import numpy as np
from subprocess import call
import sys
import pandas as pd

nnodes=1


#################
# Edit these !!!
snap_redshift = float(6.951)
snap_num = 64
npzfile = '/orange/narayanan/gkrahm/caesar_snaps/sidney_filtered_snaps/snap064/galaxy_positions_best.npz'
hydro_dir = '/orange/narayanan/gkrahm/caesar_snaps/sidney_filtered_snaps/snap064/'
model_dir_base = '/orange/narayanan/gkrahm/caesar_snaps/sidney_filtered_snaps/pd_runs/snap064/myfilter/neb/'



hydro_dir_remote = hydro_dir
model_run_name=model_run_name='pd' # shorthand for what you are running
#################



COSMOFLAG=0 #flag for setting if the gadget snapshots are broken up into multiples or not and follow a nomenclature snapshot_000.0.hdf5
FILTERFLAG = 1 #flag for setting if the gadget snapshots are filtered or not, and follow a nomenclature snap305_galaxy1800_filtered.hdf5


SPHGR_COORDINATE_REWRITE = True


#===============================================

if (COSMOFLAG == 1) and (FILTERFLAG == 1):
    raise ValueError("COSMOFLAG AND FILTER FLAG CAN'T BOTH BE SET")


data = np.load(npzfile,allow_pickle=True)
pos = data['pos'][()] #positions dictionary
#ngalaxies is the dict that says how many galaxies each snapshot has, in case it's less than NGALAXIES_MAX
ngalaxies = data['ngalaxies'][()]
print(ngalaxies)





for snap in [snap_num]:

    model_dir = model_dir_base+'params/'
    model_dir_remote = model_dir_base+'seds/'

    tcmb = 2.73*(1.+snap_redshift)
    try:
        NGALAXIES = ngalaxies['snap'+str(snap)]
    except:
        NGALAXIES = ngalaxies['snap0'+str(snap)]
    print('ngalaxies', NGALAXIES)
    ngal = NGALAXIES
    for nh in range(NGALAXIES):
        print(nh)
        try:
            try:
                center = pos['galaxy'+str(nh)]['snap'+str(snap)]#[0]
            except:
                center = pos['galaxy'+str(nh)]['snap0'+str(snap)]#[0]
            xpos = center[0]
            ypos = center[1]
            zpos = center[2]
            print('center', center)
            print('calling')
            cmd = "./cosmology_setup_all_cluster.hipergator.sh "+str(nnodes)+' '+model_dir+' '+hydro_dir+' '+model_run_name+' '+str(COSMOFLAG)+' '+str(FILTERFLAG)+' '+model_dir_remote+' '+hydro_dir_remote+' '+str(xpos)+' '+str(ypos)+' '+str(zpos)+' '+str(nh)+' '+str(snap)+' '+str(tcmb)+' '+str(ngal-1)
            call(cmd,shell=True)
            print('called')
        except:
            continue
