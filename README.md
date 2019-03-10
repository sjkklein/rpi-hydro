# rpi-hydro
Code for all of the pieces of the hydroponics system in my bathroom

## design overview
The hydroponics system is a multitiered flood and drain system. Each tier has a bell siphon draining into the next tier. With this setup I think I can grow ~100 plants in 2'x4' of floor space. Right now the system is in my spare bathroom so I can only fit 2 trays. 

### Software needs
The software needs to control the pump timing along with the light cycles. Additionally I would like to monitor that the flood and drain cycles are always working. This way if something fails the pump can be disabled and a push notification is sent to my phone. 

### Implemention

#### Hardware
I created an outlet box with a linknode R4 embedded inside it. I am using two of four the relays in order to control a single outlet for the pump and a single outlet for the lights. The other outlets of the 2 gang box are always on in order to power the raspberry pi.   
The raspberry pi has +5v, GND, and UART0_TX going to the linknode R4 in order to power it and communicate. I chose not to use the internet capabilities of the esp8266 in the outlet box to keep things simple and not spend a single second thinking about IP addresses. This thing runs the pump and without a constant connection my plants could die in hours. 

#### Software
There is a very simple arduino application that was flashed onto the linknode R4 to implement a UART based communication protocol to control the two outlets that are switchable.

##### UART comm interface
To change which outlet you are controlling you send the number in ascii. The only valid numbers are 1 and 2. To turn on the selected outlet you send +, to turn it off you send -. 
to turn on outlets 1 and 2 you send the ascii string '1+2+', to turn them off send '1-2-'. The protocol doesn't require the number of the outlet getting sent on every transaction, but it doesn't hurt.

##### Push notifications
Push notifications are implemented using the android app/api Pushed. There is a super simple api to send a notification. There was a little bit of setup involved with subscribing to the dev channel on my phone, but it wasn't too hard and google can help you there.

##### Timing implementation
I am just using python to do all of the timing. The pump is being run from a separate thread that just performs corse timing with sleep(). The lights I want to be accurate so the light cycle doesn't drift. So the lights have alarms to turn them on and off. 

