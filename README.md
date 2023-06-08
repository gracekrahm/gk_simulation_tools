# gk_simulation_tools

Workflow and Descriptions:
- filter_galaxies_simba.py
  - identifies galaxies in a simba snapshot and places each of the galaxies in their own hdf5 file
- galaxy_positions.py
  - identifies each galaxy's center pixel and writes the info in a single npz file
- powderday_setup.py and cosmology_setup_all_cluster.hipergator.sh
  - creates model *.py files for powderday
  - creates *.job file to run powderday on all galaxies
- prospector_setup.py and prosp_fits_setup.sh
  - creates *.job file to run prospector on all of the powderday seds
