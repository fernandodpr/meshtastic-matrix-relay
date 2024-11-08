# M<>M Relay

### (Meshtastic <=> Matrix Relay)

A powerful and easy-to-use relay between Meshtastic devices and Matrix chat rooms, allowing seamless communication across platforms. This opens the door for bridging Meshtastic devices to [many other platforms](https://matrix.org/bridges/).

## Features

- Bidirectional message relay between Meshtastic devices and Matrix chat rooms, capable of supporting multiple meshnets
- Supports serial, network, and ***BLE (now too!)*** connections for Meshtastic devices
- Custom keys are embedded in Matrix messages which are used when relaying messages between two or more meshnets.
- Truncates long messages to fit within Meshtastic's payload size
- SQLite database to store node information for improved functionality
- Customizable logging level for easy debugging
- Configurable through a simple YAML file
- Supports mapping multiple rooms and channels 1:1
- Relays messages to/from a MQTT broker, if configured in the Meshtastic firmware (*Note: Messages relayed via MQTT currently share the relay's `meshnet_name`*)


*We would love to support [Matrix E2EE rooms](https://github.com/geoffwhittington/meshtastic-matrix-relay/issues/33), but this is currently not implemented. If you are familiar with [matrix-nio](https://github.com/poljar/matrix-nio/), we would gladly accept a PR for this feature!*

  

### Windows Installer

<img  src="https://user-images.githubusercontent.com/1770544/235249050-8c79107a-50cc-4803-b989-39e58100342d.png"  width="500"/>  

The latest installer is available [here](https://github.com/geoffwhittington/meshtastic-matrix-relay/releases)

### Plugins
M<>M Relay supports plugins for extending its functionality, enabling customization and enhancement of the relay to suit specific needs. Plugins can add new features, integrate with other services, or modify the behavior of the relay without changing the core code.

## Core Plugins
Generate a map of your nodes

<img  src="https://user-images.githubusercontent.com/1770544/235247915-47750b4f-d505-4792-a458-54a5f24c1523.png"  width="500"/>

Produce high-level details about your mesh

<img  src="https://user-images.githubusercontent.com/1770544/235245873-1ddc773b-a4cd-4c67-b0a5-b55a29504b73.png"  width="500"/>

## Custom plugins
It is possible to create custom plugins to add new features or modify the relay's behavior. Check more info in [example_plugins/README.md](https://github.com/geoffwhittington/meshtastic-matrix-relay/tree/main/example_plugins)

## Install a community plugin
To install plugins, simply modify the config.yaml file and add the user's repository under the community-plugins section.

```
community-plugins:
  weather_plugin:
    active: true
    repository: https://github.com/anotheruser/weather_plugin.git
    tag: master

```


**Note:** If the plugin requires additional dependencies, they will be installed automatically if a requirements.txt file is present in the plugin's directory.

## Getting Started with Matrix

See our Wiki page [Getting Started With Matrix & MM Relay](https://github.com/geoffwhittington/meshtastic-matrix-relay/wiki/Getting-Started-With-Matrix-&-MM-Relay).

## Already on Matrix?

Join us!

- In our project's room: 
  [#mmrelay:meshnet.club](https://matrix.to/#/#mmrelay:meshnet.club)

- Which is a part of the Meshtastic Community Matrix space *(an unofficial group of enthusiasts)*:
  [#meshtastic-community:meshnet.club](https://matrix.to/#/#meshtastic-community:meshnet.club)  

## Supported Platforms

The relay is compatible with the following operating systems:

- Linux
- MacOS
- Windows

Refer to [the development instructions](DEVELOPMENT.md) for details about running the relay on MacOS and Linux.
