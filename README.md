										***fin_width.py***


*Syntax:
fin_width.py -h | ( -all | -list <list_file> | <cell_1>  <cell_2> … )  -path <review_path>
-h:	shows a help message
-all:	works on all cells inside "cells" folder
-list:	works on cells found in the <list_file> provided in the same folder the script is in.
<cell1>: provide the cell names which you want to check.
-path:	(optional) to provide a <review_path> of the review folder (the folder containing the "cells" folder) if you wish to run the script outside said folder.


*Mapping file:
The script uses a mapping file "fin_width.mapping" as a reference for comparison, each time you run the script, you'll be showed the current mapping file values (if it exists) and asked to confirm or change its values.
Once you confirm or enter new values, the script will work on the specified cells.


*Log file:
Upon completion, the script will print the number of failed LVS files on the terminal, along with a path to the "fin_width.log" file that contains the name of the failed cell followed by the transistors that failed alignment for all failed LVS files.
If all cells were aligned, the script would print out "Pass" and write "all cells passed" in the log file.
