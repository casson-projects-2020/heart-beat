import Adafruit_ADS1x15
import time
import subprocess

#sensor = Adafruit_ADS1x15.ADS1115()

lasttime = int( time.time() * 1000 )

w = 100
h = 21
interval = 6000 #in ms

# rolling average
ravg = 12000
_ravg = [ ravg / w for i in range( w )]
rpos = 0

# max
max = 13000

# to print the ascii-art graph of heartbeating
tela = [ ' ' for i in range( w )]
tela[ w - 1 ] = '|'

tela = [ tela.copy() for i in range( h )]
tpos = 0

# values in the sample interval
sample = []
elapsed = 0

dot = '*'

while True:
    # read from the sensor (channel 0)
    #inpval = sensor.read_adc( 0, gain=1 )
    inpval = 22000

    # update rolling average
    ravg -= _ravg[ rpos ]
    _ravg[ rpos ] = inpval / w
    ravg += _ravg[ rpos ]
    rpos += 1
    if rpos >= w:
        rpos = 0

    if max < inpval:
        max = inpval

    # update the values in the sample interval
    sample.append( inpval )

    currtime = int( time.time() * 1000 )
    elapsed += currtime - lasttime

    # plot the point if we are in the screen update time
    if elapsed > ( interval / w ):
        pp = max / h

        pos = sum( sample ) / len( sample )
        sample = []

        pos = int( pos / pp )
        if pos > h:
            pos = h

        for i in range( h ):
            tela[ i ][ tpos ] = ' '

        tela[int( h / 2 )][ tpos ] = '_'

        tela[( h - pos )][ tpos ] = dot

        tpos += 1
        if tpos >= w:
            tpos = 0

        sout = '-'.join( pixel for row in tela for pixel in row )
        sout = sout.replace( '-', '' )
        sout += 'elapsed: ' + str( elapsed )
        elapsed = 0

        print( sout, end='\r' ) #end='\x1b[1K\r' )


    lasttime = currtime
