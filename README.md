# Convert Alpha

A very simple script to convert all transparent pixels to a specific colour.

This is relevant in compression when an algorithm still uses invisible pixels for downscaling, causing the bad colour to bleed into the opaque shape

## Running

For ease of use I recommend adding this script to your PATH.<br>
Learn how to do that here: (How To Set Path Environment Variables In Windows)[https://www.addictivetips.com/windows-tips/set-path-environment-variables-in-windows-10/]

***

First open the folder that contains your images.

Then in the **Address Bar** type `cmd.exe` to open a command line interface.

And finally run the script via this syntax:

```py
python calpha.py FILES... -c COLOUR
```
where `FILES` is the list of different file name patterns
and COLOUR is the colour to set to

***

An Example would be
```py
python calpha.py *.png other/*.png -c FF0000
```
Which would update all PNG images in the current folder and the `other` folder. Every invisible pixel would be updated to be an invisible Red colour (due to FF0000).

## Change Log

### Version 1.0
* Created the script with basic functionality
* Can update transparent pixels to a colour