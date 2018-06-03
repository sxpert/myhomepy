# Undocumented OpenWebNet

There exists a part of OpenWebNet that is currently undocumented by BTicino, that is, the part of the protocol that allows programming of devices

## Diagnostic frames ??

If you read the documentation, it states there are diagnostic frames, with special WHO values, but there is no info about those.
Some network sniffing later we have the following table :

* 1000 : generic diagnostic (never seen those yet)
* 1001 : Lighting and automation system
* 1004 : heating / cooling system
* 1008 : video door entry system
* 1013 : gateway
* 1018 : energy management
* 1023 : access control

For most of those, the traffic is more or less copied to the monitor session. Not so with 1023, where only the client doing the diagnostics can see the frames

## Scanning the system

Devices have a unique identifier, set at the factory and generally on a sticker.
This "Mac Address" is a 32 bit number, represented in hex on the sticker.

In MyHomeSuite, the following subsystems can be scanned :

* 1001
* 1004
* 1018
* 1023

### step 1: clear the cache

Scanning involves some kind of cache in the gateway.
To clear this cache, one needs to send the `CMD_RESET` sentence :

`*[who]*12*0##`

the gateway returns an `ACK` frame `*#*1##`

once that is done, you can start the scan

### step 2: starting the scan

The `CMD_SCAN_SYSTEM` sentence will make the gateway scan the bus for the various devices of the WHO passed:

`*#[who]*0*13##`

The gateway then responds with a series of `DIAG_RES_ID` sentences, one per device on the bus:

`*#[who]*[where]*13*[id]##`

* `where` is probably unimportant, it is 0 for buttons, and the configured address of the leftmost relay in a F411 device
* `id` is the device mac address in decimal

The list ends with an `ACK` frame.

### step 3: more scanning

If you have more systems to scan, you can go back to step 1 with a different `who` 

### step 4: done scanning

If you are done scanning, you need to send the CMD_RESET again, otherwise, wierd things happen, you should receive an `ACK` frame for your troubles

## 


