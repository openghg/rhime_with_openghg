# *****************************************************************************
# About
# Different functions for retrieving appropriate datasets for forward 
# simulations
# 
# Current options include:
# - "data_processing_surface_notracer": Surface based measurements, without tracers
# - "data_processing_surface_tracer"  : Surface based measurements, with tracers
#
# *****************************************************************************

import os
import sys
import shutil
import numpy as np
import pandas as pd
import pickle

import rhime_with_openghg.rhime.inversionsetup as setup

from openghg.retrieve import get_obs_surface, get_flux
from openghg.retrieve import get_bc, get_footprint
from openghg.analyse import ModelScenario
from openghg.dataobjects import BoundaryConditionsData

def data_processing_surface_notracer(species, sites, domain, averaging_period, start_date, end_date,
                                     obs_data_level, inlet = None, instrument = None, calibration_scale = None, 
                                     met_model = None, fp_model = "NAME", fp_height = None,
                                     emissions_name = None, 
                                     use_bc = True, bc_input = None,
                                     bc_store = None, obs_store = None, footprint_store = None, emissions_store = None,
                                     averagingerror = True, save_merged_data = False,
                                     merged_data_name = None, merged_data_dir = None):

    """
    Retrieve and prepare fixed-surface datasets from
    specified OpenGHG object stores for forward 
    simulations that do not use atmospheric tracers
    ---------------------------------------------
    Args:
        species (str):
            Atmospheric trace gas species of interest
            e.g. "co2"
        sites (list/str):
            List of strings containing measurement
            station/site abbreviations 
            e.g. ["MHD", "TAC"]
        domain (str):
            Model domain region of interest
            e.g. "EUROPE"
        averaging_period (list/str):
            List of averaging periods to apply to 
            mole fraction data. NB. len(averaging_period) == len(sites)
            e.g. ["1H", "1H"]
        start_date (str):
            Date from which to gather data
            e.g. "2020-01-01"
        end_date (str):
            Date until which to gather data
            e.g. "2020-02-01"
        obs_data_level (list/str):
            ICOS observations data level. For non-ICOS sites
            use "None"
        inlet (list/str/opt):
            Specific inlet height for the site observations 
            (length must match number of sites)
        instrument (list/str/opt):
            Specific instrument for the site 
            (length must match number of sites) 
        calibration_scale (str):
            Convert measurements to defined calibration scale 
        met_model (str/opt):
            Meteorological model used in the LPDM
        fp_model (str):
            LPDM used for generating footprints
        fp_height (list/str):
            Inlet height used in footprints for corresponding sites
        emissions_name (list):
            List of keywords args associated with emissions files
            in the object store
        use_bc (bool, default=True):
            Use boundary conditions data in model
            Defaults to True
        bc_input (str):
            Specify boundary conditions source term
        bc_store (str):
            Name of object store to retrieve boundary conditions data from
        obs_store (str):
            Name of object store to retrieve observations data from
        footprint_store (str):
            Name of object store to retrieve footprints data from
        emissions_store (str):
            Name of object store to retrieve emissions data from
        averagingerror (bool/opt, default=True): 
          Adds the variability in the averaging period to the measurement
          error if set to True.
       save_merged_data (bool/opt, default=False):
          Save forward simulations data and observations 
       merged_data_name (str/opt):
          Filename for saved forward simulations data and observations
       merged_data_dir (str/opt):
          Directory path for for saved forward simulations data and observations
    """

    for i, site in enumerate(sites): sites[i]=site.upper()

    # Convert "None" args to list
    nsites = len(sites)
    if inlet == None:
        inlet = [None] * nsites
    if instrument == None:
        instrument = [None] * nsites
    if fp_height == None:
        fp_height = [None] * nsites
    if obs_data_level == None:
        obs_data_level = [None] * nsites


    fp_all = {}
    fp_all[".species"] = species.upper()

    # Get fluxes
    flux_dict = {}
    for source in emissions_name:
        get_flux_data = get_flux(species = species,
                                 domain = domain,
                                 source = source,
                                 start_date = start_date,
                                 end_date = end_date,
                                 store = emissions_store)

        flux_dict[source] = get_flux_data
    fp_all[".flux"] = flux_dict

    footprint_dict = {}
    scales = {}
    check_scales = []

    for i, site in enumerate(sites):
        # Get observations
        site_data = get_obs_surface(site = site,
                                    species = species.lower(),
                                    inlet = inlet[i],
                                    start_date = start_date,
                                    end_date = end_date,
                                    icos_data_level = obs_data_level[i], # NB. May need to update if variable name changes
                                    average = averaging_period[i],
                                    instrument = instrument[i],
                                    calibration_scale = calibration_scale,
                                    store = obs_store)

        unit = float(site_data[site].mf.units)

        # Get footprints
        get_fps = get_footprint(site = site,
                                height = fp_height[i],
                                domain = domain,
                                model = fp_model,
                                start_date = start_date,
                                end_date = end_date,
                                store = footprint_store)
        footprint_dict[site] = get_fps


        if use_bc == True:
            # Get boundary conditions
            get_bc_data = get_bc(species = species,
                                 domain = domain,
                                 bc_input = bc_input,
                                 start_date = start_date,
                                 end_date = end_date,
                                 store = bc_store)


            # Divide by trace gas species units
            # See if R+G can include this 'behind the scenes'
            get_bc_data.data.vmr_n.values = get_bc_data.data.vmr_n.values/unit
            get_bc_data.data.vmr_e.values = get_bc_data.data.vmr_e.values/unit
            get_bc_data.data.vmr_s.values = get_bc_data.data.vmr_s.values/unit
            get_bc_data.data.vmr_w.values = get_bc_data.data.vmr_w.values/unit
            my_bc = BoundaryConditionsData(get_bc_data.data.transpose("height", "lat", "lon", "time"),
                                           get_bc_data.metadata)
            fp_all[".bc"] = my_bc

        elif use_bc == False:
            my_bc = None
            fp_all[".bc"] = None


        # Create ModelScenario object for all emissions_sectors
        # and combine into one object
        model_scenario = ModelScenario(site = site,
                                       species = species,
                                       inlet = inlet[i],
                                       start_date = start_date,
                                       end_date = end_date,
                                       obs = site_data,
                                       footprint = footprint_dict[site],
                                       flux = flux_dict,
                                       bc = my_bc)

        if len(emissions_name) == 1:
            scenario_combined = model_scenario.footprints_data_merge()

            if use_bc:
                scenario_combined.bc_mod.values = scenario_combined.bc_mod.values * unit

        elif len(emissions_name) > 1:
            # Create model scenario object for each flux sector
            model_scenario_dict = {}
 
            for source in emissions_name:
                scenario_sector = model_scenario.footprints_data_merge(sources = source, recalculate = True)

                if species.lower() == "co2":
                    model_scenario_dict["mf_mod_high_res_"+source] = scenario_sector["mf_mod_high_res"]  
                elif species.lower() != "co2":
                    model_scenario_dict["mf_mod_"+source] = scenario_sector["mf_mod"]   
    
            scenario_combined = model_scenario.footprints_data_merge(recalculate = True)

            for key in model_scenario_dict.keys():
                scenario_combined[key] = model_scenario_dict[key]
            
            if use_bc:
                scenario_combined.bc_mod.values = scenario_combined.bc_mod.values * unit

        fp_all[site] = scenario_combined


        # Check consistency of measurement scales between sites
        # Could possibly remove this 
        check_scales += [scenario_combined.scale]
        if not all (s == check_scales[0] for s in check_scales):
            rt = []
            for i in check_scales:
                if isinstance(i, list): rt.extend(flatten(i))
            else:
                rt.append(i)
            scales[site] = rt
        else:
            scales[site] = check_scales[0]

    fp_all[".scales"] = scales
    fp_all[".units"] = float(scenario_combined.mf.units)

    # If site contains measurement errors given as repeatability and variability,
    # use variability to replace missing repeatability values, then drop variability
    for site in sites:
        if "mf_variability" in fp_all[site] and "mf_repeatability" in fp_all[site]:
            fp_all[site]["mf_repeatability"][np.isnan(fp_all[site]["mf_repeatability"])] = \
                fp_all[site]["mf_variability"][np.logical_and(np.isfinite(fp_all[site]["mf_variability"]),np.isnan(fp_all[site]["mf_repeatability"]) )]
            fp_all[site] = fp_all[site].drop_vars("mf_variability")

    # Add measurement variability in averaging period to measurement error
    if averagingerror:
        fp_all = setup.addaveragingerror(fp_all,
                                         sites,
                                         species,
                                         start_date,
                                         end_date,
                                         averaging_period,
                                         inlet = inlet,
                                         instrument = instrument)
    
    # Save output data as a pickle    
    if save_merged_data == True:
        merged_data_name_full = f"{species}_{start_date}_{merged_data_name}_merged-data.pickle"
        fp_out = open(merged_data_dir+merged_data_name, "wb")
        pickle.dump(fp_all, fp_out)
        fp_out.close()
 
        print(f"\nfp_all saved in {merged_data_dir}\n")

    return fp_all
