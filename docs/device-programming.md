# Undocumented OpenWebNet

There exists a part of OpenWebNet that is currently undocumented by BTicino, that is, the part of the protocol that allows programming of devices.

## Undocumented frames

You all know the standard `ACK` and `NACK` sentences

* `*#*0##` : `NACK` Command not executed
* `*#*1##` : `ACK` All lights are green !

In some old code, found on the remnants of Microsoft's `archive.codeplex.com` (mirrored here in the `docs/openwebnet.zip` directory) we find the following: 

* `*#*2##` : `NACK_NOP` Invalid command
* `*#*3##` : `NACK_RET` This command exists, but the target device is not present on the bus (wrong address ?)
* `*#*4##` : `NACK_COLL` Impossible to execute this command because of a collision on the bus.
* `*#*5##` : `NACK_NOBUS` Impossible to execute the command because the bus is not available / accessible.
* `*#*6##` : `NACK_BUSY` Multiframe procedure active, but not done yet...
* `*#*7##` : `NACK_PROC` \[ the documentation is mum on that one \]

Never seen those in the wild for now.

## Diagnostic frames ??

If you read the documentation, it states there are diagnostic frames, with special WHO values, but there is no info about those.
Some network sniffing later we have the following table :

* `1000` : generic diagnostic (never seen those yet)
* `1001` : Lighting and automation system
* `1004` : heating / cooling system
* `1008` : video door entry system
* `1013` : gateway
* `1018` : energy management
* `1023` : access control

For most of those, the traffic is more or less copied to the monitor session. Not so with 1023, where only the client doing the diagnostics can see the frames.

## Scanning the system

Devices have a unique identifier, set at the factory and generally on a sticker.
This "Mac Address" is a 32 bit number, represented in hex on the sticker.

In MyHomeSuite, the following subsystems can be scanned :

* `1001`
* `1004`
* `1018`
* `1023`

### step 1: clear the cache

Scanning involves some kind of cache in the gateway.
To clear this cache, one needs to send the `CMD_RESET` sentence :

`*[who]*12*0##`

the gateway returns an `ACK` frame `*#*1##`

once that is done, you can start the scan

### step 2: starting the scan

The `CMD_SCAN_SYSTEM` sentence will make the gateway scan the bus for the various devices of the WHO passed:

`*#[who]*0*13##`

The gateway then responds with a series of `RES_ID` sentences, one per device on the bus:

`*#[who]*[where]*13*[id]##`

* `where` is probably unimportant, it is 0 for buttons, and the configured address of the leftmost relay in a F411 device.
* `id` is the device mac address in decimal.

The list ends with an `ACK` frame.

### Step 3: More scanning

If you have more systems to scan, you can go back to step 1 with a different `who`.

### Step 4: Done scanning

If you are done scanning, you need to send the `CMD_RESET` again, otherwise, wierd things happen, you should receive an `ACK` frame for your troubles.

## Reading a device configuration

This gets more interesting...

Once you have all your devices' mac addresses, you can start poking at them to get their configuration parameters.

### Step 1: Starting the device diagnostic

The process is started by sending the `CMD_DIAG_ID` sentence.

`*[who]*10#[id]*0##`

Where `who` is the system, and `id` is the mac address of the device.

The gateway responds with an `ACK` frame.

*Note:* there are other modes, such as by pressing a button, which I haven't looked at yet.

*Note 2:* you may see many `CMD_CONF_ABORT` during this process. it looks like those are used as a way of telling that something is busy.
I have no idea why they didn't use the `NACK_BUSY` sentence instead, which would have made much more sense...

`*[who]*3*0##`

### Step 2: First pass at getting data back

This is where it gets wierd, you'd imagine getting all the answers in the command session, which would make things more logical... 
Well, no, doesn't work that way, you get that first salvo of answers on the monitor session...

Thus... in the monitor sessions you get the following :

#### 2.1: A reminder that a device is being looked at

You get that frame you send back from the gateway.

`*[who]*10#[id]*0##`

Note that this may be useful if you're listening in and another machine launches a device diagnostic.

#### 2.2: Generic information about the device

The `RES_OBJECT_MODEL` sentence gives several bits of information about the device.

`*#[who]*[where]*1*[object_model]*[n_conf]*[brand]*[line]##`

* `who` and `object_model` gives the exact device type, for instance, `(1001, 2)` is a 2 button, Basic Command device (for instance an _H4652_), `(1001, 129)` is a _F411/2_
* `n_conf` gives the number of physical configuration spots on the device
* `brand` gives the device brand, it may be `0` for older devices
* `line` gives the product line, which may also be `0` for older devices

#### 2.3: Firmware version numbers

The `RES_FW_VERSION` sentence gives the device's firmware version, as `[major]*[minor]*[build]`.

`*#[who]*[where]*2*[fw_version]##`

#### 2.4: Hardware version

You may receive `RES_HW_VERSION` with the version number of the hardware.

`*#[who]*[where]*3*[hw_version]##`

#### 2.5: Configurators

The next sentence, `RES_CONF_1_6` gives the value of physical configurators on the device.

`*#[who]*[where]*4*[c1]*[c2]*[c3]*[c4]*[c5]*[c6]##`

You may also get the `RES_CONF_7_12` sentence, if there are more than 6 physical configurators slots (see the `n_conf` in `RES_OBJECT_MODEL`).

`*#[who]*[where]*5*[c7]*[c8]*[c9]*[c10]*[c11]*[c12]##`

#### 2.6: Micro version

On more advanced devices you may have a larger processor, and smaller microcontrollers to connect the device to the bus.

This `RES_MICRO_VERSION` sentences gives the firmware of the helper microcontroller.

`*#[who]*[where]*6*[micro_version]##`

#### 2.5: Diagnostic bits

There are two series of diagnostic bits, A, and B, respectively given by the `RES_DIAG_A` and `RES_DIAG_B` sentences.

`*#[who]*[where]*7*[bitmask_dia_a]##`

`*#[who]*[where]*8*[bitmask_dia_b]##`

#### 2.6: Device mac address (again !)

You then get the `RES_ID` sentence that you got from scanning the system. this is probably in case you're using one of the other scanning modes.

`*#[who]*[where]*13*[id]##`

#### 2.7: Submodules configuration

A device is composed of submodules, called _slots_. For instance, on the 4652/2 type device, there is one slot for each rocker button.

Each slot can be set to a series of data models, which is specific for each device.

One of the data model is the _unconfigured_ mode, where the portion of the device doesn't do anything.

There are multiple sentences related to this part of the configuration, so let's start...

##### 2.7.1: Slot data model

Ths slot data model is given by the `RES_KO_VALUE` sentence.

`*#[who]*[where]*30*[slot]*[keyo]*[state]##`

* `slot` is the slot number, this can be between 1 and 32
* `keyo` is the data model identifier (an integer)
* `state` indicates if the slot is configured. Note that this may be somewhat duplicated with the _unconfigured_ `keyo` number for each device

##### 2.7.2: Slot is somehow busy

This needs an example...

*#1001*02*31*4*1*0##

When a F411/2 is configured with slot 1 set as _Automation Control_, this takes 2 adjacent relays. In that case, you will get the info with the `` sentence.

_TODO: find which sentence is actually sent here_

##### 2.7.3: Address and System

In certain cases, you may get `RES_KO_SYS`, indicating the bus address this submodule answers to, and the System.

`*#[who]*[where]*32#[slot]*[sys]*[addr]##`

* `sys` is the subsystem this device is in, typically `1` for lighting.
* `addr` is the address the device will respond to.

For now, I have only seen actuators (_F411\[something\]_) sending this.

_Note:_ It looks like there is a bug in the _F454_, when a _H4652_ slot is configured in `CEN` mode, the programming tool sends this information 
(the address is used as the `CEN` command number), however, this is not given back when reading the configuration again

#### 2.8: End of transmission

When the gateway is done with all the submodules, it sends the `RES_TRANS_END` sentence.

`*1001*4*0##`

But you're not done yet...

### Step 3: Getting details about the configuration

Well, technically, you could just go ahead and skip to _Step 4_, but that's not what we're here for, are we...

So, lets start the next phase, requesting detailed configuration for each slot.

#### 3.1: Requesting the lot

To start the flow of goodies, you have to send the `CMD_PARAM_ALL_KO` sentence.

`*#[who]*0*38#0##`

_Note_: there is a more specific version of this sentence, `CMD_PARAM_KO`.

`*#[who]*0*38#[slot]##`

Where `slot` is the slot number.

As you can infer, _0_ means _all_ :-)

#### 3.2: Getting all parameters

You are then flooded with the parameters, in a series of `RES_PARAM_KO` sentences.

Note that, contrarily to the previous step, this part is also sent on the command connection... 
(another developper perhaps ? previous step is a bug or a missing line of code ? mysteries and illogical things abound in this gateway firmware...)

`*#[who]*[where]*35#[index]#[slot]*[val_par]##`

* `index` is the parameter number
* `slot` is the slot number
* `val_par` is the value for this parameter

These are all specific depending on the data model for the slot. A series of documentation files will be required at this point :-)

#### 3.3: End of transmission

When the list of parameters is done, the gateway sends an `ACK` frame.

### Step 4: End of the diagnostic session

This is perhaps the most important part of the procedure. Not doing this will leave the device under scrutiny in limbo (is there a timeout ? no idea).

You **MUST** send the `CMD_DIAG_ABORT` sentence.

`*[who]*6*0##`

At which point, the gateway will answer with an `ACK` sentence, and you'll be done.

You can reuse the command connection, or you can close it and open a new one. Remember, there's a 30s timeout on that one.

