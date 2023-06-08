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
snap_redshift = float(7.490)
snap_num = 59
npzfile = '/blue/narayanan/gkrahm/gizmo_runs/snap059/filtered_snaps/galaxy_positions.npz'
model_dir_base = '/blue/narayanan/gkrahm/gizmo_runs/snap059/pd_runs/' # where do you want your POWDERDAY parameters model files to go?
hydro_dir =  '/blue/narayanan/gkrahm/gizmo_runs/snap059/filtered_snaps/' # where are your filtered galaxies?
hydro_dir_remote = hydro_dir
model_run_name=model_run_name='simba_m25n512' # shorthand for what you are running
ngal_max = 10 #max galaxy number to make files for if different than ngalaxies
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

    NGALAXIES = ngalaxies['snap'+str(snap)]
    print('ngalaxies', NGALAXIES)
    #for nh in range(NGALAXIES):
    ngal_max = 10
    for nh in range(ngal_max):
        xpos = pos['galaxy'+str(nh)]['snap'+str(snap)][0]
        ypos = pos['galaxy'+str(nh)]['snap'+str(snap)][1]
        zpos = pos['galaxy'+str(nh)]['snap'+str(snap)][2]
        print('calling')
        cmd = "./cosmology_setup_all_cluster.hipergator.sh "+str(nnodes)+' '+model_dir+' '+hydro_dir+' '+model_run_name+' '+str(COSMOFLAG)+' '+str(FILTERFLAG)+' '+model_dir_remote+' '+hydro_dir_remote+' '+str(xpos)+' '+str(ypos)+' '+str(zpos)+' '+str(nh)+' '+str(snap)+' '+str(tcmb)+' '+str(ngal_max)
        call(cmd,shell=True)
        print('called')
