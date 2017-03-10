import wave
import pigpio

I2C_ADDR=0x13

# Read wav file
refWave = wave.open("Ref8000.wav")

# setup i2c
pi=pigpio.pi()
h = pi.i2c_open(1, I2C_ADDR)

# start sending through i2c
for x in range(0,refWave.getnframes()):
	pi.i2c_write_device(h,refWave.readframes(1))

pi.i2c_close(h) 
