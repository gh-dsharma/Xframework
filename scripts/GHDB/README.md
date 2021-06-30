## What the script does:

* Creates new FlowcellID based on existing FlowcellID by using the user input `-in_FCID` as a reference to create the new FlowcellID and samples.
* The script takes an optional parameter `--out_FCID` to create the FlowcellID as per the user.
  * If the parameter is not set, the script will generate a FlowcellID.
* The script takes an optional parameter `--samples` to limit the number of generated samples associated with the new FlowcellID. 
  * If the parameter is not set, the script will generate as many samples as the input FlowcellID.
  * If the number of requested samples exceedes the number of samples available in the input FlowcellID, the request is rejected.
* The script takes an optional parameter `--file` to allow a CSV file to represent the mapping between input samples and output samples. This allows the user to model the output samples based on known input samples.
  * The CSV file has two columns: in_sample and out_sample.
  * Each row will model a sample from the `-in_FCID` to the `--out_FCID`.
  * If an `in_sample` has a value, the script will check to see if it's associated with the `-in_FCID`. If the check fails the script will exit.
    * If an `in_sample` is `<EMPTY>`, the script will use the `nth` record returned by the query and use the `out_value` to create a new sample and associate it with the `--out_FCID`.
  * The script will use the `out_value` to create a new sample and associate it with the `--out_FCID`
    * If the `out_value` is `<EMPTY>`, the script will generate a new sample ID and associate it with the `--out_FCID`.
* The script takes an optional parameter `--commit` to write the new Flowcell and associate output samples to the database. If this parameter is not set the script will only generate the log.


__Note__: If the user passes both the `--samples` and `--file` parameter. The script will use the `--file` over the `--sample` parameter.

## How to use the script:

* Clone this repo
* Navigate to the `GHDB` folder
* Optionally create a virtual environment: `python3 -m venv .venv` and activate it `source .venv/bin/activate`
* Install requirements: `pip3 install -r requirements.txt`
* Update the `.env` file with the proper credentials for the database you want to target
* Examples:

`python3 ghdb_create.py -in_FCID '150911_NB501022_0013_AHJ33JBGXX'`

Executing the script above will take the `-in_FCID` and look for it in the database. It checks to see if there are one or more samples associated with it. It generates a new FlowcellID and all samples associated with it.

`python3 ghdb_create.py -in_FCID '150911_NB501022_0013_AHJ33JBGXX' --out_FCID 'VGTEST_D00560_0531_AAAAB0ZZZZ'`

Executing the script above will take the `-in_FCID` and look for it in the database. It checks to see if there are one or more
samples associated with it. It checks that the `--out_FCID` does not exist, and if true, it creates it and generates as many samples
as the `-in_FCID` and associates them with the `--out_FCID`. If the `--out_FCID` already exists, the script will exit.

`python3 ghdb_create.py -in_FCID '150911_NB501022_0013_AHJ33JBGXX' --out_FCID 'VGTEST_D00560_0531_AAAAB0ZZZZ' --samples 5`

Executing the script above will take the `-in_FCID` and look for it in the database. It checks to see if the the number of samples
associated with it is equal or greater to the `--samples` value. It checks that the `--out_FCID` does not exist, and if true, it creates it
and generates as many samples as specified by the `--samples` parameter and associates them with the `--out_FCID`. If the `--out_FCID` already exists, the script will exit.

`python3 ghdb_create.py -in_FCID '150911_NB501022_0013_AHJ33JBGXX' --out_FCID 'VGTEST_D00560_0531_AAAAB0ZZZZ' --file 'test.csv'`

Executing the script above will take the `-in_FCID` and look for it in the database. It checks to see if the the number of samples
associated with it is equal or greater to the number of samples listed in the CSV file. It checks that the `--out_FCID` does not exist, and if true, it creates it and generates/creates as many samples as specified by the CSV file and associates them with the `--out_FCID`.
If the `--out_FCID` already exists, the script will exit.


## Remember: 
Use the `--commit` parameter when you're ready to write to the database!