# baseball awards

Parse Baseball Reference awards pages into csvs and convert them into the Lahnman database format

## setup

* Manually download baseball reference award pages using your browser
    * This is the fastest way -- something like requests won't work because the pages are filled in asynchronously by the server so requests will only grab the MVP awards and nothing else
    * i.e. https://www.baseball-reference.com/awards/awards_2021.shtml
* Manually update helpers/max_points_file.py if necessary and re-run to regenerate data/max_points.json
* Clone baseballdatabank and copy core/People.csv into data/
    * https://github.com/chadwickbureau/baseballdatabank
* Run helpers/id_mismatches.py to regenerate data/bbref_to_lahnman.json
    * This contains all people with a bbref ID that have a different lahnman ID. This is needed for the conversion into the Lahnman database format to make sure all player IDs align

## usage

1. Run parse.py - this fills in data/ with player and manager award data by year
2. Run convert_to_lahnman.py - this fills contrib/ with award data in the Lahnman database format
3. Contribute to the Lahnman database via baseballdatabank
    * https://github.com/chadwickbureau/baseballdatabank/tree/master/contrib
