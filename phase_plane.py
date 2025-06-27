import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import rioxarray as rio
import geopandas as gpd
import glob

##########################

# reading the file that contains vertically integrated MSE (daily averaged), and domain mean 

# the file contains some repeated time steps, so making sure that the unique time steps are only saved.
h = ds.h.sel(valid_time=ds["valid_time"].dt.month.isin([6, 7, 8,9]))

# calculating MSE tendency
dh_dt = h.differentiate("valid_time")*1e9 #this function calculates in nano seconds, it need to be multiplied by 10^9

# selecting only july and august for this study
h_sliced = h.sel(valid_time=h["valid_time"].dt.month.isin([7, 8]))
dhdt_sliced = dh_dt.sel(valid_time=h["valid_time"].dt.month.isin([7, 8]))

# defining a function for creating the simplest quiver plot (phase plane diagram for MSE)
def phase_plot (a,b, color, title) :    
    plt.figure(figsize = (6,6))

    # a - MSE
    # b - MSE tendency

    # we need to make sure that da/dt and db/dt are nearly of the same order, and they determine the magnitude of the length of the arrow
    da_dt = a.differentiate("valid_time")*1e9 # this makes sure that the units of the data remains conserved
    db_dt = np.gradient(b) #the array b already has the units of JOules/(Kg*s), calculating simple gradient is enough.

    # size and width of the arrows and the arrowheads can be adjusted manually, by adding more specification, for now we keeping it simple.
    plt.quiver(a.values, b.values, da_dt, db_dt,
               color=color)
    #plt.scatter(a, b, color = "red", label = "data points")
    plt.title(title, fontweight="bold", fontsize=13)
    plt.xlabel("Moist Staic Energy (MSE)",fontsize=10, fontweight ="bold")
    plt.ylabel("MSE tendency",fontsize=10, fontweight="bold")
    
    plt.tick_params(axis='y',labelsize=8) 

    plt.tick_params(axis='x', labelsize=8)
    
    plt.axhline(0, color="black", linewidth=1.5, linestyle="--")  # Bold y=0 line
    plt.grid()
    #plt.savefig(file_dest_name)

phase_plot (h_sliced, dhdt_sliced,   "red", "Phase plane")
