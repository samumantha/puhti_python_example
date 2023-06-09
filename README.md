# Python Puhti examples

This is an adapted version of [Geocomputing Python Puhti examples](https://github.com/csc-training/geocomputing/tree/master/python/puhti) for Aalto project course workshop in March 2023.

Three different job styles: interactive, serial, and embarrasingly/delightfully/naturally parallel. 
For parallel jobs there are multiple options with different command line / workload manager tools or Python libraries. We'll have a look at using `GNUParallel` and `dask`. 

Interactive:  developing your scripts,  limited test data. 
Computationally more demanding analysis: use Puhti's batch system for requesting the resources and running your scripts. 

## Example case

Calculate NDVI (Normalized Difference Vegetation Index) from the Sentinel2 satellite image's red and near infrared bands. 

Basic idea behind the script is to:

- Find red and near infrared channels of Sentinel L2A products from its `SAFE` folder and open the `jp2` files. -> `readImage`
- Read the data as `numpy` array with `rasterio`, scale the values to reflectance values and calculate NDVI index. -> `calculateNDVI`
- Save output as GeoTiff with `rasterio`. -> `saveImage`

Files:

* The input **ESA Sentinel-2 L2A images** are in JPG2000 format and are already stored in Puhti: `/appl/data/geo/sentinel/s2_example_data/L2A`. Puhti has only these example images, more [Sentinel L2A images are available from CSC Allas](https://docs.csc.fi/data/datasets/spatial-data-in-csc-computing-env/#spatial-data-in-allas).
* The example scripts are in subfolders by job type and used parallel library. Each subfolder has 2 files:
    * A **.py** file for defining the tasks to be done.
    * A batch job **.sh** file for submitting the job to Puhti batch job scheduler (SLURM).

## Let's get started 
### Get example scripts to Puhti

* Log in to Puhti web interface: https://puhti.csc.fi
* Start a `Login node shell`
* Create a folder for yourself:
    * Switch to your projects scratch directory: `cd /scratch/project_200xxxx/` (fill in your project number for x)
    * Create new own folder:`mkdir yyy` (fill in your user name for y)
    * Switch into your own folder: `cd yyy` (fill in your username for y)
    * Get the exercise material by cloning this repository: `git clone https://github.com/samumantha/puhti_python_example`
    * Switch to the directory with example files: `cd puhti_python_example`.
    * Check that we are in the correct place: `pwd` should show something like `/scratch/project_200xxxx/yyy/puhti_python_example`.

## Interactive job

Within an [interactive job](https://docs.csc.fi/computing/running/interactive-usage/) it is possible to edit the script in between test-runs; so this suits best when still writing the script. Usually it is best to use some smaller test dataset for this.

### Visual Studio Code

With Visual Studio Code you can also just run parts of the script.

* Start [Visual Studio Code](https://docs.csc.fi/computing/webinterface/vscode/) in [Puhti web interface](https://docs.csc.fi/computing/webinterface/).
    * Open VSCode start page from front page: Apps -> Visual Studio code
    * Choose settings for VSCode:
        * Project: project_200xxxx
        * Partition: interactive
        * Number of CPU cores: 1
        * Memory: 4 Gb
        * Local disk: 0
        * Time: 2:00:00
        * Modules: geoconda
        * `Launch`
    * Wait a moment -> Connect to Visual studio code
    * VSCode opens up in the browser
* Open folder with exercise files: 
    * File -> Open folder -> `/scratch/project_200xxxx/yyy/geocomputing/python/puhti` -> OK
* Open [serial/single_core_example.py](serial/single_core_example.py). This is basic Python script, which uses a **for loop** for going through all 3 files.  
* Check that needed Python libraries are available in Puhti. If it is not your own script you can see which libraries are used in this script by checking the imports. To check whether those libraries are available: Select all import rows and press `Shift+Enter`. Wait a few seconds. The import commands are run in Terminal (which opens automatically on the bottom of the page). If no error messages are visible, the packages are available. Also other parts of the script can be tested in the same manner (select the code and run with `Shift+Enter`).
* Run the full script: 
    * Exit Python console in Terminal: type `exit()` in the terminal
    * Click green arrow above script (Run Python File in Terminal)
    * Wait, it takes a few minutes for complete. The printouts will appear during the process.
    * Check that there are 3 new GeoTiff files in your outout directory in the Files panel of VSCode.
* Optional, check your results with [QGIS](https://docs.csc.fi/apps/qgis/)

### Jupyter

If you prefer prototyping and testing in a Jupyter Notebook, you can also do that in a similar manner than using Visual Studio Code. Choose **Jupyter** from the Puhti web interface dashboard or the Apps tab in the Puhti webinterface.

### Command line

If you prefer working in the terminal, you can also start an interactive job there by starting a compute node shell directly from Tools tab in Puhti webinterface. Choose settings for the interactive session:
* Project: project_200xxxx
* Number of CPU cores: 1
* Memory: 4 Gb
* Local disk: 0
* Time: 2:00:00

You can also start an [interactive session](https://docs.csc.fi/computing/running/interactive-usage/) by starting a login node shell from Tools tab in Puhti webinterface or by connecting to Puhti via ssh connection with `sinteractive --account project_200xxxx --cores 1 --time 02:00:00 --mem 4G --tmp 0`. Which gives you a compute node shell (you can see "where" you are from your terminal prompt [<username>@puhti-loginXX] -> login node, [<username>@rXXcXX] (XX being some numbers) -> compute node). 

For both of above:

After getting access to the compute node shell, you can load modules and run scripts "like on a normal linux computer", excluding graphical access.
```
module load geoconda
python interactive_example.py /appl/data/geo/sentinel/s2_example_data/L2A
```

## Serial job

For a one core batch job, use the same Python-script as for interactive working. **Latest now, we have to move to the terminal.**

* Open [serial_job/single_core_example.sh](serial_job/serial_batch_job.sh). Where are output and error messages written? How many cores and for how long time are reserved? How much memory? Which partition is used? Which module is used?
* Submit batch job from **login node shell**
```
cd /scratch/project_200xxxx/yyy/puhti_python_example/serial
sbatch single_core_example.sh
``` 
* `sbatch` prints out a job ID, use it to check state and efficiency of the batch job. Did you reserve a good amount of memory?
```
seff [jobid]
```
* Once the job is finished, see output in out.txt and err.txt for any possible errors and other outputs. 
* Check that you have new GeoTiff files in working folder.
* Check the resources used in another way. 
```
sacct -j [jobid] -o JobName,elapsed,TotalCPU,reqmem,maxrss,AllocCPUS
```
	- elapsed – time used by the job
	- TotalCPU – time used by all cores together
	- reqmem – amount of requested memory
	- maxrss – maximum resident set size of all tasks in job.
	- AllocCPUS – how many CPUs were reserved


## Parallel job

In this case the Python code takes care of dividing the work to 3 processes, one for each input file. Python has several packages for code parallelization, here we'll take a look at `dask` (for others, check [Geocomputing multiporcessing example](https://github.com/csc-training/geocomputing/tree/master/python/puhti/03_parallel_multiprocessing) and [Geocomputing joblib example](https://github.com/csc-training/geocomputing/tree/master/python/puhti/03_parallel_joblib) ):

### dask 

`dask` is versatile and has several options for parallelization, this example is for single-node (max 40 cores)- usage, but `dask` can also be used for multi-node jobs. This example uses [delayed functions](https://docs.dask.org/en/latest/delayed.html) from Dask to parallelize the workload. Typically, if a workflow contains a for-loop, it can benefit from delayed. [Dask delayed tutorial](https://tutorial.dask.org/03_dask.delayed.html)

* [parallel_dask/dask_singlenode.sh](parallel_dask/dask_singlenode.sh) batch job file for `dask`.
	* `--ntasks=1` + `--cpus-per-task=3` reserves 3 cores - one for each file
	* `--mem-per-cpu=4G` reserves memory per core

* [parallel_dask/dask_singlenode.py](parallel_dask/dask_singlenode.py)


* Submit the parallel job to Puhti from Puhti login node shell:
```
cd ../parallel_dask
sbatch dask_singlenode.sh
```

* Check with `seff` how much time and resources you used?


## GNU parallel

GNU parallel can help parallelizing a script which otherwise is not parallelized. In this example we want to run the same script on three different inputfiles which we can read into a textfile and use as argument to the parallel tool.

This is similar to array jobs (see [Geocomputing array job example](https://github.com/csc-training/geocomputing/tree/master/python/puhti/02_array)), with the advantage that we do not start and need to monitor multiple jobs.

[gnu_parallel/gnu_parallel_example.sh](gnu_parallel/gnu_parallel_example.sh).
The only difference to serial job is that we do not loop through the directory inside the Python script but let GNU parallel handle that step.

> To get to know how many `cpus-per-task` we need you can use for example `ls /appl/data/geo/sentinel/s2_example_data/L2A | wc -l` to count everything within the data directory before writing the batch job script. 

Submit the gnu_parallel job
```
cd ../gnu_parallel
sbatch gnu_parallel_example.sh
```
* Check with `seff` how much time and resources you used?

## Using Allas

Before using Allas from Puhti we need to load the tools and configure the connection:

`module load allas`
`allas-conf --mode s3cmd`

### from command line

Using `s3cmd`, you can find all commands in bottom of this page: https://s3tools.org/usage

`s3cmd <command>`

### from Python

See `allas_from_python.py` for some examples.

### from Webinterface

https://pouta.csc.fi/dashboard
-> object store -> containers
(might need Pouta access via project?)

### Making things public

You can make single buckets publicly available via the internet, everyone can then access the files within a bucket, such as [todays presentation](https://a3s.fi/2007552_CSC_presentation/Aalto_py_23.html#/). 

## Notes on many small runs

"Too many files" issues are also often encountered with workflows consisting of thousands of small runs. As a general guide, keep the number of files in a single directory well below one thousand, and organize your data into multiple directories. Also, use command `csc-workspaces` to monitor that the total number of files in your projects stays well below the limits. If most of the files are temporary, or there simply is too many of them, using the fast local SSD disks (NVMe) in the I/O nodes can solve the problem. You can pack small files into a bigger archive file with the `tar` command. Most importantly, if there are output files that you do not need, find out how to turn off writing those in the first place.

## Example benchmarks 

These are just to demonstrate the difference between single core sequential vs. some kind of parallelism. Depending on the issue, some library might be faster or slower.

| Example         | Jobs | CPU cores / job | Time (min) | CPU efficiency |
|-----------------|------|-----------------|------------|----------------|
| single core     | 1    | 1               | 02:54      | 86.70%         |
| multiprocessing | 1    | 3               | 01:05      | 92.31%         |
| joblib          | 1    | 3               | 01:12      | 86.57%         |
| dask            | 1    | 3               | 01:01      | 78.46%         |
| array job       | 3    | 1               | 01:03      | 95.16%         |
| GNU parallel    | 1    | 3               | 00:55      | 15.15%         |
