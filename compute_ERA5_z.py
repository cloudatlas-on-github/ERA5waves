#Input surface pressure (sp) and column temperature (t)
#Output height in km for whole column
#See https://confluence.ecmwf.int/display/CKB/ERA5%3A+compute+pressure+and+geopotential+on+model+levels%2C+geopotential+height+and+geometric+height
import numpy as np

def compute_ERA5_z(sp,t):
        
    #We assume that humidity and surface geopotential is zero
    q=np.zeros(137)
    zp=0.0
    Rd=287.06
    
    #Load in file with parameters
    #Change path for spiritx to /home/ratlas/python/akbk.csv    
    data=np.loadtxt('/home/ratlas/python/akbk.csv',skiprows=2,delimiter=',')

    ak=np.concatenate(([0.0],data[:,1]))
    bk=np.concatenate(([0.0],data[:,2]))
    
    ERA5_plev=ak[:-1]+bk[:-1]*sp
    ERA5_plevplusone=ak[1:]+bk[1:]*sp
        
    dlog_p=np.zeros(137)
    alpha=np.zeros(137)
        
    dlog_p[0] = np.log(ERA5_plevplusone[0]/ 0.1)
    alpha[0] = np.log(2)
        
    dlog_p[1:] = np.log(ERA5_plevplusone[1:]/ERA5_plev[1:])
    alpha[1:] = 1.-((ERA5_plev[1:]/(ERA5_plevplusone[1:]-ERA5_plev[1:]))*dlog_p[1:])
                
    t=t*(1+0.609133*q)*Rd
    
    z_hs=np.zeros(137)
    
    z_hs[136]=zp
    
    for i in np.arange(1,137):
        dz=t[136-i]*dlog_p[136-i]
        z_hs[136-i]=z_hs[136-i+1]+dz
                    
    return z_hs/(9.8*1e3)
