import numpy as np

#Input surface pressure (sp)
#Output pressure in Pa for whole column
#See https://confluence.ecmwf.int/display/CKB/ERA5%3A+compute+pressure+and+geopotential+on+model+levels%2C+geopotential+height+and+geometric+height

def compute_ERA5_pressure(sp):

    #Load in file with parameters
    #Change path for spiritx to /home/ratlas/python/akbk.csv
    data=np.loadtxt('/home/ratlas/python/akbk.csv',skiprows=2,delimiter=',')

    #Read parameters into variables
    ak=np.concatenate(([0.0],data[:,1]))
    bk=np.concatenate(([0.0],data[:,2]))

    #Define pressure array
    ERA5_p=np.zeros(137)

    #Compute pressure level by level
    for j in range(137):
        ERA5_p[j]=.5*(ak[j]+bk[j]*sp)+.5*(ak[j+1]+bk[j+1]*sp)
    return ERA5_p
