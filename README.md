# system-application (name TBD)

## Contents
- [Description](#description)
- [Setup Guide](#setup-guide)
- [Credits](#credits)

## Description
A web application for those with DID & OSDD
to organise alters & subsystems. 

DID & OSDD are more commonly known by the outdated term Multiple
Personality Disorder (MPD). MPD is a term [introduced in the DSM-3](https://www.frontiersin.org/articles/10.3389/fpsyg.2021.637929/full#B2) of in 1980
and was later reclassified into Dissociative Identity Disorder (DID)
and Dissociative Disorder Not Otherwise Specified (DDNOS) in future editions. 
DDNOS was later renamed to Other Specified Dissociative Disorder (OSDD) 
in the DSM-5 in 2013. 

Note that the "personalities" mentioned are referred to as "alters"
(deriving from "alter-ego"), and a collection of alters in a body
is known as a "system", 

[Discord](https://discord.com) is the preferred communication app for many
systems due to the integration of bots such as [TupperBox](https://tupperbox.app)
and [PluralKit](https://pluralkit.me) (open-source on [GitHub](https://github.com/PluralKit/PluralKit)), 
which allow users to add a prefix and/or suffix to their messages in order to 
change the display name and profile picture under which they are sent by making
use of discord's Webhook integration. 

![A gif of a Discord proxy bot in action](jbrunton4.github.io/systems-application/assets/img/proxy-demo.gif)
<br /><sup>A gif of a Discord proxy bot in action</sup> 

Due to the nature of these bots and Discord itself, it can be somewhat
difficult for the average user to search through alters' profiles, 
and customisation is highly limited. This is what inspired me to create 
this solution. 

## Setup Guide
This project was built to work with Python 3.11.3 and requirements as listed in 
`requirements.txt` to run on a machine running Windows 11 build 22621.1555.

If you have a compatible Python installation on your machine and PIP is in your path, 
you can run `start.bat` to automatically ensure requirements and start the server. 

## Credits
Props to [TupperBox](https://tupperbox.app) and [PluralKit](https://pluralkit.me)
for inspiring this project and being a valuable tool for anyone who uses proxies, 
be it systems, role-players, or others. Please consider donating to these projects
in order to help keep them running. 

