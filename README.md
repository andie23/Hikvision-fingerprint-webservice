# Description

Web based service for Hikvision fingerprint devices. Has web based APIs for verifying and recording fingerprints

# How it works
Runs a local web service on a windows machine on some port number. With the fingerprint device connected to the localmachine, 
the webservice listerns for events to initiate the fingerprint device to scan any finger placed on the scanning glass. 
You can integrate this service with your website inside the browser using the localhost's name and the port number assigned to the webservice.

# Api endpoints
  `/capture` : get's a snapshot of a fingerprint and returns fingerprint token
  `/match` : service for matching two fingerprint tokens
  
# Requirements
 * Windows 10
 * Hikvision fingerprint SDK files
 * 
# Installation
  * In application folder, create direction named lib
  * Copy Hikvision SDK files into lib directory 
