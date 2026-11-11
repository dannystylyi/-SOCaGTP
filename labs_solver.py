import orbital_math as orb

a = orb.orbital_elements(printable=True)
orb.spacecraft_position_velocity(dict_orbital_elements=a, printable=True)
orb.construct_motion_trajectory(a)
