<img src="https://github.com/openghg/logo/raw/main/OpenGHG_Logo_Landscape.png" height="150"> <img src="https://cdn.freebiesupply.com/logos/thumbs/2x/university-of-bristol-logo.png" height="150">

# RHIME-with-OpenGHG
----
## Welcome 
Hello and welcome to the RHIME-with-OpenGHG repository. Here, we present and document the RHIME inverse model as developed by the University of Bristol. RHIME, previously referred to as "Brisol-MCMC" or "HBMCMC", was previously kept in the "openghg_inversions" repository. But that code has recently had a bit of an overhaul and a bit of a re-brand so we felt a new repository seemed fitting! 

After months of development, we finally have a stable version of RHIME-with-OpenGHG available to be used for all your atmospheric inverse modelling needs. Please see below for instructions on installation and setup. Have fun!


## What is RHIME?
RHIME (Regional Hierarchical Inverse Modelling Environment; [Ganesan et al. 2014](https://acp.copernicus.org/articles/14/3855/2014/)) is a hierarchical Bayesian inverse model that has been frequently used for trace gase inversions of various atmospheric species. Bayesian inference using a Markov Chain Monte Carlo (MCMC) approach is used to quantify top-down emissions of trace gases at a regional scale. RHIME uses hyperparameters that characterize probability density functions (PDFs) of: the a priori emissions, boundary condition mole fractions, model-data covariances and offset terms. The RHIME framework allows uncertainties in the scaling parameters to be included in the model.

## What is OpenGHG?
[OpenGHG](https://openghg.org) is a platform for greenhouse gas data analysis. RHIME-with-OpenGHG uses the OpenGHG library for processing the necessary data for the inversion. Before diving in with using RHIME-with-OpenGHG, we strongly encourage users to spend some time getting familiar with using OpenGHG. Details on installing and using OpenGHG can be found [here](https://github.com/openghg/openghg), 

----

## Installation and Setup
As RHIME-with-OpenGHG is dependent on OpenGHG, please ensure that when running locally you are using Python 3.8 or later on Linux or MacOS. Please see the [OpenGHG project](https://github.com/openghg/openghg/) for further installation instructions of OpenGHG and setting up an object store.

### Setup a virtual environment

```bash
python -m venv rhime_openghg
```
Next activate the environment

```bash
source rhime_openghg/bin/activate
```

### Installation using `pip`

First you'll need to clone the repository

```bash
git clone https://github.com/openghg/rhime_with_openghg.git
```

Next make sure `pip` and related install tools are up to date and then install RHIME-with-OpenGHG using the editable install flag (`-e`)

```bash
pip install --upgrade pip setuptools wheel
pip install -e rhime_with_openghg
```

### Setup

Once installed, ensure that your OpenGHG object store is configured and that you are comfortable with adding data to your object store. The RHIME inverse model assumes all necessary data required for the inversion run has already been added to the object store.  

----

## Getting Started with RHIME-with-OpenGHG
