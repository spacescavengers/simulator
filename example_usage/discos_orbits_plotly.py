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
import plotly.graph_objects as go


def create_earth_trace():

    # Set up 100 points. First, do angles
    theta = np.linspace(0, 2*np.pi, 100)
    phi = np.linspace(0, np.pi, 100)

    # Set up coordinates for points on the sphere
    x0 = earth['radius'] * np.outer(np.cos(theta), np.sin(phi))
    y0 = earth['radius'] * np.outer(np.sin(theta), np.sin(phi))
    z0 = earth['radius'] * np.outer(np.ones(100), np.cos(phi))

    # Set up trace
    # trace= go.Surface(x=x0, y=y0, z=z0, colorscale=[[0,'#325bff'], [1,'#151A7B']])
    trace = go.Surface(x=x0, y=y0, z=z0, colorscale='blues')
    trace.update(showscale=False)
    return trace


def extract_orbit_trace(sc: SC):
    x_coord = sc.states[:, 0]
    y_coord = sc.states[:, 1]
    z_coord = sc.states[:, 2]

    trace = go.Scatter3d(x=x_coord, y=y_coord, z=z_coord, marker=dict(
        size=0.1), line=dict(color='#ffff00', width=2))
    return trace


if __name__ == '__main__':
    # orbits = []
    # with open("C:/_user/spacescAvengers/code/AWP/data/discos/active_object_orbits.csv", "r", encoding="utf-8") as active_orbits_csv:
    #     orbits = list(csv.reader(active_orbits_csv, delimiter=","))[2:]

    # # sma, ecc, inc, raan, aPer, mAno
    # # coes = [ earth[ 'radius' ] + 1000, 0.7, 30.0, 0.0, 0.0, 0.0 ]

    orbits = []
    with open("C:/_user/spacescAvengers/code/AWP/data/discos/aggregated_valid_orbits.csv", "r", encoding="utf-8") as active_orbits_csv:
        orbits = list(csv.reader(active_orbits_csv, delimiter=","))[2:]

	# sma, ecc, inc, raan, aPer, mAno, object_count
	#coes = [ earth[ 'radius' ] + 1000, 0.7, 30.0, 0.0, 0.0, 0.0 ]

    valid_orbits = np.array(orbits)[:, :7].astype(float)
    valid_orbits = valid_orbits[valid_orbits[:, 6] > 5]
    valid_orbits = valid_orbits[:, :6]
    valid_orbits = valid_orbits[ np.logical_and(valid_orbits[:,0] > 8000, valid_orbits[:, 0] < 60000)]

    traces = []
    traces.append(create_earth_trace())

    for orbit in valid_orbits: #[:200]:
        coes = orbit.tolist()
        spacecraft = SC(
            {
                'coes': coes,
                'tspan': '1',
                'dt': 100.0,
                'orbit_perts': {'J2': True}
            })

        traces.append(extract_orbit_trace(spacecraft))

    layout = go.Layout(title='Discos Object Orbits', showlegend=False, margin=dict(l=0, r=0, t=0, b=0),
                       # paper_bgcolor = 'black',
                       scene=dict(xaxis=dict(title='X axis',
                                             titlefont_color='black',
                                             backgroundcolor='black',
                                             color='black',
                                             gridcolor='white'),
                                  yaxis=dict(title='Y axis',
                                             titlefont_color='black',
                                             backgroundcolor='black',
                                             color='black',
                                             gridcolor='white'
                                             ),
                                  zaxis=dict(title='Z axis',
                                             backgroundcolor='black',
                                             color='white',
                                             gridcolor='white'
                                             )
                                  ))

    fig = go.Figure(data=traces, layout=layout)

    fig.show()
    fig.write_html("discos_orbits.html")

    print("End!")
