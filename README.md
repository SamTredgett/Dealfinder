# Dealfinder

Please install dependencies from requirements.txt

Please note, this also operates on the following:

Chrome version: 95.0.4638.69

Chromedriver version: 95.0.4638.69

Alternate chromedriver version may be necessary if you're running this script on a computer with a different version of
Chrome installed.

To run this, please generate a virtualenv using the requirements.txt file, then run each script individually.
At the end of each script you will be prompted in the terminal to provide name for the ouput CSV file for the scraping results.


**Notes on performance**

I am aware of an ongoing consistency bug with bt.py, I've tried to iron this out, but frankly I'm no sure
what the issue is. It seems to have trouble occasionally switching to the cookie iframe and this causes it to not find
the button to click. If you do experience this issue, please just re-run the script once or twice, it should work.