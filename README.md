# baseball awards

Parse Baseball Reference awards pages into csvs and convert them into the Lahnman database format

## setup

* Manually download baseball reference award pages using your browser
    * This is the fastest way -- something like requests won't work because the pages are filled in asynchronously by the server so requests will only grab the MVP awards and nothing else
    * i.e. https://www.baseball-reference.com/awards/awards_2021.shtml
* Manually update helpers/create_max_points_file.py if necessary and re-run to regenerate data/max_points.json

## usage

1. Run parse.py - this fills in data/ with player and manager award data by year
2. Run convert_to_lahnman.py - this fills contrib/ with award data in the Lahnman database format
3. Contribute to the Lahnman database via baseballdatabank
    * https://github.com/chadwickbureau/baseballdatabank/tree/master/contrib
