import h5py
import numpy as np
import sys, os
import numpy as np
import glob
import tqdm
import yt

##############
# Line arguments
###############
#snap = int(sys.argv[1])
#snap_dir = sys.argv[2]
#outfile = snap_dir+'/snap'+str(snap)+'_positions_best.npz'
#snap = int(sys.argv[1])
snap = 64
snap_dir = './' #where are the filtered galaxies?
outfile = './galaxy_positions_best.npz' #where do you want the output to go?
snaplabel = '64'
################

pos = {}
ngalaxies = {}


unit_base = {
    "UnitLength_in_cm": 3.08568e21,
    "UnitMass_in_g": 1.989e43,
    "UnitVelocity_in_cm_per_s": 100000,
}

bbox_lim = 1e5  # kpc

bbox = [[-bbox_lim, bbox_lim], [-bbox_lim, bbox_lim], [-bbox_lim, bbox_lim]]


infiles = sorted(glob.glob(snap_dir+'/galaxy_*.hdf5'))
count = 0
for i in tqdm.tqdm(range(len(infiles))):
#for i in tqdm.tqdm(range(1)):

    print('count', count)
    count += 1
    pos['galaxy'+str(i)] = {}
    fname = snap_dir+'/galaxy_'+str(i)+'.hdf5'
    try:
        ds = yt.load(fname, unit_base=unit_base, bounding_box=bbox)
        ds.index
        ad = ds.all_data()
    # total_mass returns a list, representing the total gas and dark matter + stellar mass, respectively
        print([tm.in_units("Msun") for tm in ad.quantities.total_mass()])
        density = ad["PartType0", "density"]
        wdens = np.where(density == np.max(density))
    except:
        continue
    coordinates = ad["PartType0", "Coordinates"]
    center = coordinates[wdens][0]
    print("center = ", center)
    x_pos, y_pos, z_pos = center
    pos['galaxy'+str(i)]['snap'+str(snap)] = np.array([x_pos, y_pos, z_pos])
    print('center', center)
    print('pos', pos['galaxy'+str(i)]['snap'+str(snap)])
    #gas_mass = np.sum(gas_masses)
    #print(gas_mass, 'gas mass')
    #star_mass = np.sum(star_masses)
    #infile.close()
ngalaxies['snap'+str(snap)] = count
np.savez(outfile, ngalaxies=ngalaxies, pos=pos)

