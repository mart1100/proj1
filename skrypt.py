from math import sin, cos, sqrt, atan, atan2, degrees, radians, tan
import sys

o = object()

class Transformacje:
    def __init__(self, model: str = "wgs84"):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy - promień równikowy
            b - mała półoś elipsoidy - promień południkowy
            flat - spłaszczenie
            ecc2 - mimośród^2
        + WGS84: https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
        + Inne powierzchnie odniesienia: https://en.wikibooks.org/wiki/PROJ.4#Spheroid
        + Parametry planet: https://nssdc.gsfc.nasa.gov/planetary/factsheet/index.html
        """
        if model == "wgs84" or model == "Wgs84" or model == "WGS84":
            self.a = 6378137.0 # semimajor_axis
            self.b = 6356752.31424518 # semiminor_axis
        elif model == "grs80" or model == "Grs80" or model == "GRS80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        elif model == "krasowski" or model == "Krasowski" or model == "Krassowski" or model == "krassowski" or model == "krass" or model == "Krass":
            self.a = 6378245.0
            self.b = 6356863.019
        else:
            raise NotImplementedError(f"{model} model not implemented")
        self.flat = (self.a - self.b) / self.a
        self.ecc = sqrt(2 * self.flat - self.flat ** 2) # eccentricity  WGS84:0.0818191910428 
        self.ecc2 = (2 * self.flat - self.flat ** 2) # eccentricity**2
        
    def deg2dms(self, deg):
        '''
        Funkcja zamieniająca stopnie dziesiętne na stopnie, minuty, sekundy.
        Parameters
        ----------
        deg : float
            stopnie w postaci dziesiętnej (decimal degrees)

        Returns
        -------
        d : stopnie
        m : minuty
        s : sekundy
        '''
        d = int(deg)
        m = int(60 * (deg - d))
        s = (deg - d - m/60) * 3600
        return(d,m,s)


    
    def xyz2plh(self, X, Y, Z, output = 'dec_degree'):
        """
        Algorytm Hirvonena - algorytm transformacji współrzędnych ortokartezjańskich (x, y, z)
        na współrzędne geodezyjne długość szerokość i wysokośc elipsoidalna (phi, lam, h). Jest to proces iteracyjny. 
        W wyniku 3-4-krotneej iteracji wyznaczenia wsp. phi można przeliczyć współrzędne z dokładnoscią ok 1 cm.     
        Parameters
        ----------
        X, Y, Z : FLOAT
             współrzędne w układzie orto-kartezjańskim, 

        Returns
        -------
        lat
            [stopnie dziesiętne] - szerokość geodezyjna
        lon
            [stopnie dziesiętne] - długośc geodezyjna.
        h : TYPE
            [metry] - wysokość elipsoidalna
        output [STR] - optional, defoulf 
            dec_degree - decimal degree
            dms - degree, minutes, sec
        """
        r   = sqrt(X**2 + Y**2)           # promień
        lat_prev = atan(Z / (r * (1 - self.ecc2)))    # pierwsze przybliilizenie
        lat = 0
        while abs(lat_prev - lat) > 0.000001/206265:    
            lat_prev = lat
            N = self.a / sqrt(1 - self.ecc2 * sin(lat_prev)**2)
            h = r / cos(lat_prev) - N
            lat = atan((Z/r) * (((1 - self.ecc2 * N/(N + h))**(-1))))
        lon = atan(Y/X)
        N = self.a / sqrt(1 - self.ecc2 * (sin(lat))**2);
        h = r / cos(lat) - N       
        if output == "dec_degree":
            return degrees(lat), degrees(lon), h 
        elif output == "dms":
            lat = self.deg2dms(degrees(lat))
            lon = self.deg2dms(degrees(lon))
            # return f"{lat[0]:02d}:{lat[1]:02d}:{lat[2]:.2f}", f"{lon[0]:02d}:{lon[1]:02d}:{lon[2]:.2f}", f"{h:.3f}"
            return f'{lat[0]:3d}{chr(176)}{abs(lat[1]):02d}\'{abs(lat[2]):.2f}\"', f'{lon[0]:3d}{chr(176)}{abs(lon[1]):02d}\'{abs(lon[2]):.2f}\"', f"{h:.3f}"
        else:
            raise NotImplementedError(f"{output} - output format not defined")
            

    def plh2xyz(self, phi, lam, h):
        '''
        Przeliczenie współrzędnych geodezyjnych (phi, lam, h) do współrzędnych orto-kartezjańskich (x, y, z).

        Parameters
        ----------
        phi : FLOAT
            [stopnie dziesiętne] - szerokosć geodezyjna
        lam : FLOAT
            [stopnie dziesiętne] - długosć geodezyjna
        h : FLOAT
            [m] - wysokosć elipsoidalna

        Returns
        -------
        x, y, z : FLOAT
            [m] - współrzędne w układzie orto-kartezjańskim.
        '''
        phi = radians(phi)
        lam = radians(lam)
        Rn = self.a / sqrt(1 - self.ecc2 * sin(phi)**2)
        q = Rn * self.ecc2 * sin(phi)
        x = (Rn + h) * cos(phi) * cos(lam)
        y = (Rn + h) * cos(phi) * sin(lam)
        z = (Rn + h) * sin(phi) - q
        return x,y,z
    
    
    def pl21992(self, phi, lam):
        '''
        Aplikacja odwzorowania Gaussa-Krugera dla układu 1992,
        dla elipsoidy GRS-80 (WGS-84) i stałej skali zniekształceń m0 = 0.9993. 
        Współrzędnymi wejsciowymi są współrzędne elipsoidalne (phi, lam).

        Parameters
        ----------
        phi : FLOAT
            [stopnie dziesiętne] - szerokosć geodezyjna
        lam : FLOAT
            [stopnie dziesiętne] - długosć geodezyjna

        Returns
        -------
        x1992 : FLOAT
            [m] - odcięta w układzie 1992
        y1992 : FLOAT
            [m] - rzędna w układzie 1992
        '''
        if self.a == 6378245.0:
            raise NotImplementedError("pl21992 method not implemented for Krasowski model")
        else:
            phi = radians(phi)
            lam = radians(lam)
            b2 = self.a**2 * (1 - self.ecc2)
            e_prim2 = (self.a**2 - b2) / b2
            deltal = lam - radians(19)
            t = tan(phi)
            eta2 = e_prim2 * (cos(phi)**2) 
            N = self.a / sqrt(1 - self.ecc2 * sin(phi)**2)
            A0 = 1 - (self.ecc2 / 4) - ((3 * (self.ecc2**2)) / 64) - ((5 * (self.ecc2**3)) / 256)
            A2 = (3 / 8) * (self.ecc2 + (self.ecc2**2) / 4 + (15 * (self.ecc2**3)) / 128)
            A4 = (15 / 256) * (self.ecc2**2 + (3 * (self.ecc2**3)) / 4)
            A6 = (35 * (self.ecc2**3)) / 3072
            sigma = self.a * (A0 * phi - A2 * sin(2 * phi) + A4 * sin(4 * phi) - A6 * sin(6*phi))
            xgk = sigma + ((deltal)**2)/2 * N * sin(phi) * cos(phi) * (1 + ((deltal)**2)/12 * (cos(phi))**2 * (5 - t**2 + 9 * eta2 + 4 * (eta2)**2) + ((deltal)**4)/360 * (cos(phi))**4 * (61 - 58*t**2 + t**4 + 270*eta2 - 330*eta2*t**2))
            ygk = deltal * N * cos(phi) * (1 + ((deltal)**2)/6 * (cos(phi))**2 * (1 - t**2 + eta2) + ((deltal)**4)/120 * (cos(phi))**4 * (5 - 18 * t**2 + t**4 + 14 * eta2 - 58 * eta2 * t**2))
            x1992 = xgk * 0.9993 - 5300000
            y1992 = ygk * 0.9993 + 500000
        return x1992, y1992
    
    
    def pl22000(self, phi, lam):
        '''
        Aplikacja odwzorowania Gaussa-Krugera dla układu 2000,
        dla elipsoidy GRS-80 (WGS-84) i stałej skali zniekształceń m0 = 0.999923. 
        Współrzędnymi wejsciowymi są współrzędne elipsoidalne.

        Parameters
        ----------
        phi : FLOAT
            [stopnie dziesietne] - szerokosć geograficzna
        lam : FLOAT
            [stopnie dziesietne] - dlugosć geograficzna

        Returns
        -------
        x2000 : FLOAT
            [m] - odcięta w układzie 2000
        y2000 : FLOAT
            [m] - rzędna w układzie 2000
        '''
        if self.a == 6378245.0:
            raise NotImplementedError("pl22000 method not implemented for Krasowski model")
        else:
            if lam < 16.5:
                lam0 = radians(15)
                c = lam0 / 3
            elif lam >= 16.5 and lam < 19.5:
                lam0 = radians(18)
                c = lam0 / 3
            elif lam >= 19.5 and lam < 22.5:
                lam0 = radians(21)
                c = lam0 / 3
            else:
                lam0 = radians(24)
                c = lam0 / 3 
            phi = radians(phi)
            lam = radians(lam)
            b2 = self.a**2 * (1 - self.ecc2)
            e_prim2 = (self.a**2 - b2) / b2
            deltal = lam - lam0
            t = tan(phi)
            eta2 = e_prim2 * (cos(phi)**2) 
            N = self.a / sqrt(1 - self.ecc2 * sin(phi)**2)
            A0 = 1 - (self.ecc2 / 4) - ((3 * (self.ecc2**2)) / 64) - ((5 * (self.ecc2**3)) / 256)
            A2 = (3 / 8) * (self.ecc2 + (self.ecc2**2) / 4 + (15 * (self.ecc2**3)) / 128)
            A4 = (15 / 256) * (self.ecc2**2 + (3 * (self.ecc2**3)) / 4)
            A6 = (35 * (self.ecc2**3)) / 3072
            sigma = self.a * (A0 * phi - A2 * sin(2 * phi) + A4 * sin(4 * phi) - A6 * sin(6*phi))
            xgk = sigma + ((deltal)**2)/2 * N * sin(phi) * cos(phi) * (1 + ((deltal)**2)/12 * (cos(phi))**2 * (5 - t**2 + 9 * eta2 + 4 * (eta2)**2) + ((deltal)**4)/360 * (cos(phi))**4 * (61 - 58*t**2 + t**4 + 270*eta2 - 330*eta2*t**2))
            ygk = deltal * N * cos(phi) * (1 + ((deltal)**2)/6 * (cos(phi))**2 * (1 - t**2 + eta2) + ((deltal)**4)/120 * (cos(phi))**4 * (5 - 18 * t**2 + t**4 + 14 * eta2 - 58 * eta2 * t**2))
            x2000 = xgk * 0.999923
            y2000 = ygk * 0.999923 + 500000 + c * 1000000
        return x2000, y2000
            
if __name__ == "__main__":
    # utworzenie obiektu
    geo = Transformacje(model = "wgs84")
    print(sys.argv)
    # dane XYZ geocentryczne
    # X = 3664940.500; Y = 1409153.590; Z = 5009571.170
    # phi, lam, h = geo.xyz2plh(X, Y, Z)
    # print(phi, lam, h)
    # phi, lam, h = geo.xyz2plh2(X, Y, Z)
    # print(phi, lam, h)
    input_file_path = sys.argv[-1]
    
    if '--header_lines' in sys.argv:
        header_lines = int(sys.argv[3])
    
    if '--xyz2plh' in sys.argv and '--plh2xyz' in sys.argv:
        print('Możesz podać tylko jedną flagę.')
        
    elif '--xyz2plh' in sys.argv:
        with open(input_file_path, 'r') as f:
            lines = f.readlines()
            lines = lines[4:]
        
            coords_plh = []
            for line in lines: 
                line = line.strip()
                x_str,y_str,z_str = line.split(',')
                x,y,z = float(x_str),float(y_str),float(z_str)
                if 'dms' in sys.argv:
                    p,l,h = geo.xyz2plh(x,y,z, output = 'dms')
                else:
                    p,l,h = geo.xyz2plh(x,y,z)
                coords_plh.append([p,l,h])
    
        with open('result_xyz2plh.txt','w+') as f:
            f.write('phi[deg], lam[deg], h[m] \n')
            for coords in coords_plh:
                coords_plh_line = ','.join([str(coord) for coord in coords])
                f.write(coords_plh_line + '\n')
            
            
    elif '--plh2xyz' in sys.argv:  
            
        with open(input_file_path, 'r') as f:
            lines = f.readlines()
            lines = lines[4:]
            
        coords_xyz = []
        for line in lines: 
            line = line.strip()
            phi_str,lam_str,h_str = line.split(',')
            phi, lam, h = float(phi_str),float(lam_str),float(h_str)
            x, y, z = geo.plh2xyz(phi,lam,h)
            coords_xyz.append([x,y,z])
    
        with open('result_plh2xyz.txt','w+') as f:
            f. write('x[m], y[m], z[m] \n')
            for coords in coords_xyz:
                coords_xyz_line = ','.join([f'{coord:11.3f}' for coord in coords])
                f.write(coords_xyz_line + '\n')

    elif '--pl21992' in sys.argv:
        with open(input_file_path, 'r') as f:
        	lines = f.readlines()
        	lines = lines[header_lines:]
            
        coords_1992 = []
        for line in lines: 
            line = line.strip()
            phi_str,lam_str,h_str = line.split(',')
            phi, lam,h = float(phi_str),float(lam_str),float(h_str)
            x, y = geo.pl21992(phi, lam)
            coords_1992.append([x,y])
        
        with open('result_pl21992.txt','w+') as f:
            f. write('x[m], y[m] \n')
            for coords in coords_1992:
                coords_1992_line = ','.join([f'{coord:11.3f}' for coord in coords])
                f.write(coords_1992_line + '\n')
