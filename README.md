This project is a fork off of https://github.com/ev3dev-python-tools/ev3dev2simulator with the support for the configuration for the Owheo foyer floor tile pattern and its noisy color sensor readings.

# ev3dev2simulator: simulator for the EV3 (ev3dev2 API)

The behaviour of the EV3 robot is simulated in the simulator. This is convenient to quickly test programs when you momentarily don’t have access to an EV3.

![cosc343_ev3dev2simulator](img/owheo_foyer.png?raw=true "cosc343_ev3dev2simulator")

You can use the 'ev3dev2' python library to program the EV3. The simulator installs a fake 'ev3dev2' library on the PC. When using this library on the PC, every call to this API is forwarded to the simulator which uses it to simulate the behaviour of the EV3 robot. 

For an example see: https://github.com/ev3dev-python-tools/thonny-ev3dev/wiki/Simulator-example<br>
The running program can be seen in the following video: http://www.cs.ru.nl/lab/ev3dev2simulator.html .

The thonny-ev3dev plugin makes it easier to program the EV3 programmable LEGO brick 
using the [Thonny Python IDE for beginners](http://thonny.org/). 
The thonny-ev3dev plugin for the Thonny IDE comes with the ev3dev2simulator.

For more info about the thonny-ev3dev plugin see: https://github.com/ev3dev-python-tools/thonny-ev3dev/wiki <br>
For more info about Thonny: http://thonny.org

## Getting started

   Clone the repository to your hardrive
   
      git clone https://github.com/lechszym/cosc343_ev3dev2simulator.git
    
   Then change cd into the new created folder

      cd cosc343_ev3dev2simulator

   Activate the anaconda cosc343 environment
   
      conda activate cosc343

   Uninstall previous version of ev3dev2simulator

      pip uninstall ev3dev2simulator
      
   Install the new version from the source code
   
      python setup.py install 

   Then you can run the simulator by running the following script
   
      ev3dev2simulator -t owheo_foyer.yaml

## Changing the location of the bottle/target

Edit the file 'owhoe_foyer.yaml' and change the 'tile' value of the 'target' obstacle.  Values 1 through 12 correspond to the location of the target tiles specified in the assignment script.
