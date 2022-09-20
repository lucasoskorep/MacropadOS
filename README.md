``` 
 _______________________
| |MACROPAD OS!| /    \ | 
| |____________| \____/ |
| _____   _____   _____ |
||key1 | |key2 | |key3 ||
||_____| |_____| |_____||
| _____   _____   _____ |
||key4 | |key5 | |key6 ||   
||_____| |_____| |_____||
| _____   _____   _____ |
||key7 | |key8 | |key9 ||
||_____| |_____| |_____||
| _____   _____   _____ |
||key11| |key13| |key12||
||_____| |_____| |_____||
|_______________________|
```

# Macropad OS!

MacropadOS is a simple OS build to run on the [Adafruit Macropad](https://www.adafruit.com/product/5128).  It's a very 
basic GUI running in CircuitPython which allows users to navigate through apps, change settings, and more coming soon!

The OS itself is one part of the project though, this also includes a framework for building quick and simple apps in 
CircuitPython using a framework very similar to Android apps with a very similar app-lifecycle (OnStart, OnResume, etc). 

This repo contains everything you need to get started, from building the macropad itself to installing the software and 
creating your own apps!


## Building the Macropad (Pictures coming soon<sup>tm</sup>):

See the 3d_printing_files folder for all the required .3mf model files!
If printing at home is not an option for you, you can reach out to https://craftcloud3d.com or similar services to 
print the files for you! 


#### Required Materials:
* 3d Printed
  * 1x Main body
  * 1x Key stabilizer
  * 2x Peg Feet (can be TPU)
  * 1x Support Bar (can be TPU)
  * 12x Cherry MX Compatible KeyCaps
* Purchased
  * 12x Cherry MX Compatible Keys

#### Optional (also 3d printed, but with TPU or another flex material):
* 1x Top Dampener
* 1x Bottom Dampener

#### Assembly:
1. Print all the required parts and any optional parts above. 
2. (Optional)Take the dampeners if you are using them and place them into the main body with the pegs facing out of the body at the top and bottom. 
3. Take the Adafruit Macropad and place it into the main body. It will snap into the second set of slots on the side of the body. 
4. Snap the key stabilizer into the top slots on the body above the macropad itself.  Feet of the stabilizer should touch the macropad itself. 
5. Install the 12 keys into each slot
6. Add the Keycaps and press them onto each key
7. Flip macropad over and press in peg feet
8. Do the same for the top Support bar
9. You now have a fully assembled Macropad!



## Installing Macropad OS:
Requirements:
* Macropad with the CircuitPython installed on it.  See [docs](https://CircuitPython.org/board/adafruit_macropad_rp2040/)
* Python 3.5+ 

Installation:
```bash
pip install circup # See the circup repository(https://github.com/adafruit/circup) for any issues installing circup
circup install -r requirements.txt
# Open copy_to_device.cmd and make the first line the letter of your circutpython drive
copy_to_device.cmd
# Alternatively just copy all of the files not in the 3d printing folder and copy them to the CircuitPython device
```

Congrats!  MacropadOS is now installed and after all of the files are transferred to the device it will boot. 

## Creating JSON Apps (Easy):

Documentation coming soon...

## Creating Python Apps (Advanced):

Documentation coming soon...

