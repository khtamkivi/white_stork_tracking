# Tracking the white storks

![alt text](https://flightforsurvival.org/wp-content/uploads/2020/09/White-Stork-cDave-Walker_Birdlife-Cyprus_August-2020-scaled.jpg)

This repository holds data and notebooks about a data science project done on white stork tracking data from 1991-2017. The data originates from a Movebank repository: https://www.movebank.org/cms/webapp?gwt_fragment=page=studies,path=study7431347

The GPS tracking data is complemented with average annual land surface temperature data from Berkeley Earth: https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_complete.txt

The notebooks aim to answer a seemingly simple question - has the global land surface temperature rise and climate warming had an effect on white stork migration behaviour over the years?

Answering this question requires extensive tracking data cleaning, migration period labelling, migration behaviour statistics, migration path clustering and in the end a rather short correlation analysis. The repository also holds a dashboard.py file that allows the user to visualise the migration paths of different individuals.

In order to run all of the files without any additional package installations or version conflicts, run the following command in your terminal (while being in the git directory):

conda env create -f environment.yml

and activate it with:

conda activate storks

```
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```
