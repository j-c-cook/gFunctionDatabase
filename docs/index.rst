.. gFunctionLibraryDocumentation documentation master file, created by
   sphinx-quickstart on Tue Feb  2 18:41:02 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

###############################
gFunctionDatabase Documentation
###############################

************
Introduction
************

Installation
============

The source code for this project can be found on github at https://github.com/j-c-cook/gFunctionDatabase.

The `gFunctionDatabase <https://pypi.org/project/gFunctionDatabase/>`_ package has been uploaded to
`PyPi <https://pypi.org>`_. Install the library via pip:

.. code-block:: none

   pip install gFunctionDatabase

As long as you are connected to the internet, pip will download and install the package directly from
PyPi. If you would like to install a specific version, then you need to specify. For example, if you
would like to install version 0.2, then the following command is needed:

.. code-block:: none

   pip install gFunctionDatabase==0.2

Background
===========

Thermal response functions, known as g-functions, are commonly used to simulate
grount heat exchangers used with ground-source heat pump systems. G-functions
were originally developed by Prof. Johan Claesson and his graduate students at
the University of Lund in Sweden. (:cite:label:`Claesson_Eskilson_1987`,
:cite:label:`Eskilson_1988`, :cite:label:`Hellstrom_1991`) G-functions are used
by ground heat exchanger design tools (:cite:label:`Spitler_2000`,
:cite:label:`BLOCON_2015`, :cite:label:`BLOCON_2017`) and whole building energy
simulation tools (:cite:label:`Liu_2006`, :cite:label:`Mitchell_2020`).
G-functions are unique to a specific borehole configuration (geometry e.g. 5
rows of 10 boreholes spaced 5m apart) and depth.

Calculation of g-functions can be quite computationally time-consuming,
particularly for configurations containing a large number of boreholes. However,
once the g-function is computed, the actual simulation time can be quite short,
particularly if a hybrid time step (:cite:label:`Cullin_2011`) approach is used.
Because of this, pre-computed g-function libraries are commonly used in design
tools and building simulation tools. In practice, the g-functions are
pre-calculated for specific configurations; for each configuration multiple
depths are pre-computer for interpolation purposes. Then, a design tool, can
iteratively adjust the depth to find the correct-sized ground heat exchanger.
Furthermore, the g-functions scale with several non-dimensional parameters that
allow wider application than the specific horizontal spacing and depths used in
the pre-calculation.

Currently, available libraries, implemented in eQuest (:cite:label:`Liu_2006`,
GLHEPRO :cite:label:`Spitler_2000`, EED :cite:label:`BLOCON_2015`) have less
than 1000 possible configurations and are proprietary. This documentation for
the g-function database gives a description of a new publicly available library
containing g-functions for 34,321 configurations at 5 depths. Some of the
configurations are available in existing libraries; others are new. The new
configurations are C-shapes, lopsided-U-shapes and zoned rectangles (
:cite:label:`Cook_Spitler_2021`).

Calculation methodology
=======================

This section breifly describes the procedure used to calculate the g-functions.
The g-functions are calculated with a tool that we call "cpgfunction"
:cite:`Cook_Spitler_2021`. It is based on the semi-anlytical finite line source
methodology developed by Cimmino [:cite:label:`Cimmino_2018`,
:cite:label:`Cimmino_2018b`] for an open-source tool written in Python, called
pygfunction. Cpgfunction is written in C++. Cpgfunction was developed with an
eye towards reducing memory consumption, which can be quite high for large
numbers of boreholes, exceeding 96 GB in many cases. For calculating large
numbers of g-functions, as was done here, the memory requirements can become
critical when running on a cluster. Keeping the memory requirements below
96 GB allowed us to fully use the most common compute nodes on the Oklahoma
State High Performance Computing Cluster :cite:`OSUHPCC`. The time requirement
also improved for most cases, but large number of regularly spaced boreholes
the computation times are similar. For further information on cpgfunction, see
Cook and Spitler (2021).

The g-functions are calculated using the uniform borehole wall temperature
(UBHWT) boundary condition. That is, the heat input at each segment is adjusted
to give uniform (but changiing with time) temperature at the borehole walls.
This is the method commonly used to develop other g-function libraries and has
been used to size ground heat exchangers for commercial systems for the last
30 years.

Database contents
================

The database contains configurations and methods to access and use g-functions.

********************
Modules and examples
********************

.. toctree::
   :maxdepth: 2

   modules
   examples

**********************
Libraries and examples
**********************

.. toctree::
   :maxdepth: 2

   libraries
   lib_examples

************
Bibliography
************

.. bibliography:: references.bib
    :cited:
    :style: unsrt
