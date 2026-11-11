import numpy
import datetime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# x, y, z # Coordinates of the center of mass # km
# Vx, Vy, Vz # Velocity (km/s)
# t0 # Start time
mu = 398600 # Gravitational parameter of Earth (km^3/s^2)
omega_earth = 7.2921159e-5 # Angular velocity of Earth (rad/s)
R_earth = 6371 # Radius of Earth (km)

def orbital_elements(x=5700, y=8500, z=-9000, Vx=-4, Vy=0, Vz=-3, t0="22.08.2025", printable=False): 
    date_str = str(t0) + " 12:00:00" 
    t0 = datetime.datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")

    r = numpy.array([x, y, z]) # Position vector (km)
    V = numpy.array([Vx, Vy, Vz]) # Velocity vector (km/s)

    # Specific angular momentum vector (SAMV)
    sigma = numpy.cross(r, V) # (km^2/s)

    # Semi-latus rectum
    p = numpy.linalg.norm(sigma)**2 / mu # (km)

    # Specific orbital energy
    h = numpy.linalg.norm(V)**2 - 2 * mu / numpy.linalg.norm(r) # (km^2/s^2)

    # Eccentricity
    e = numpy.sqrt(1 + h * numpy.linalg.norm(sigma)**2 / mu**2) # Dimensionless

    #  SAMV components
    sigma_x, sigma_y, sigma_z = sigma
    sx = sigma_x / numpy.linalg.norm(sigma)
    sy = sigma_y / numpy.linalg.norm(sigma) 
    sz = sigma_z / numpy.linalg.norm(sigma)

    # Inclination 
    i = numpy.arccos(sz) # (rad)
    i_deg = numpy.degrees(i) # (deg)

    # Right ascension of the ascending node (RAAN)
    sin_Omega = sx / numpy.sin(i)
    if (sin_Omega > 0):
        Omega = numpy.arccos(-sy / numpy.sin(i)) # (rad)
        
    else:
        Omega = 2 * numpy.pi - numpy.arccos(-sy / numpy.sin(i)) # (rad)
    Omega_deg = numpy.degrees(Omega) # (deg)

    # Argument of perigee
    f = -numpy.cross(sigma, V) - mu * r / numpy.linalg.norm(r) # Eccentricity vector (km/s^2)  
    e_n = numpy.array([numpy.cos(Omega), numpy.sin(Omega), 0]) # Node vector (dimensionless)
    cos_omega = numpy.dot(f, e_n) / numpy.linalg.norm(f)
    fx = f[0] / numpy.linalg.norm(f)
    fy = f[1] / numpy.linalg.norm(f)
    fz = f[2] / numpy.linalg.norm(f)
    if (fz >= 0):    
        omega = numpy.arccos(cos_omega) # (rad)
    else:
        omega = 2 * numpy.pi - numpy.arccos(cos_omega) # (rad)
    omega_deg = numpy.degrees(omega) # (deg)

    # True anomaly
    # r = p / (1 + e * numpy.cos(v)) # (km) 
    cos_v = (p / numpy.linalg.norm(r) - 1) / e
    if (numpy.dot(r, V) >= 0):
        v = numpy.arccos(cos_v) # (rad)
    else:
        v = 2 * numpy.pi - numpy.arccos(cos_v) # (rad)
    v_deg = numpy.degrees(v) # (deg)

    # The argument of latitude
    u = omega + v # (rad)
    u_deg = numpy.degrees(u) # (deg)

    if (h < 0):
        # Semi-major axis
        a = -mu / h # (km)

        # Eccentric anomaly
        E = 2 * numpy.arctan(numpy.sqrt((1 - e) / (1 + e)) * numpy.tan(v / 2)) # (rad)
        E_deg = numpy.degrees(E) # (deg)

        # Mean anomaly
        M = E - e * numpy.sin(E) # (rad)
        M_deg = numpy.degrees(M) # (deg)

        # Mean motion
        n = numpy.sqrt(mu / a**3) # (rad/s)

        # Time since periapsis passage
        delta_t = M / n
        t_p = t0 - datetime.timedelta(seconds=delta_t) # (s)

        H = H_deg = None

    elif (h == 0):
        # Time since periapsis passage
        delta_t = (numpy.tan(v / 2 + numpy.tan(3 * v / 2)) / 2) / numpy.sqrt(mu / p**3)
        t_p = t0 - datetime.timedelta(seconds=delta_t) # (s)

        a = E = E_deg = H = H_deg = M = M_deg = n = None

    else:
        # Semi-major axis
        a = -mu / h # (km)

        #Hyperbolic anomaly
        H = 2 * numpy.arctanh(numpy.tan(v / 2) * numpy.sqrt((e - 1) / (e + 1))) # (rad)
        H_deg = numpy.degrees(H) # (deg)
    
        # Mean motion
        n = numpy.sqrt(mu / numpy.abs(a)**3) # (rad/s)

        # Time since periapsis passage
        delta_t = (-H + e * numpy.sinh(H)) / n
        t_p = t0 - datetime.timedelta(seconds=delta_t) # (s)

        E, E_deg, M, M_deg = None

    dt = (t0 - t_p).total_seconds() # (s)

    ret_values = a, e, i_deg, p, Omega_deg, omega_deg, v_deg, u_deg, t_p, E_deg, H_deg, M_deg, n, h, dt, t0, r
    val_names =("Semi-major axis", "Eccentricity", "Inclination", "Semilatus rectum", "RAAN", "Argument of perigee",
    "True anomaly", "Argument of latitude", "Time since periapsis passage", "Eccentric anomaly",
    "Hyperbolic anomaly", "Mean anomaly", "Mean motion", "Specific orbital energy", "Time difference", "Start time", "Start position")

    ret_dict = dict(zip(val_names, ret_values))

    # Print the results
    if printable:
        if h < 0:
            print("Orbit type: Elliptical")
        elif h == 0:
            print("Orbit type: Parabolic")
        else:
            print("Orbit type: Hyperbolic")
        for name, value in ret_dict.items():
            print(f"{name}: {value}")
    return ret_dict



def spacecraft_position_velocity(new_time=5*3600 , dict_orbital_elements={}, printable=False, main=True): 
        # This function calculates the position and velocity of a spacecraft at a given time based on its orbital elements

    orb_dict = dict_orbital_elements
    new_time = orb_dict.get("Start time", None) + datetime.timedelta(seconds=new_time)
    e = orb_dict.get("Eccentricity", 0)
    n = orb_dict.get("Mean motion", 0)
    t_p = orb_dict.get("Time since periapsis passage", None)
    p = orb_dict.get("Semilatus rectum", 0)
    time_diff = (new_time - t_p).total_seconds()
    Omega = numpy.radians(orb_dict.get("RAAN", 0))
    omega = numpy.radians(orb_dict.get("Argument of perigee", 0))
    i = numpy.radians(orb_dict.get("Inclination", 0))
        
    if e < 1:
        # Elliptical orbit
        if main:
            E0 = 0
            eps = 1e-6  # Convergence criterion
            E = e * numpy.sin(E0) + n * time_diff

            j = 0
            while(abs(E - E0) > eps and ((not (j > 1e6)) or j < 1)):
                E0 = E
                E = e * numpy.sin(E0) + n * time_diff
                j += 1
        else:
            E = orb_dict.get("Eccentric anomaly", 0)
        v = 2 * numpy.arctan(numpy.sqrt((1 + e) / (1 - e)) * numpy.tan(E / 2))

    elif e == 1:
        # Parabolic orbit
        print("Parabolic orbit calculations are not implemented yet.")
        return None

    else:
        print("Hyperbolic orbit calculations are not implemented yet.")
        return None


    # Radial velocity
    Vr = numpy.sqrt(mu / p) * e * numpy.sin(v) # (km/s)

    # Transverse velocity
    Vt = numpy.sqrt(mu / p) * (1 + e * numpy.cos(v)) # (km/s)

    u = omega + v # Argument of latitude (deg)

    # Position
    r = p / (1 + e * numpy.cos(v)) # (km)

    # Transition from the orbital to the geocentric equatorial coordinate system
    # Rotation matrix
    A = numpy.array([
        [
            numpy.cos(u) * numpy.cos(Omega) - numpy.sin(u) * numpy.cos(i) * numpy.sin(Omega), 
            -numpy.sin(u) * numpy.cos(Omega) - numpy.cos(u) * numpy.cos(i) * numpy.sin(Omega), 
            numpy.sin(i) * numpy.sin(Omega)
        ],
        [
            numpy.cos(u) * numpy.sin(Omega) + numpy.sin(u) * numpy.cos(i) * numpy.cos(Omega), 
            -numpy.sin(u) * numpy.sin(Omega) + numpy.cos(u) * numpy.cos(i) * numpy.cos(Omega), 
            -numpy.sin(i) * numpy.cos(Omega)
        ],
        [
            numpy.sin(u) * numpy.sin(i), 
            numpy.cos(u) * numpy.sin(i), 
            numpy.cos(i)
        ]
    ])

    r_vector = numpy.dot(A, numpy.array([r, 0, 0])) # Position vector in geocentric equatorial coordinates (km)
    V_vector = numpy.dot(A, numpy.array([Vr, Vt, 0])) # Velocity vector in geocentric equatorial coordinates (km/s)

    if printable:
        print(f"Position vector (km): {r_vector}")
        print(f"Velocity vector (km/s): {V_vector}")
        print(f"Eccenric anomaly (deg): {numpy.degrees(E)}")
    return r_vector, V_vector, numpy.degrees(E)

def construct_motion_trajectory(orbital_elements={}, k=2, printable=False):
    # Construction of the Earth satellite's motion trajectory 
    orb = orbital_elements
    E0_deg = orb.get("Eccentric anomaly", 0)    
    E0 = numpy.radians(E0_deg) 
    r0 = orb.get("Start position", 0)
    e = orb.get("Eccentricity", 0)
    n = orb.get("Mean motion", 0)
    theta0 = numpy.atan2(r0[0], r0[1])
    # Start longitude
    l0 = -94.65 # (deg)

    def norm_lon(lon_deg):
        return (lon_deg + 180.0) % 360.0 - 180.0

    # Interval
    E_interval = [int(E0_deg), int(E0_deg + k * 360)]

    # Points of the trajectory
    points = []
    for E_deg in range(E_interval[0], E_interval[1], 1):
        E = numpy.radians(E_deg)
        dt = (E-E0-e*(numpy.sin(E)-numpy.sin(E0)))/n
        r_vector, *_ = spacecraft_position_velocity(new_time=dt, dict_orbital_elements=orb)
        if (r_vector[0]>0): 
            theta = numpy.arctan(r_vector[1]/r_vector[0])
        elif(r_vector[0] < 0 and r_vector[1] >= 0):
            theta = numpy.arctan(r_vector[1]/r_vector[0]) + numpy.pi
        elif(r_vector[0] < 0 and r_vector[1] < 0):
            theta = numpy.arctan(r_vector[1]/r_vector[0]) - numpy.pi
        elif(r_vector[0] == 0 and r_vector[1] > 0):
            theta = numpy.pi / 2
        elif(r_vector[0] == 0 and r_vector[1] < 0):
            theta = -numpy.pi/2
        else: theta = None

        dtheta = theta - theta0
        phi = numpy.arcsin(r_vector[2]/numpy.linalg.norm(r_vector))
        l = numpy.radians(l0) + dtheta - omega_earth*dt
        lon_deg = norm_lon(numpy.degrees(l))
        points.append([E_deg, lon_deg, numpy.degrees(phi)])

    if printable:
        for i in points:
            print(i)

        # Plotting a route on a world map (cylindrical projection)
    fig = plt.figure(figsize=(14, 7))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Подложка карты: суша, океан, береговые линии, границы, сетка
    ax.add_feature(cfeature.LAND.with_scale('110m'),
                   facecolor='0.92', edgecolor='none', zorder=0)
    ax.add_feature(cfeature.OCEAN.with_scale('110m'),
                   facecolor='#dbe9f4', edgecolor='none', zorder=0)
    ax.add_feature(cfeature.COASTLINE.with_scale('110m'),
                   linewidth=0.6, edgecolor='0.3', zorder=1)
    ax.add_feature(cfeature.BORDERS.with_scale('110m'),
                   linewidth=0.3, edgecolor='0.55', zorder=1)
    gl = ax.gridlines(draw_labels=True, linewidth=0.3,
                      color='gray', alpha=0.4)
    gl.top_labels = False
    gl.right_labels = False

    seg_x, seg_y = [], []
    prev_lon = None
    for E_deg, lon_deg, lat_deg in points:
        if prev_lon is not None and abs(lon_deg - prev_lon) > 180.0:
            if seg_x:
                ax.plot(seg_x, seg_y, '-', color='tab:blue', linewidth=1.3,
                        transform=ccrs.PlateCarree(), zorder=2)
            seg_x, seg_y = [], []
        seg_x.append(lon_deg)
        seg_y.append(lat_deg)
        prev_lon = lon_deg
    if seg_x:
        ax.plot(seg_x, seg_y, '-', color='tab:blue', linewidth=1.3,
                transform=ccrs.PlateCarree(), zorder=2)

    # The starting point of the route
    ax.plot(points[0][1], points[0][2], 'o', color='red', markersize=8,
            transform=ccrs.PlateCarree(), zorder=3,
            label=r'Начальная точка ($\lambda_0$, $\varphi_0$)')

    ax.set_title(f"Трасса ИСЗ на {k} витках (λ₀ = {l0}°)")
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()





