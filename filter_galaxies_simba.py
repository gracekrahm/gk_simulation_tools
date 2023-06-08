import h5py
import caesar
import sys
import glob
import numpy as np
import tqdm
import os

###########
# Line arguments
###########
snapshot_path = '/orange/narayanan/desika.narayanan/gizmo_runs/simba/m25n512/output/snapshot_'
snap_num = 59
#output_path = '/orange/narayanan/desika.narayanan/gizmo_runs/simba/m25n512/filtered_snaps/snap'+str(snap_num).zfill(3)
output_path = '/blue/narayanan/gkrahm/gizmo_runs/simba/m25n512/filtered_snaps/snap'+str(snap_num).zfill(3)
#output_path = '/blue/narayanan/gkrahm/gizmo_runs/simba/m25n512/filtered_snaps/snap'+str(snap_num).zfill(3)
caesar_file = '/orange/narayanan/desika.narayanan/gizmo_runs/simba/m25n512/output/Groups/caesar_0059_z7.490.hdf5'

#see if the output path exists, and if not, make it

if not os.path.exists(output_path):
      os.makedirs(output_path)
      print("creating output directory: "+output_path)


obj = caesar.load(caesar_file)
snap_str = str(snap_num).zfill(3)

input_file = h5py.File(snapshot_path+str(snap_str)+'.hdf5', 'r')


galcount = len(obj.galaxies)
for galaxy in range(galcount):
      print()
      print("GALAXY NUM:",str(galaxy))
      print()
      glist = obj.galaxies[int(galaxy)].glist
      slist = obj.galaxies[int(galaxy)].slist


      with h5py.File(output_path+'galaxy_'+str(galaxy)+'.hdf5', 'w') as output_file:
          output_file.copy(input_file['Header'], 'Header')
          print('starting with gas attributes now')
          output_file.create_group('PartType0')
          for k in tqdm.tqdm(input_file['PartType0']):
              output_file['PartType0'][k] = input_file['PartType0'][k][:][glist]
          print('moving to star attributes now')
          output_file.create_group('PartType4')
          for k in tqdm.tqdm(input_file['PartType4']):
              output_file['PartType4'][k] = input_file['PartType4'][k][:][slist]


      print('done copying attributes, going to edit header now')
      outfile_reload = output_path+'galaxy_'+str(galaxy)+'.hdf5'

      re_out = h5py.File(outfile_reload,'r+')
      re_out['Header'].attrs.modify('NumPart_ThisFile', np.array([len(glist), 0, 0, 0, len(slist), 0]))
      re_out['Header'].attrs.modify('NumPart_Total', np.array([len(glist), 0, 0, 0, len(slist), 0]))

      re_out.close()
