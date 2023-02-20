# k3y1ogg3r

## Intro

The goal of the project was to create and use an Advanced Persistent Threat (APT) tool that will be permanently embedded in a specific computer system. The tool aims to covertly track the activities of operators, gain access to selected information resources, and covertly derive this information with the security of the location and identity of the recipient.

## Description 

The program, written in Python 3, records the keys pressed by the victim and collects information about the system, such as 
such as:
- Operating system
- Computer name (hostname)
- CPU
- Public IP address
- Private IP address
- MAC physical address
- Subnet mask
- Broadcast address

The program also creates an entry in the system registry (autostart) so that it can run automatically when the computer is restarted. To reduce the probability of detection, the program creates hidden files, deletes sent logs and hides in the task manager,impersonating the name of a standard Windows process.

Every minute, the program sends logs to the attacker's email address and automatically deletes them from the victim's computer. With the logs, the attacker can gain access to passwords, PINs and usernames. The program can be terminated by the victim when it is detected and the process is killed using the Windows task manager.

## Requirements:
- Python 3.x
- Windows operating system

## Installation and Usage
- Clone this repository in the terminal (or command prompt)
```shell
   git clone https://github.com/WojciechSkumajTo/k3y1ogg3r.git 
```
- Run the Python 3 code in the terminal (or command prompt):
```shell
  sudo python3 systems.py
```
OR
- installing the *.exe program as administrator
