# Packettracer for Fedora ecosystem
Helper script to install Cisco Packet Tracer on Fedora and other Red Hat-based distributions.

## Install
1. Download the Cisco Packet Tracer `.deb` package and place it in this directory.
2. Make the setup script executable:
```bash
    chmod u+x setup.sh
    ./setup.sh Cisco*.deb
    sudo dnf install packettracer*.rpm
```

## Uninstall
```bash
    sudo dnf remove packettracer
```

## Why create the stupid code like that?
Simple answer, Cisco provide Packet Tracer as a .deb package, and there is no build for Red Hat-based distributions. 
I needed it for my own hobby, so I wrote this script to fill the gap. So, i hope you happy. Probably no? :>
