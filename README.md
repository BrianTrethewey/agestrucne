# negui

Overview
--------

	Our goal is a front end that incorporates the population
	genetics functions provided by Tiago Antao's python program at
	https://github.com/tiagoantao/AgeStructureNe.git.  

	This project will proceed by iterative implementation, to provide several
	analyses performed by Tiago's code, along with some added analyses.

	 Codewise we have a tkinter-based interface, supported by a class structure,
	essentially a host ttk notebook that brings up interfaces for various analyses.
	These interfaces essentially consist of the GUI itself as a class, which then
	uses non-gui classes that handle the input (as delivered by the interface,
	analysis, and output.   This is seen in the file, preliminary_uml_classes.png (a
	diagram that is sorely in need up updating).  A better look at the current
	structure of the program can be seen via descriptions of classes and
	relationships by loading doxydoc/html/index.html into a browser. 


Current python version
----------------------
	python 2.7


OS-comaptibility
-----------------
	1. Linux. The program has been run on Linux (Ubuntu 16.04).

	2. OSX. The program has been run on OSX (version unknown).

	3. Windows 10 (64-bit) and Windows 7 (32-bit) shows successful runs.  
	   One persistent problem is the inability to remove files for
	   some cleanup operations when processes are user cancelled. See
	   the "BUGS" file for this and other windows-specific issues.

Current dependencies
--------------------
	1.  pygenomics, https://github.com/tiagoantao/pygenomics.git The
	pygenomics python modules should be installed using the supplied
	setup.py, so that they can be imported by your python interpereter.

	
	2.  SimuPOP, http://simupop.sourceforge.net The SimuPOP modules should
	be installed using setup.py (or pip), so that they can be accessed
	by your python interpreter. 

		i. VC++ Library, 2008 (Windows only).  Installation of SimuPOP
		on Windows (10 and 7) did not work without installing the Microsoft VC++
		Redistributable 2008 library, as noted in the SimuPOP installation web page.
		Note that the link on the Simupop installation web page points to the Microsoft
		to the 32-bit libary download-page (unless I missed an option).  Most of us will
		actually need the x64 verion at
		https://www.microsoft.com/en-us/download/details.aspx?id=15336

		ii.  SWIG.  Before python will install simuPOP you'll need the SWIG
		tool at http://www.swig.org/download.html. (This tool makes C and C++ code in
		simuPOP python compatible). You can try to install simuPOP first, and install
		SWIG if you get a message that SWIG is missing.

		iii. Python compiler for Windows. Windows users
		may also need to install the windows python compiler.  Simupop, if it's
		installation fails for lack of this compiler, will give you the correct web
		address from which to download and intall it.

	4.  NeEstimator,
	http://www.molecularfisherieslaboratory.com.au/neestimator-software.
	Our program will look for the executable Ne2L (Linux) Ne2.exe (Windows), Ne2M
	(Mac OSX) in your PATH variable.

Installation.  
------------

While future versions may include setup.py installation into default python
library directories, as of now:

	1. Clone the repository or download the files from
	https://github.com/popgengui/negui

	2. Add the location of the python modules to your PYTHONPATH variable,
	and add negui.py to your PATH: 
		i. Linux/OSX: If you downloaded the
	python files into /home/myname/mydir/negui-master, you can either: 

			a. On starting a new terminal you can make python aware of the
			modules, and add the negui.py to your command path, by typing these two lines: 

				PATH=${PATH}:/path/to/the/negui/modules
				PYTHONPATH=${PYTHONPATH}:/path/to/the/negui/modules 

			b. If your Linux or OSX installation has the typical configuration, then you
			can also automate the change by adding the above lines to the .bashrc file, or
			on OSX, the .bash_profile file, in your home directory. After these lines you
			should then and add an export line for each of the variables: 

				export PYTHONPATH 
				export PATH Windows 

		ii. Windows: Windows provides a gui interface that allows you to
		add new environmental variables.  In most distributions you can find it by
		opening the file explorer and right clicking on the "Computer" icon (Win7), or
		"ThisPC" (Win10).  On the Menu,  select properties->advanced system settings
		(list on right-hand side) -> Environment Varibles.  Under the "system variables"
		window (the bottom window) you can click "New..." to add new variables, as
		likely you'll need to for PYTHONPATH.  To add the path to your negui modules to
		the PATH varable, select "Edit...".  See the existing variables for examples of
		path formatting in Windows.


Current Functionality
---------------------

	1. The GUI interface is invoked using the command 

		python /path/to/negui/negui.py 

	Better, modify negui.py to be executable with the command, 

		chmod +x negui.py  

	This done, and with the location of negui.py in your PATH variable
	(see above), you can simply type negui.py at a terminal. Optionally negui also
	can an integer argument that gives the number or processes to use when doing
	simulation replicates.  This number should practically not exceed the number of
	CPU's on your machine.  It defaults to "1" when no such argument is given.  Note
	that multiple processes are only useful for the simulations when more than one
	replicate is performed (multiplexing in simulations currently is done
	per-replicate). These are the current interfaces:

		a. Simupop simulation:  clicking on the "New" main menu option, then
		"Add new simulation" creates a tab window allowing AgeStructureNe-based simuPop
		simulations when supplied with configuration files.  Currently, life tables are
		preloaded from the resources directory.  Thus, if you need to use your own,
		please open an example or examples in resources, and modify as needed,
		remembering to use a model name that will match that in the configuration file
		you'll load to run the simulation.  Also, currently, you'll need to name your
		customized life table table file so that it ends in ".life.table.info." 

			i. Input: In the interface you'll see the editable parameters listed, as well as
			buttons tos select input configuration file, outpout directory, and the output
			base name (the prefix applied to the output files.		

			ii. Output:  A simulation run produces 5 files, 4 of
			which are compressed.  There are 3 files from the original output of Tiago's
			AgeStructureNe code, *.sim, *.gen, *.db.  There is now also a *.conf, which is a
			configuration file that has all of teh setting used in the simulation, as read
			in from both the life table and the original configuration file, and reflecting
			any changes the user made using the interface, before running the simulation.
			One uncompressed file, *.genepop, is produced.  THis can be then used as input
			to the Ne-estimation analysis.	

		b. LDNe estimation:  Click on the "New" menu, then "Add new Ne
		estimation," to get an interface for running an Ne estimation using NeEstimator,
		via Tiago's AgeStructureNe implemenation.  It requires a genepop file as input
		(using the "select" button).  

			i. Input:  one or more genepop file.  Note that the
			select dialog for genepop files will let you enter an expression in the
			filenames box,  such as *.genepop, to show only matching files.  You can then
			use the shift or control key along with mouse or pad, to load multiple files at
			once.  Currently you can also set several parameters.  Note that setting the
			"replicates" parameter to values other than 1 is currently not useful.
			Replicates in this interface refers to repeated Ne estimates of subsamples of
			the genepop individuals, and such subsampling is not yet available in the GUI.
			Thus 2 or more replicates will simply add identical estimates to the *tsv table.

			ii. Output:  A *.tsv file, giving, for each population in the genepop file, an
			LDNe estimate, with confidence intervals, Expected r-squared, Overall r-squared,
			total Independent Comparisons, Harmonic Mean Sample Size, as produced by the
			NeEstimator program (see the header line in the *tsv for which values are in
			which columns).  A second file *.msgs is also produced, currently not used by
			the program for any results.

	2. You can also perform Ne estimation from the command line, which
	offers subsampling of individuals using  percentages of the populaion
	(randomly selected), or values of N in a remove-N scheme, whereby N randomly
	selected individuals are removed from the population before the Ne is estimated.
	Repicates at each percentage or N value is user set.  In the remove-N case of
	N=1, all combinations are run. For a list of the required input arguments type
	the command "pgdriveneestimator.py" with no arguments.

