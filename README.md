GenomeSpaceTesting version 1.0 24/07/2015
=====================================================================

Author:
	Name: Ruijing (Regina) Zhang
	email: ruijingz@student.unimelb.edu.au

=====================================================================

Usage:
	GenomeSpaceTesting is an automated testing program for 
	GenomeSpace to make sure that the functionality in GenomeSpace
	works properly

=====================================================================

Installation and Setup

Prerequisites: Python 2.7 is installed in the machine

How to Get Selenium?

1. Open up a terminal
2. Type “sudo easy_install selenium” (since you have Python 2.7 installed in your machine and the package 3. manager easy_install) and return
4. Enter your password to install
4. To check if the installation was successful
	4.1. Go to the terminal
	4.2. Type “python” and return to go to the python console  
	4.3. Type “import selenium”
		4.3.1. if installation was successful, the prompt will show at the next line 
		4.3.2. if installation failed, an error message will show



Testing on Chrome

1. Download Chromedriver from here
2. Follow the steps shown in the figure to set up chromedriver
	OR
unzip the package
copy the file to some directory you want it to be in
specify the chromedriver path in the script “chrome_path.py” located in “UROP/GenomeSpaceTesting/source/” directory


Testing on Firefox

Note: 
One of the core tool used in this program, Selenium, only supports certain version of Firefox ( e.g. Selenium 2.45.0, used when developing this program, supports version of Firefox only upto 35)

1. Go into “UROP/GenomeSpaceTesting” and find the file “gs_test.sh”
2. Open the file in a text editor
3. Go to the last line of the file
4. Replace the “GSchrome.py” with “GSfirefox.py” in “./source/GSchrome.py"
5. Save it


How to Run The Program?

1. Go into “UROP/GenomeSpaceTesting” folder
2. Open the configuration file, “file_paths.cfg”, in a text editor
3. Specify all the information in the configuration file
	3.1. The minimum changes
		1.1.1. fill in [UserDetails]
		1.1.2. fill in [GSContainerOne] and [GSContainerTwo]
		1.1.3. EITHER should the container and directory names in the values in [GSFolderPaths] and [GSFilePaths]  be replaced OR leave the values blank
	3.2. Requirements to the changes in the config file are stated in the file as comments
	3.3. The default files are stored in the “UROP/GenomeSpaceTesting/test_files/” folder; changing the contents of the files is allowed but do not delete any file.
	3.4. If file paths are not specified in the config file, a default file is going to be used

4. Open up a terminal and direct to the “UROP/GenomeSpaceTesting” directory
5. Type “./gs_test.sh” and return


Where to Find The Report?

1. After the first run of the program, a folder called “reports” will be automatically generated
2. Go into the “reports” folder and all the subfolders named after the date (“dd-mm-yy”) of the test conducted will be listed there
3. Find the folder with the date of the report you want to see
4. And all the report of tests conducted in that day will be included in the folder with the name as the time (“hh.mm.ss.txt”) when it was conducted


What is The Format of A Report?

1. The first section is the errors/messages given when parsing the config file; if no errors or special message is given, this section will not be shown
2. The second section contains very brief information for the status of the test cases showing if the test cases failed or succeeded
3. The third section consists of all the detailed error messages for failed cases; if no case has failed, this section will not be shown
