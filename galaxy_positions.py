import h5py
import numpy as np
import sys, os
import numpy as np
import glob
import tqdm

##############
# Line arguments
###############
#snap = int(sys.argv[1])
#snap_dir = sys.argv[2]
#outfile = snap_dir+'/snap'+str(snap)+'_positions.npz'
#snap = int(sys.argv[1])
snap = 59
snap_dir = './' #where are the filtered galaxies?
outfile = './galaxy_positions.npz' #where do you want the output to go?
snaplabel = '059'
################

pos = {}
ngalaxies = {}

infiles = sorted(glob.glob(snap_dir+'/snap059galaxy_*.hdf5'))
count = 0
for i in tqdm.tqdm(range(len(infiles))):
    print('count', count)
#snap059galaxy_10.hdf5
    #infile = h5py.File(snap_dir+'/snap'+snaplabel+galaxy_'+str(i)+'.hdf5', 'r')
    infilename = snap_dir+'snap059galaxy_'+str(i)+'.hdf5'
    #print(infilename)
    infile = h5py.File(infilename, 'r')
    #try:
        #infile = h5py.File(snap_dir+'/galaxy_'+str(i)+'.hdf5', 'r')
    #except:
        #continue
    count += 1
    pos['galaxy'+str(i)] = {}


    gas_masses = infile['PartType0']['Masses']
    gas_coords = infile['PartType0']['Coordinates']
    star_masses = infile['PartType4']['Masses']
    star_coords = infile['PartType4']['Coordinates']
    total_mass = np.sum(gas_masses) + np.sum(star_masses)

    x_pos = (np.sum(gas_masses * gas_coords[:,0]) + np.sum(star_masses * star_coords[:,0])) / total_mass
    y_pos = (np.sum(gas_masses * gas_coords[:,1]) + np.sum(star_masses * star_coords[:,1])) / total_mass
    z_pos = (np.sum(gas_masses * gas_coords[:,2]) + np.sum(star_masses * star_coords[:,2])) / total_mass
    print('xpos',x_pos)

    pos['galaxy'+str(i)]['snap'+str(snap)] = np.array([x_pos, y_pos, z_pos])
    #print('pos', pos)
    infile.close()
ngalaxies['snap'+str(snap)] = count


np.savez(outfile, ngalaxies=ngalaxies, pos=pos)
