#!/usr/bin/env python3 

# For directory access.
import os
import sys

# For datetimes
import datetime

# For timezone conversion info.
import pytz

# For logging.
import logging
import logging.config

# Import the Swiss Ephemeris
import swisseph as swe

##############################################################################

# Directory where the swiss ephemeris files are located.
SWISS_EPHEMERIS_DATA_DIR = os.path.join(sys.path[0], "../data/ephe")

##############################################################################


class PlanetaryInfo:
    """Class that holds information about a planet's position, speed, etc.,
    for a given timestamp.

    The following is a list of data fields accessable through a fully populated
    PlanetaryInfo object.

    # Get info for the Sun.
    p = Ephemeris.getPlanetaryInfo(swe.SUN, datetime.datetime.utcnow())

    # Data fields in 'p':
    p.name      = <Planet Name>
    p.id        = <Planet ID>
    p.dt        = <Timestamp for this planetary data, as a datetime.datetime with datetime.tzinfo>
    p.julianDay = <Timestamp for this planetary data, as a Julian Day integer in UTC>


    p.geocentric['tropical']['longitude']       = <Longitude (degrees)>
    p.geocentric['tropical']['latitude']        = <Latitude (degrees)>
    p.geocentric['tropical']['distance']        = <Distance (AU)>
    p.geocentric['tropical']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.geocentric['tropical']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.geocentric['tropical']['distance_speed']  = <Distance speed (AU/day)>
    p.geocentric['tropical']['rectascension']       = <Rectascension (degrees)>
    p.geocentric['tropical']['declination']         = <Declination (degrees)>
    p.geocentric['tropical']['distance']            = <Distance (AU)>
    p.geocentric['tropical']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.geocentric['tropical']['declination_speed']   = <Latitude speed (degrees/day)>
    p.geocentric['tropical']['distance_speed']      = <Distance speed (AU/day)>
    p.geocentric['tropical']['X']  = <X location (AU)>
    p.geocentric['tropical']['Y']  = <Y location (AU)>
    p.geocentric['tropical']['Z']  = <Z location (AU)>
    p.geocentric['tropical']['dX'] = <X speed (AU)>
    p.geocentric['tropical']['dY'] = <Y speed (AU)>
    p.geocentric['tropical']['dZ'] = <Z speed (AU)>

    p.geocentric['sidereal']['longitude']       = <Longitude (degrees)>
    p.geocentric['sidereal']['latitude']        = <Latitude (degrees)>
    p.geocentric['sidereal']['distance']        = <Distance (AU)>
    p.geocentric['sidereal']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.geocentric['sidereal']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.geocentric['sidereal']['distance_speed']  = <Distance speed (AU/day)>
    p.geocentric['sidereal']['rectascension']       = <Rectascension (degrees)>
    p.geocentric['sidereal']['declination']         = <Declination (degrees)>
    p.geocentric['sidereal']['distance']            = <Distance (AU)>
    p.geocentric['sidereal']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.geocentric['sidereal']['declination_speed']   = <Latitude speed (degrees/day)>
    p.geocentric['sidereal']['distance_speed']      = <Distance speed (AU/day)>
    p.geocentric['sidereal']['X']  = <X location (AU)>
    p.geocentric['sidereal']['Y']  = <Y location (AU)>
    p.geocentric['sidereal']['Z']  = <Z location (AU)>
    p.geocentric['sidereal']['dX'] = <X speed (AU)>
    p.geocentric['sidereal']['dY'] = <Y speed (AU)>
    p.geocentric['sidereal']['dZ'] = <Z speed (AU)>


    p.topocentric['tropical']['longitude']       = <Longitude (degrees)>
    p.topocentric['tropical']['latitude']        = <Latitude (degrees)>
    p.topocentric['tropical']['distance']        = <Distance (AU)>
    p.topocentric['tropical']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.topocentric['tropical']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.topocentric['tropical']['distance_speed']  = <Distance speed (AU/day)>
    p.topocentric['tropical']['rectascension']       = <Rectascension (degrees)>
    p.topocentric['tropical']['declination']         = <Declination (degrees)>
    p.topocentric['tropical']['distance']            = <Distance (AU)>
    p.topocentric['tropical']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.topocentric['tropical']['declination_speed']   = <Latitude speed (degrees/day)>
    p.topocentric['tropical']['distance_speed']      = <Distance speed (AU/day)>
    p.topocentric['tropical']['X']  = <X location (AU)>
    p.topocentric['tropical']['Y']  = <Y location (AU)>
    p.topocentric['tropical']['Z']  = <Z location (AU)>
    p.topocentric['tropical']['dX'] = <X speed (AU)>
    p.topocentric['tropical']['dY'] = <Y speed (AU)>
    p.topocentric['tropical']['dZ'] = <Z speed (AU)>

    p.topocentric['sidereal']['longitude']       = <Longitude (degrees)>
    p.topocentric['sidereal']['latitude']        = <Latitude (degrees)>
    p.topocentric['sidereal']['distance']        = <Distance (AU)>
    p.topocentric['sidereal']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.topocentric['sidereal']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.topocentric['sidereal']['distance_speed']  = <Distance speed (AU/day)>
    p.topocentric['sidereal']['rectascension']       = <Rectascension (degrees)>
    p.topocentric['sidereal']['declination']         = <Declination (degrees)>
    p.topocentric['sidereal']['distance']            = <Distance (AU)>
    p.topocentric['sidereal']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.topocentric['sidereal']['declination_speed']   = <Latitude speed (degrees/day)>
    p.topocentric['sidereal']['distance_speed']      = <Distance speed (AU/day)>
    p.topocentric['sidereal']['X']  = <X location (AU)>
    p.topocentric['sidereal']['Y']  = <Y location (AU)>
    p.topocentric['sidereal']['Z']  = <Z location (AU)>
    p.topocentric['sidereal']['dX'] = <X speed (AU)>
    p.topocentric['sidereal']['dY'] = <Y speed (AU)>
    p.topocentric['sidereal']['dZ'] = <Z speed (AU)>


    p.heliocentric['tropical']['longitude']       = <Longitude (degrees)>
    p.heliocentric['tropical']['latitude']        = <Latitude (degrees)>
    p.heliocentric['tropical']['distance']        = <Distance (AU)>
    p.heliocentric['tropical']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.heliocentric['tropical']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.heliocentric['tropical']['distance_speed']  = <Distance speed (AU/day)>
    p.heliocentric['tropical']['rectascension']       = <Rectascension (degrees)>
    p.heliocentric['tropical']['declination']         = <Declination (degrees)>
    p.heliocentric['tropical']['distance']            = <Distance (AU)>
    p.heliocentric['tropical']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.heliocentric['tropical']['declination_speed']   = <Latitude speed (degrees/day)>
    p.heliocentric['tropical']['distance_speed']      = <Distance speed (AU/day)>
    p.heliocentric['tropical']['X']  = <X location (AU)>
    p.heliocentric['tropical']['Y']  = <Y location (AU)>
    p.heliocentric['tropical']['Z']  = <Z location (AU)>
    p.heliocentric['tropical']['dX'] = <X speed (AU)>
    p.heliocentric['tropical']['dY'] = <Y speed (AU)>
    p.heliocentric['tropical']['dZ'] = <Z speed (AU)>

    p.heliocentric['sidereal']['longitude']       = <Longitude (degrees)>
    p.heliocentric['sidereal']['latitude']        = <Latitude (degrees)>
    p.heliocentric['sidereal']['distance']        = <Distance (AU)>
    p.heliocentric['sidereal']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.heliocentric['sidereal']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.heliocentric['sidereal']['distance_speed']  = <Distance speed (AU/day)>
    p.heliocentric['sidereal']['rectascension']       = <Rectascension (degrees)>
    p.heliocentric['sidereal']['declination']         = <Declination (degrees)>
    p.heliocentric['sidereal']['distance']            = <Distance (AU)>
    p.heliocentric['sidereal']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.heliocentric['sidereal']['declination_speed']   = <Latitude speed (degrees/day)>
    p.heliocentric['sidereal']['distance_speed']      = <Distance speed (AU/day)>
    p.heliocentric['sidereal']['X']  = <X location (AU)>
    p.heliocentric['sidereal']['Y']  = <Y location (AU)>
    p.heliocentric['sidereal']['Z']  = <Z location (AU)>
    p.heliocentric['sidereal']['dX'] = <X speed (AU)>
    p.heliocentric['sidereal']['dY'] = <Y speed (AU)>
    p.heliocentric['sidereal']['dZ'] = <Z speed (AU)>
    """

    def __init__(self, planetName, planetId, dt, julianDay,
                 geocentricDict=None,
                 topocentricDict=None,
                 heliocentricDict=None):
        """Initializes the PlanetaryInfo class with the given parameters.
        
        Parameters are as follows:
        
        planetName - String holding the name of the planet.
        planetId   - Integer ID that represents the planet in the
                     Swiss Ephemeris.
        dt         - The datetime.datetime object that holds the timestamp for
                     which the planetary information and data is valid for.
        julianDay  - The float value that holds the timestamp for the
                     which the planetary information and data is valid
                     for.  This should be equivalent to the value in
                     'dt' converted to julian day.
        """
        
        self.name = planetName
        self.id = planetId
        self.dt = dt
        self.julianDay = julianDay
        self.geocentric = geocentricDict
        self.topocentric = topocentricDict
        self.heliocentric = heliocentricDict


    def __str__(self):
        """Returns a string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns a string representation of this object."""

        # Datetime format to datetime.strftime().
        fmt = "%Y-%m-%d %H:%M:%S.%f %Z%z"

        formatStr = "[name={}, id={}, datetime={}, julianDay={}, " + \
                    "geocentric={}, topocentric={}, heliocentric={}]"

        returnStr = formatStr.format(self.name, 
                                     self.id, 
                                     self.dt.strftime(fmt),
                                     self.julianDay,
                                     self.geocentric,
                                     self.topocentric,
                                     self.heliocentric)

        return returnStr


class Ephemeris:
    """Provides access to ephemeris data.  Please exercise caution when 
    using this class in multithreaded environments because the underlying
    implementation of swisseph is a simple C library and there is no way to
    make sure the internally stored data maintains its integrity
    across multiple threads.

    The recommended way to use this class:

    ############################

    # Initialize the class.  This only needs to be called once 
    # before being used.
    Ephemeris.initialize()

    # Set the geographic position (required).
    Ephemeris.setGeographicPosition(-77.084444, 38.890277)

    # Call the get function for the planet of interest.
    p = getVenusPlanetaryInfo(datetime.datetime.utcnow())

    # Extract the value(s) needed from teh PlanetaryInfo object.
    longitude = p.geocentric['tropical']['longitude']

    # Print values.
    print("Venus geocentric tropical longitude is: {}".format(longitude))

    # Close when all done.
    Ephemeris.closeEphemeris()

    #############################


    For more fine-grained control, the class can also be used by manually
    calling the individual set-flags functions and then calling calc_ut().
    """

    # Logger object for this class.
    log = logging.getLogger("ephemeris.Ephemeris")


    # Flag that is used in Swiss Ephemeris calculations.  
    # We make mods to this variable to add options.
    iflag = 0

    @staticmethod
    def initialize():
        """Initializes the Ephemeris with default settings."""

        Ephemeris.log.debug("Entering initialize()")


        # Set up the swiss ephemeris data directory location.
        Ephemeris.log.info("Setting Ephemeris data directory to " +
                           SWISS_EPHEMERIS_DATA_DIR)
        swe.set_ephe_path(SWISS_EPHEMERIS_DATA_DIR)

        # Reset the iflag used.
        Ephemeris.iflag = 0

        # Use Swiss Ephemeris (and not JPL or Moshier)
        Ephemeris.log.info("Setting flag to use Swiss Ephemeris")
        Ephemeris.iflag |= swe.FLG_SWIEPH

        # Calculate speeds when doing calculations.
        Ephemeris.log.info("Setting flag to calculate speeds")
        Ephemeris.iflag |= swe.FLG_SPEED

        # Use true positions of the planets by default.
        Ephemeris.log.info("Setting to use true planetary positions")
        Ephemeris.setTruePlanetaryPositions()
        
    @staticmethod
    def closeEphemeris():
        """Does any cleanup needed to close the ephemeris.  
        Using the ephemeris after calling this yields undefined results.  
        """

        Ephemeris.log.debug("Entered closeEphemeris()")

        # Call close on the Swiss Ephemeris so it can cleanup files and
        # deallocate memory, etc.
        swe.close()

        Ephemeris.log.debug("Leaving closeEphemeris()")

    @staticmethod
    def setGeographicPosition(geoLongitudeDeg, 
                              geoLatitudeDeg, 
                              altitudeMeters=0.0):
        """Sets the position for planetary calculations.

        Parameters:
        geoLongitudeDeg - Longitude in degrees.  West longitudes are negative,
                          East longitudes are positive.
        geoLatitudeDeg  - Latitude in degrees.
        altitudeMeters  - Altitude in meters.
        """

        debugStr = "Entering setGeographicPosition(lon={}, lat={}, alt={})"
        Ephemeris.log.debug(debugStr.format(geoLongitudeDeg, 
                                            geoLatitudeDeg,
                                            altitudeMeters))

        swe.set_topo(geoLatitudeDeg, geoLatitudeDeg, altitudeMeters)

        Ephemeris.log.debug("Leaving setGeographicPosition()")


    @staticmethod
    def datetimeToJulianDay(dt):
        """Utility function for converting a datetime.datetime object 
        to Julian Day.  
        
        Parameters:
        
        dt - A datetime.datetime object with the 'tzinfo' attribute set
        as a pytz-created datetime.tzinfo.  
        
        The tzinfo attribute needing to be set to a pytz-created
        datetime.tzinfo is to allow us to normalize for 
        changes in the timezone properly.  The conversion process 
        to a Julian Day utilizes the Swiss Ephemeris.
        """

        Ephemeris.log.debug("Entering datetimeToJulianDay({})".format(dt))

        # Error checking of the input datetime object.
        if (dt.tzinfo == None):
            errStr = "Ephemeris.datetimeToJulianDay(): tzinfo attribute " + \
                "in the datetime.datetime cannot be None"
            raise ValueError(errStr)

        # Convert to UTC.
        dtUtc = pytz.utc.normalize(dt.astimezone(pytz.utc))

        Ephemeris.log.debug("datetime converted to UTC is: {}".format(dtUtc))

        # Get the Julian Day as calculated by Swiss Ephemeris.
        cal = swe.GREG_CAL
        (jd_et, jd_ut) = \
                swe.utc_to_jd(dtUtc.year, dtUtc.month, dtUtc.day, 
                              dtUtc.hour, dtUtc.minute, dtUtc.second,
                              cal)

        # We use the Julian Day for Universal Time (UT).
        jd = jd_ut
        
        debugStr = "Swiss Ephemeris converted UTC datetime({}) to " + \
                   "jd_et={}, jd_ut={}.  Using jd_ut as julian day."
        Ephemeris.log.debug(debugStr.format(dtUtc, jd_et, jd_ut))

        Ephemeris.log.debug("Leaving datetimeToJulianDay() and " + \
                            "returning {}".format(jd))
        return jd


    @staticmethod
    def julianDayToDatetime(jd, tzInfo=pytz.utc):
        """Utility function for converting a Julian Day number to 
        a datetime.datetime object.  The returned datetime object is created 
        with the timestamp in the timezone specified (or UTC by default if the
        argument is not specified).
        
        This conversion process utilizes the Swiss Ephemeris to 
        do the conversion and calculation.
        """
        
        Ephemeris.log.debug("Entering julianDayToDatetime({}, {})".\
                            format(jd, tzInfo))

        gregFlag = 1
        (year, month, day, hour, mins, secs) = swe.jdut1_to_utc(jd, gregFlag)

        debugStr = "Got converted values from Swiss Ephemeris: " + \
                   "year={}, month={}, day={}, hour={}, mins={}, secs={}"
        Ephemeris.log.debug(debugStr.\
                            format(year, month, day, hour, mins, secs))

        # Here we need to convert a float seconds to an integer seconds 
        # plus a integer microseconds.  FYI: int() truncates towards zero.
        secsTruncated = int(secs)
        usecs = int(round((secs - secsTruncated) * 1000000))

        Ephemeris.log.debug("secs={}, secsTruncated={}, usecs={}".\
                            format(secs, secsTruncated, usecs))


        # Create a datetime.datetime in UTC.
        dtUtc = datetime.datetime(year, month, day, hour, mins, 
                               secsTruncated, usecs, pytz.utc)

        # Convert to the timezone specified.
        dt = tzInfo.normalize(dtUtc.astimezone(tzInfo))

        Ephemeris.log.debug("Returning julian day converted from " + \
                            "jd={} to datetime={}".format(jd, dt))

        return dt


    @staticmethod
    def getPlanetNameForId(planetId):
        """Returns the string representation of a planet name for the given
        planet ID.

        Parameters:
        planetId - Integer value that maps to a planet ID in the Swiss Ephemeris.
        """

        # Use the Swiss Ephemeris call to get the planet name.
        planetName = swe.get_planet_name(planetId)

        # Do a bit of cleanup of some of the planet names (if it's one of the
        # following planets).
        if planetName == "mean Node":
            planetName = "Mean North Node"
        elif planetName == "true Node":
            planetName = "True North Node"
        elif planetName == "mean Apogee":
            planetName = "Mean Lunar Apogee"
        elif planetName == "osc. Apogee":
            planetName = "Osculating Lunar Apogee"
        elif planetName == "intp. Apogee":
            planetName = "Interpolated Lunar Apogee"
        elif planetName == "intp. Perigee":
            planetName = "Interpolated Lunar Perigee"

        return planetName


    @staticmethod
    def setSiderealZodiac():
        """Initializes the settings to use the sidereal zodiac for
        calculations.  This function sets the Ayanamsa to use as Lahiri, as
        calculated in the Swiss Ephemeris.  It should be noted that the
        calculation done for the Lahiri Ayanamsa from the Swiss Ephemeris is
        not the most accurate, and can be off by approximately 2 arc minutes.
        There are better ways to calculate this Ayanamsa.  More details on this
        topic can be found at: 
        http://jyotish-blog.blogspot.com/2005/12/ayanamsha-in-jhora-702-vs-swiss.html
        """

        Ephemeris.log.debug("Entering setSiderealZodiac()")

        Ephemeris.log.debug("swe.FLG_SIDEREAL == {}".format(swe.FLG_SIDEREAL))
        Ephemeris.log.debug("iflag before: {}".format(Ephemeris.iflag))
        Ephemeris.iflag |= swe.FLG_SIDEREAL
        Ephemeris.log.debug("iflag after: {}".format(Ephemeris.iflag))
        swe.set_sid_mode(swe.SIDM_LAHIRI)

        Ephemeris.log.debug("Leaving setSiderealZodiac()")

    def setTropicalZodiac():
        """Initializes the settings to use the tropical zodiac for
        calculations
        """

        Ephemeris.log.debug("Entering setTropicalZodiac()")

        Ephemeris.log.debug("swe.FLG_SIDEREAL == {}".format(swe.FLG_SIDEREAL))
        Ephemeris.log.debug("iflag before: {}".format(Ephemeris.iflag))
        Ephemeris.iflag &= (~swe.FLG_SIDEREAL)
        Ephemeris.log.debug("iflag after: {}".format(Ephemeris.iflag))

        Ephemeris.log.debug("Leaving setTropicalZodiac()")
        

    @staticmethod
    def setTruePlanetaryPositions():
        """Initializes the settings to use the true planetary positions"""

        Ephemeris.log.debug("Entering setTruePlanetaryPositions()")

        Ephemeris.log.debug("swe.FLG_TRUEPOS == {}".format(swe.FLG_TRUEPOS))
        Ephemeris.log.debug("iflag before: {}".format(Ephemeris.iflag))
        Ephemeris.iflag |= swe.FLG_TRUEPOS
        Ephemeris.log.debug("iflag after: {}".format(Ephemeris.iflag))

        Ephemeris.log.debug("Leaving setTruePlanetaryPositions()")

    @staticmethod
    def setApparentPlanetaryPositions():
        """Initializes the settings to use the true planetary positions"""

        Ephemeris.log.debug("Entering setApparentPlanetaryPositions()")

        Ephemeris.log.debug("swe.FLG_TRUEPOS == {}".format(swe.FLG_TRUEPOS))
        Ephemeris.log.debug("iflag before: {}".format(Ephemeris.iflag))
        Ephemeris.iflag &= (~swe.FLG_TRUEPOS)
        Ephemeris.log.debug("iflag after: {}".format(Ephemeris.iflag))

        Ephemeris.log.debug("Leaving setApparentPlanetaryPositions()")


    @staticmethod
    def __clearCoordinateSystemFlags():
        """Private function that clears the flags for the coordinate position
        calculations.
        """

        debugStr ="Clearing flags for different coordinate systems." 
        Ephemeris.log.debug(debugStr)

        Ephemeris.iflag &= (~swe.FLG_EQUATORIAL)
        Ephemeris.iflag &= (~swe.FLG_XYZ)
        Ephemeris.iflag &= (~swe.FLG_RADIANS)

    @staticmethod
    def setEclipticalCoordinateSystemFlag():
        """Sets the ephemeris to return results in ecliptical polar
        coordinates.  This is the default setting in Swiss Ephemeris and is
        equvalent to the flag cleared.  This causes swe_calc() and
        swe_calc_ut() to return the following values when it is called:
        (
         longitude in degrees, 
         latitude in degrees, 
         distance in AU,
         longitude speed in deg/day, 
         latitude speed in deg/day,
         speed in distance units AU/day
         )
        """

        Ephemeris.log.debug("setEclipticalCoordinateSystemFlag()")
        # Just clear the coordinate system flags.  Ecliptical coordinates 
        # is the default, so we don't need to do anything more than just 
        # clear the flags. 
        Ephemeris.__clearCoordinateSystemFlags()

    @staticmethod
    def setEquatorialCoordinateSystemFlag():
        """Sets the ephemeris to return results in equatorial 
        coordinates.  This causes swe_calc() and swe_calc_ut() to return
        the following values when it is called:
        (
         Rectascension (degrees in Earth sky)
         Declination (degrees in Earth sky.  Range is: -90 to +90, where -90 is
                      south pole),
         Distance (units in AU),
         Speed in rectascension (deg/day),
         Speed in declination (deg/day),
         Speed in distance (AU/day)
         )
        """

        Ephemeris.log.debug("setEquatorialCoordinateSystemFlag()")
        Ephemeris.__clearCoordinateSystemFlags()
        Ephemeris.iflag |= swe.FLG_EQUATORIAL

    @staticmethod
    def setRectangularCoordinateSystemFlag():
        """Sets the ephemeris to return results in XYZ coordinates.
        This causes swe_calc() and swe_calc_ut() to return the following values
        when it is called:
        (
        X (units in AU),
        Y (units in AU),
        Z (units in AU),
        dX (units in AU/day),
        dY (units in AU/day),
        dZ (units in AU/day)
        )
        """

        Ephemeris.log.debug("setRectangularCoordinateSystemFlag()")
        Ephemeris.__clearCoordinateSystemFlags()
        Ephemeris.iflag |= swe.FLG_XYZ

    @staticmethod
    def setRadiansCoordinateSystemFlag():
        """Sets the ephemeris to return results in radians coordinates"""

        Ephemeris.log.debug("setRadiansCoordinateSystemFlag()")
        Ephemeris.__clearCoordinateSystemFlags()
        Ephemeris.iflag |= swe.FLG_RADIANS

    @staticmethod
    def unsetRadiansCoordinateSystemFlag():
        """Unsets the ephemeris from returning results in radians
        coordinates.  Future calls to swe_calc() and swe_calc_ut() will 
        return values in degrees.
        """

        Ephemeris.log.debug("unsetRadiansCoordinateSystemFlag()")
        Ephemeris.iflag &= (~swe.FLG_RADIANS)

    @staticmethod
    def setHeliocentricCalculations():
        """Sets the flag to do heliocentric calculations."""

        Ephemeris.log.debug("setHeliocentricCalculations()")
        Ephemeris.iflag &= (~swe.FLG_TOPOCTR)
        Ephemeris.iflag |= swe.FLG_HELCTR
        
    @staticmethod
    def setGeocentricCalculations():
        """Sets the flag to do geocentric calculations."""

        Ephemeris.log.debug("setGeocentricCalculations()")
        Ephemeris.iflag &= (~swe.FLG_HELCTR)
        Ephemeris.iflag &= (~swe.FLG_TOPOCTR)
        
    @staticmethod
    def setTopocentricCalculations():
        """Sets the flag to do topocentric calculations."""

        Ephemeris.log.debug("setTopocentricCalculations()")
        Ephemeris.iflag &= (~swe.FLG_HELCTR)
        Ephemeris.iflag |= swe.FLG_TOPOCTR

    @staticmethod
    def calc_ut(jd, planet, flag=swe.FLG_SWIEPH+swe.FLG_SPEED):
        """Wrapper for the Swiss Ephemeris call calc_ut().
        Parameters and return values are the same as they are for calc_ut().
        This is added to enhance debugging.  
        
        Return value:
        Returns a tuple of 6 floats.
        
        Parameters are the same as they are to calc_ut():
        jd - Float value for the Julian Day
        planet - Integer value for the planet to do the calculation for.
        flag - Integer for what flags to use in the calculation.
        """
        
        Ephemeris.log.debug("Entering calc_ut(jd={}, planet={}, flag={})".\
                format(jd, planet, flag))

        # Do the calculation.
        (arg1, arg2, arg3, arg4, arg5, arg6) = swe.calc_ut(jd, planet, flag)

        # Log some debug for the calculations and parameters.
        if (Ephemeris.log.isEnabledFor(logging.DEBUG)):
            Ephemeris.__logDebugCalcUTInfo(jd, planet, flag, 
                                           arg1, arg2, arg3, arg4, arg5, arg6)
        
        Ephemeris.log.debug("Leaving calc_ut(jd={}, planet={}, flag={})".\
                format(jd, planet, flag))

        # Return calculated values.
        return (arg1, arg2, arg3, arg4, arg5, arg6)

    @staticmethod
    def __logDebugCalcUTInfo(jd, planet, flag, 
                             arg1, arg2, arg3, arg4, arg5, arg6):
        """Helper function that simply logs the parameters provided.
        These are the parameters provided to calc_ut() and returned 
        values from calc_ut().
        """
        
        # Only continue and log if the logging level is set to DEBUG.
        if (not Ephemeris.log.isEnabledFor(logging.DEBUG)):
            return

        debugStr = "calc_ut(): ----------------------------------------------"
        Ephemeris.log.debug(debugStr)
        Ephemeris.log.debug("calc_ut(): jd={}, planet={}, flag={}".\
                format(jd, planet, flag))

        Ephemeris.log.debug("calc_ut(): Julian day {} converts to UTC timestamp: {}".\
                format(jd, Ephemeris.julianDayToDatetime(jd)))

        Ephemeris.log.debug("calc_ut(): Planet {} converts to: {}".\
                format(planet, Ephemeris.getPlanetNameForId(planet)))

        Ephemeris.log.debug("calc_ut(): Flags that set are: ")
        
        if (Ephemeris.iflag & swe.FLG_JPLEPH):
            Ephemeris.log.debug("calc_ut():  - FLG_JPLEPH")
        if (Ephemeris.iflag & swe.FLG_SWIEPH):
            Ephemeris.log.debug("calc_ut():  - FLG_SWIEPH")
        if (Ephemeris.iflag & swe.FLG_MOSEPH):
            Ephemeris.log.debug("calc_ut():  - FLG_MOSEPH")
        if (Ephemeris.iflag & swe.FLG_HELCTR):
            Ephemeris.log.debug("calc_ut():  - FLG_HELCTR")
        if (Ephemeris.iflag & swe.FLG_TRUEPOS):
            Ephemeris.log.debug("calc_ut():  - FLG_TRUEPOS")
        if (Ephemeris.iflag & swe.FLG_SPEED):
            Ephemeris.log.debug("calc_ut():  - FLG_SPEED")
        if (Ephemeris.iflag & swe.FLG_EQUATORIAL):
            Ephemeris.log.debug("calc_ut():  - FLG_EQUATORIAL")
        if (Ephemeris.iflag & swe.FLG_XYZ):
            Ephemeris.log.debug("calc_ut():  - FLG_XYZ")
        if (Ephemeris.iflag & swe.FLG_RADIANS):
            Ephemeris.log.debug("calc_ut():  - FLG_RADIANS")
        if (Ephemeris.iflag & swe.FLG_TOPOCTR):
            Ephemeris.log.debug("calc_ut():  - FLG_TOPOCTR")
        if (Ephemeris.iflag & swe.FLG_SIDEREAL):
            Ephemeris.log.debug("calc_ut():  - FLG_SIDEREAL")

        Ephemeris.log.debug("calc_ut(): Calculated values:")
        if (Ephemeris.iflag & swe.FLG_EQUATORIAL):
            # Equatorial position calculated.
            # output here:
            debugStr = "calc_ut():  {:<36}{}"
            Ephemeris.log.debug(debugStr.\
                    format("Rectascension (deg):", arg1))
            Ephemeris.log.debug(debugStr.\
                    format("Declination (deg):", arg2))
            Ephemeris.log.debug(debugStr.\
                    format("Distance (AU):", arg3))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in rectascension (deg/day):", arg4))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in declination (deg/day):", arg5))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in distance (AU/day)", arg6))
        elif (Ephemeris.iflag & swe.FLG_XYZ): 
            # XYZ position calculated.
            debugStr = "calc_ut():  {:<15}{}"
            Ephemeris.log.debug(debugStr.\
                    format("X (AU):", arg1))
            Ephemeris.log.debug(debugStr.\
                    format("Y (AU):", arg2))
            Ephemeris.log.debug(debugStr.\
                    format("Z (AU):", arg3))
            Ephemeris.log.debug(debugStr.\
                    format("dX (AU/day):", arg4))
            Ephemeris.log.debug(debugStr.\
                    format("dY (AU/day):", arg5))
            Ephemeris.log.debug(debugStr.\
                    format("dZ (AU/day):", arg6))
        else:
            # Ecliptic position calculated.
            debugStr = "calc_ut():  {:<32}{}"
            Ephemeris.log.debug(debugStr.\
                    format("Longitude (deg):", arg1))
            Ephemeris.log.debug(debugStr.\
                    format("Latitude (deg):", arg2))
            Ephemeris.log.debug(debugStr.\
                    format("Distance (AU):", arg3))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in longitude (deg/day):", arg4))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in latitude (deg/day):", arg5))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in distance (AU/day):", arg6))
    
    # TODO:  need to add functions for getting house cusp locations for different house systems.  

    @staticmethod
    def getPlanetaryInfo(planet, dt):
        """Returns a PlanetaryInfo object with a bunch of information about a
        planet at a given date/time.

        Parameters:
        planet    - Integer that maps to a planet in the SwissEph constants.
        dt        - datetime.datetime object that represents the date and time
                    for which the info is requested.  This object must 
                    have the tzinfo attribute defined and it must created 
                    from pytz.
        
        Returns:
        A PlanetaryInfo object for the given timestamp.
        It has all fields populated.  The timestamp in the PlanetaryInfo 
        object returned is the same timestamp passed into this function.
        See the class description for PlanetaryInfo for details on 
        all the fields available.
        """

        debugStr = "Entered getPlanetaryInfo(planet={}, datetime={}"
        planetName = Ephemeris.getPlanetNameForId(planet)
        Ephemeris.log.debug(debugStr.format(planetName, dt))

        # Convert time to Julian Day.
        jd = Ephemeris.datetimeToJulianDay(dt)
        
        # Geocentric, Tropical, Ecliptical info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Geocentric, Tropical, Equatorial info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Geocentric, Tropical, Rectangular info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        geocentricTropicalDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Geocentric, Sidereal, Ecliptical info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Geocentric, Sidereal, Equatorial info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Geocentric, Sidereal, Rectangular info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        geocentricSiderealDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}


        # Topocentric, Tropical, Ecliptical info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Topocentric, Tropical, Equatorial info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Topocentric, Tropical, Rectangular info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        topocentricTropicalDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Topocentric, Sidereal, Ecliptical info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Topocentric, Sidereal, Equatorial info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Topocentric, Sidereal, Rectangular info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        topocentricSiderealDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Heliocentric, Tropical, Ecliptical info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Heliocentric, Tropical, Equatorial info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Heliocentric, Tropical, Rectangular info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        heliocentricTropicalDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Heliocentric, Sidereal, Ecliptical info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Heliocentric, Sidereal, Equatorial info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Heliocentric, Sidereal, Rectangular info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planet, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        heliocentricSiderealDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Dictionary holding all the geocentric information.
        geocentricDict = {'tropical': geocentricTropicalDict,
                          'sidereal': geocentricSiderealDict}

        # Dictionary holding all the topocentric information.
        topocentricDict = {'tropical': topocentricTropicalDict,
                           'sidereal': topocentricSiderealDict}

        # Dictionary holding all the heliocentric information.
        heliocentricDict = {'tropical': heliocentricTropicalDict,
                            'sidereal': heliocentricSiderealDict}

        # Dictionary holding everything about the planet at the 
        # timestamp given.
        planetaryInfo = PlanetaryInfo(planetName,
                                      planet,
                                      dt,
                                      jd,
                                      geocentricDict,
                                      topocentricDict,
                                      heliocentricDict)

        debugStr = "Leaving getPlanetaryInfo(planet={}, datetime={}"
        Ephemeris.log.debug(debugStr.format(planetName, dt))

        return planetaryInfo


    ######################################################################

    @staticmethod
    def getSunPlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about the Sun at
        the given timestamp. 
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getSunPlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.SUN, timestamp)

    @staticmethod
    def getMoonPlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about the Moon at
        the given timestamp. 
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getMoonPlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.MOON, timestamp)

    @staticmethod
    def getMercuryPlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the Mercury at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getMercuryPlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.MERCURY, timestamp)

    @staticmethod
    def getVenusPlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the Venus at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getVenusPlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.VENUS, timestamp)

    @staticmethod
    def getMarsPlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the Mars at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getMarsPlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.MARS, timestamp)

    @staticmethod
    def getJupiterPlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the Jupiter at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getJupiterPlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.JUPITER, timestamp)

    @staticmethod
    def getSaturnPlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the Saturn at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getSaturnPlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.SATURN, timestamp)

    @staticmethod
    def getUranusPlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the Uranus at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getUranusPlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.URANUS, timestamp)

    @staticmethod
    def getNeptunePlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the Neptune at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getNeptunePlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.NEPTUNE, timestamp)

    @staticmethod
    def getPlutoPlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the Pluto at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getPlutoPlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.PLUTO, timestamp)

    @staticmethod
    def getMeanNorthNodePlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the MeanNorthNode at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getMeanNorthNodePlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.MEAN_NODE, timestamp)

    @staticmethod
    def getTrueNorthNodePlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the TrueNorthNode at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getTrueNorthNodePlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.TRUE_NODE, timestamp)

    @staticmethod
    def getMeanLunarApogeePlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the MeanLunarApogee at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getMeanLunarApogeePlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.MEAN_APOG, timestamp)

    @staticmethod
    def getOsculatingLunarApogeePlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the OsculatingLunarApogee at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getOsculatingLunarApogeePlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.OSCU_APOG, timestamp)

    @staticmethod
    def getInterpolatedLunarApogeePlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the InterpolatedLunarApogee at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getInterpolatedLunarApogeePlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.INTP_APOG, timestamp)

    @staticmethod
    def getInterpolatedLunarPerigeePlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the InterpolatedLunarPerigee at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getInterpolatedLunarPerigeePlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.INTP_PERG, timestamp)

    @staticmethod
    def getEarthPlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the Earth at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getEarthPlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.EARTH, timestamp)

    @staticmethod
    def getChironPlanetaryInfo(timestamp):
        """Returns a Python dictionary containing information about
        the Chiron at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        Ephemeris.log.debug("getChironPlanetaryInfo({})".\
                            format(timestamp))

        return Ephemeris.getPlanetaryInfo(swe.CHIRON, timestamp)



# For debugging the Ephemeris class during development.  
if __name__=="__main__":
    # Exercising the PlanetaryInfo and Ephemeris classes.
    print("------------------------")

    # Initialize Logging for the Ephemeris class (required).
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Initialize Ephemeris (required).
    Ephemeris.initialize()

    # Set the Location (required).
    Ephemeris.setGeographicPosition(-77.084444, 38.890277)

    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(eastern)
    print("now is: {}".format(now))

    # Get planetary info for all the planets, and print out the info.
    p = Ephemeris.getSunPlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMoonPlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMercuryPlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getVenusPlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMarsPlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getJupiterPlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getSaturnPlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getUranusPlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getNeptunePlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getPlutoPlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMeanNorthNodePlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getTrueNorthNodePlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMeanLunarApogeePlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getOsculatingLunarApogeePlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getEarthPlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getChironPlanetaryInfo(now)
    print("At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))

    print("------------------------")

    # Pick out the tropical longitude.
    longitude = p.geocentric['tropical']['longitude']
    print("At {}, the Geocentric Tropical Longitude of {} is: {}".\
            format(now, p.name, longitude))

    print("------------------------")

    print("Showing how we lose about a second of precision " + \
          "converting between datetime and julian day:")

    print("now is: {}".format(now))

    jd = Ephemeris.datetimeToJulianDay(now)
    print("now to jd is: {}".format(jd))

    dt = Ephemeris.julianDayToDatetime(jd, eastern)
    print("jd back to eastern datetime is: {}".format(dt))

    amsterdam = pytz.timezone('Europe/Amsterdam')
    dt = Ephemeris.julianDayToDatetime(jd, amsterdam)
    print("jd to asterdam datetime is: {}".format(dt))
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    print("jd to asterdam datetime formatted is: {}".\
          format(dt.strftime(fmt)))


    dt = Ephemeris.julianDayToDatetime(jd, pytz.utc)
    print("jd to UTC datetime (explicit) is: {}".format(dt))

    dt = Ephemeris.julianDayToDatetime(jd)
    print("jd to UTC datetime (implicit) is: {}".format(dt))

    print("------------------------")

    # Close the Ephemeris so it can do necessary cleanups.
    Ephemeris.closeEphemeris()

    # Shutdown logging so all the file handles get flushed and 
    # cleanup can happen.
    logging.shutdown()

    print("Exiting.")




