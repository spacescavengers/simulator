'''
AWP | Astrodynamics with Python by Alfonso Gonzalez
https://github.com/alfonsogonzalez/AWP
https://www.youtube.com/c/AlfonsoGonzalezSpaceEngineering

Hello world of Spacecraft class
Two-body propagation with J2 perturbation for 100 periods
'''

# Python standard libraries
# AWP libraries
from Spacecraft import Spacecraft as SC
from planetary_data import earth
import csv as csv
import plotting_tools as pt
import numpy as np

if __name__ == '__main__':
	# orbits = []
	# with open("C:/_user/spacescAvengers/code/AWP/data/discos/active_object_orbits.csv", "r", encoding="utf-8") as active_orbits_csv:
	# 	orbits = list(csv.reader(active_orbits_csv, delimiter=","))[2:]

	# # sma, ecc, inc, raan, aPer, mAno 
	# #coes = [ earth[ 'radius' ] + 1000, 0.7, 30.0, 0.0, 0.0, 0.0 ]

	orbits = []
	with open("C:/_user/spacescAvengers/code/AWP/data/discos/aggregated_valid_orbits.csv", "r", encoding="utf-8") as active_orbits_csv:
		orbits = list(csv.reader(active_orbits_csv, delimiter=","))[2:]

	# sma, ecc, inc, raan, aPer, mAno, object_count
	#coes = [ earth[ 'radius' ] + 1000, 0.7, 30.0, 0.0, 0.0, 0.0 ]

	valid_orbits = np.array(orbits)[:, :6].astype(float)
	valid_orbits = valid_orbits[ np.logical_and(valid_orbits[:,0] > 8000, valid_orbits[:, 0] < 50000)]

	spacecrafts = []
	for orbit in valid_orbits:
		coes = orbit.tolist()
		spacecraft   = SC(
				{
				'coes'       : coes,
				'tspan'      : '1', 
				'dt'         : 100.0,
				'orbit_perts': { 'J2': True }
				} )
		spacecrafts.append(spacecraft)
	
	rs = [ sc.states[ :, :3 ] for sc in spacecrafts ]
	pt.plot_orbits( rs,
		{
		'traj_lws': 1,
		'show'    : True
		} )

	print("End!")