import wave
import pigpio

I2C_ADDR=0x13

def i2c(id, tick):
    global pi
	global wavFile

    s, b, d = pi.bsc_i2c(I2C_ADDR)
	if b == 2:
		wavFile.writeframes(d)
    elif b:
		print("file closed")
		wavFile.close()
        if d[0] == ord('t'): # 116 send 'HH:MM:SS*'

            print("sent={} FR={} received={} [{}]".
               format(s>>16, s&0xfff,b,d))

            s, b, d = pi.bsc_i2c(I2C_ADDR,
               "{}*".format(time.asctime()[11:19]))

        elif d[0] == ord('d'): # 100 send 'Sun Oct 30*'

            print("sent={} FR={} received={} [{}]".
               format(s>>16, s&0xfff,b,d))

            s, b, d = pi.bsc_i2c(I2C_ADDR,
               "{}*".format(time.asctime()[:10]))

pi = pigpio.pi()
wavFile = wave.open("Ref8000_I2C.wav",'w')
wavFile.setnchannels(1)
wavFile.setsampwidth(2)
wavFile.setframerate(8000)

if not pi.connected:
    exit()

# Respond to BSC slave activity

e = pi.event_callback(pigpio.EVENT_BSC, i2c)

pi.bsc_i2c(I2C_ADDR) # Configure BSC as I2C slave

time.sleep(600)

e.cancel()

pi.bsc_i2c(0) # Disable BSC peripheral

pi.stop()