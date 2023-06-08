import numpy as np
from subprocess import call
import sys
import pandas as pd

nnodes=1


#################
# Edit these !!!
snap_redshift = float(7.490)
snap_num = 59
#npzfile = '/blue/narayanan/gkrahm/gizmo_runs/snap059/filtered_snaps/galaxy_positions.npz'
npzfile = '/blue/narayanan/gkrahm/gizmo_runs/snap059/filtered_snaps/galaxy_positions_new.npz'
model_dir_base = '/blue/narayanan/gkrahm/gizmo_runs/snap059/pd_runs/' # where do you want your POWDERDAY parameters model files to go?
model_run_name=model_run_name='simba_m25n512' # shorthand for what you are running
ngal_max = 10 #max galaxy number to make files for if different than ngalaxies
sed_fits_dir = '/blue/narayanan/gkrahm/gizmo_runs/snap059/sed_fits' #where do you want your PROSPECTOR SED fit files to go?
#################





SPHGR_COORDINATE_REWRITE = True


#===============================================

data = np.load(npzfile,allow_pickle=True)
#ngalaxies is the dict that says how many galaxies each snapshot has, in case it's less than NGALAXIES_MAX
ngalaxies = data['ngalaxies'][()]





for snap in [snap_num]:

    model_dir = model_dir_base+'params/'
    model_dir_remote = model_dir_base+'seds/'

    tcmb = 2.73*(1.+snap_redshift)

    NGALAXIES = ngalaxies['snap'+str(snap)]
    print('ngalaxies', NGALAXIES)
    #for nh in range(NGALAXIES):
    ngal = ngal_max
    for nh in range(ngal):
        print('calling')
        cmd = "./prosp_fits_setup.sh "+str(nnodes)+' '+model_dir+' '+model_dir_remote+' '+str(nh)+' '+str(snap)+' '+str(snap_redshift)+' '+str(tcmb)+' '+str(ngal-1)+' '+sed_fits_dir
        call(cmd,shell=True)
        print('called')
