
"""
Brianca Washington
1001132562
"""
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
	

def applyShelvingFilter(inName, outName, g, fc) :
    #open wav file
	orig,fs  = sf.read(inName) 
	# book equations
	mu=10**(g/20)
	angle=(2*np.pi*fc/fs)
	gamma=(1-((4/(1+mu))*np.tan(angle/2)))/(1+((4/(1+mu))*np.tan(angle/2)))
	a=(1-gamma)/2
	
	y=np.ones(len(orig))
	u=np.ones(len(orig))
	#setting the 0 values 
	u[0]=a*orig[0]
	y[0]=orig[0]+(mu-1)*u[0]
	
	for i in range(len(orig)):
		u[i]=a*(orig[i] +orig[i-1])+ (gamma*u[i-1])
		y[i]=orig[i]+(mu-1)*u[i]
	# FFT of the filters
	OFFT=abs(np.fft.fft(orig))
	YFFT=abs(np.fft.fft(y))

	# calulate the length , N and max amplitude
	length= round(len(orig)/4)
	N=np.arange(0,length)*(fs/len(orig))
	amp=max(OFFT)+100
	# we only want N/4
	ogl=OFFT[:length]
	flt=YFFT[:length]

	# plot  both ffts
	orgl=plt.subplot(1,2,1)
	orgl.set_title('original signal')
	orgl.plot(N,ogl)
	orgl.set_ylim(0,amp)
	
	fltd=plt.subplot(1,2,2)
	fltd.set_title('filtered signal')
	fltd.plot( N,flt)
	fltd.set_ylim(0,amp)
	plt.show()

    #save file back
	sf.write(outName, y, fs)
##########################  main  ##########################
if __name__ == "__main__" :
    inName = "P_9_2.wav"
    gain = -10  # can be positive or negative
                # WARNING: small positive values can greatly amplify the sounds
    cutoff = 300
    outName = "shelvingOutput.wav"

    applyShelvingFilter(inName, outName, gain, cutoff)
