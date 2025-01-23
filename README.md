This code allows to use a Raspberry Pi Pico w or any rp2040 System On Chip to broadcast audio.
The main objective of this project is to stream audio coming from ADC to use it as a IOT doorbell capable of 2 way audio communication.

As you can see, the code just generates random waveforms and sends it.
In reality rp2040 isn't capable of such thing, and the stream tends to lag a little.

*Somehow, i think this script can actually damage the coms between the rp2040 and the CYW43439 permanently.

The intention is to rewrite the whole script to C++ and overclock the Pi to it's limits. 
