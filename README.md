# c-backporter
Objective: Develop a small, efficient Python-based solution for backporting changes from the recently updated C file to the old one.

## How to Run:
### Running Locally: 

1. Ensure that `diffutils` and `patch` are installed locally. 
    > On `Linux` and `Mac`, they should be installed already, but if not, you can install them using `apt-get` or `brew`
2. Install all the pip packages:

    `pip install -r requirements.txt`
3. Run the application, providing the required files:

    `python run.py [-h] [--outputdir OUTPUTDIR] before_file after_file target_file`

For example, you can run it on sample files in the `data` directory by running:
    `python run.py data/before.c data/after.c data/target.c -o data`

### Run Docker image
1. Pull the latest version of the image ([dfreilich/backporter](https://hub.docker.com/repository/docker/dfreilich/backporter/general)) from Dockerhub:

    `$ docker pull dfreilich/backporter`
2. Prepare a directory with 3 required files: `before.c`, `after.c`, and `target.c` (alternatively, you can override the run command and provide different files, but that is the simplest method)
3. Run the image, mounting the directory to the `/data` directory in the docker container:

    `$ docker run -v $(pwd)/data:/data dfreilich/backporter`

### Understanding the Results
Upon running the tool, you should notice a few additional files:
1. `result.c` &rarr; This file is the result of backporting the patches to the target file
2. `patch_log.txt` &rarr; This file contains the log of patches, letting you know what file was patched, and around which lines were patched (Note: This can have slightly imprecise line counts, depending on OS and how complex the file is, but it should be fairly close to the patched section)
3. `result.c.orig`/`result.c.rej` &rarr; These files will only be created in the event of a merge conflict, where it was unable to auto-merge a patch. The `*.rej` file will contain details about the failed section, and the `.orig` file is how it was originally, so you can merge it by hand.
4. `patch.diff` &rarr; If you are running this by running the project directly (and not via the docker image), you may also see `patch.diff`. This is the result of the diff between the `before` and `after` file.

## Scope:
* Language & Tools: Python, with permissible use of common external tools compatible with Ubuntu or other Linux OSes.
* Format: Proof-of-concept. Focus on functionality and efficiency rather than extensive development time.

## Task Description:
### Script Functionality:
Input: Accept three .c files as arguments (before, after, target) from the Command Line Interface (CLI). 
* before – the original file before the patch,
* after – a patched version
* target – an old version of the same file to apply patch to.

### Primary Task:
* Find the difference (diff) between the “before” and “after” files called the “patch”.
* Attempt to apply the patch to the third “target” .c file. This process is known as "backporting".

### Handling Merge Conflicts:
* The script should recognize potential merge conflicts during backporting.
* The script should automatically apply as many hunks from the patch as possible.
* For hunks with merge conflicts, leave those parts of the file unchanged.
* Log details about which hunks were successfully applied and which had conflicts.
* Conflicts should be identified in the log by stating the start and end lines of the conflicted hunks in the resultant file.

### Output:

* A resulting .c file with all or partially applied hunks, named “result.c”.
* A log file detailing the applied hunks and merge conflicts.

## Project Delivery:

* The solution must be provided as a deployable project.
* Include all prerequisites for deployment and running the tool locally.
* A recorded demo showcasing usage and explanation is highly encouraged.

## Evaluation Criteria:
* Efficiency in identifying and applying changes.
* Accuracy in handling merge conflicts.
* Clarity and usability of the output files (resultant file and log).
* Ease of deployment and usage.


This task aims to test the candidate's proficiency in Python, understanding of file manipulation, and approach to problem-solving in a real-world scenario. The candidate is encouraged to demonstrate creativity and efficiency in their solution.