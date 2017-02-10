# MCM_GetXsec

It is not suggested to run this on a remote machine at places such as LPC or LXPLUS because of sudo privileges needed and the slow nature of X11 on these computers.

There are quite a few dependencies to run this repo.  There are different headless (aka graphicless) webbrowsers that exist, namely 
PhantomJS, but the mcm page has untrusted certifications that stop the program from crawling through the pages.  Firefox has the ability
to ignore these warnings, but it only works currently with the developmental version of firefox (the "nightly" version).  This can be 
run with visuals which is slightly slower and requires no sudo privileges, but without makes things slightly more streamlined

The option to run with or without visuals is available when setting up the files.

### Dependencies
- Python
 - selenium
 - pyvisualdisplay
- firefox (nightly version)
 - geckodriver
- xvfb

All of these programs are check for and installed when running the setup program.

## Running

The process is fairly easy to run, simply setup, then run by typing:
```
./setup.sh
python get_xsec.py
```

The package should run out of the box.  The output from the program are the non-redundent values from each of the selected options.  The
default options are "Dataset name", "Generators", and "Generator parameters".  The output is raw, so for more sophisticated output, this 
must be done by the user or will be updated in later versions.

### Values to change

There are a few values that can be changed to get different results.  First is the options.

There is a variable, `shown_list` that is a list of all the possible values that can be shown in the table.  The ones you wish to have 
in your output are put into `shown_wants`.  Simply put all of the options you want into the `shown_wants` array.  Be warned, the program
only looks for rows that have values in each column, so if certain options are picked, samples may be ignored because they don't have
a value in every column.

The other important variable is `sample_filename`.  This is the variable that holds the filename of the text file with the samples in 
it.  The default filename is `sample_filename`, but this can easily be changed if many different types of samples are needed to be 
iterated over.  

## Possible Errors
In testing this program, a bug is showing that doesn't have an obvious answer.  Because this program works with selenium which acts as 
the user would in filling in and clicking values, there is sometimes lag between when the page has been loaded fully and when selenium
tries to get values from a page.  This means that some arrays might show up empty when run over.  This is usually random, and running 
program again has led it to work the second time.  The ways to guard against this is making the program sleep more between requests.

To do this, go to the command `time.sleep(#)` and change \# to a larger number is the problem persists.  Also, change the \# in 
`driver.implicitly_wait(#)` to a larger value so the program tries over that time period till it gets a none null result.  

Any other issues that one might find, please raise an issue or email the BSM3G group for more help
