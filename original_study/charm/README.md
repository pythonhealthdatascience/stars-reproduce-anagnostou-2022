# dynamiC Hospital wARd Management (CHARM)

DOI: 10.17633/rd.brunel.18517892

CHARM is a discrete-event simulation that models dynamic reconfiguration of hospital wards for bed capacity planning facilitating continuation of normal ICU operations and Covid-19 outbreaks.

CHARM is built in Python 3 using [SimPy](https://simpy.readthedocs.io/en/latest/).

## CHARM: How to use

#### Dependencies

simpy 

*Note: simpy version >= 4.0.0*

#### Run CHARM on Ubuntu

1. Install simpy.

     $ pip install simpy
 
2. Download the CHARM code or clone the CHARM repository.
   
3. cd into the CHARM directory.

4. Run the model.

     $ python3 main.py -z ZONES.csv -p ICU_INPUT_PARAMS.csv -c DAILY_ARRIVALS.csv

   *Note: Example input CSV files are in the input directory.*

## CHARM Docker: How to use

#### Dependencies

docker

*Download and install from [here](https://docs.docker.com/get-docker/).*

#### Build and run the CHARM docker image localy

1. Download the CHARM code or clone the CHARM repository.
   
2. cd into the CHARM directory.

3. Build the image.

     $ docker build -t charm .

4. Run the image.

     $ docker run -it -v $PWD/output/:/charm_app/output charm

