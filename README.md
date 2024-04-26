
# SSTI_Detector
This SSTI detector identifies and tests potential Server-Side Template Injection vulnerabilities by injecting various payloads into input fields or parameters and observing the server's response for indications of successful injection, aiding in identifying and mitigating security risks.


## Deployment

To deploy this project download the repository

```bash
  git clone https://github.com/KushagraVarshney101/SSTI_Detector
```
Install necessary Requirements
```bash
  pip3 install -r requirements.txt
```


## Usage
For GET Method
```bash
  python3 Detector.py -u <Insert URL> --get 1
```
For Post Method
```bash
  python3 Detector.py -p <Insert Parameter> --post 1
```
To Scan List Of URL's
```bash
  python3 Detector.py -f <Your List Of URL's in a .txt file>
```
## Reference

This tool has been made by taking Reference from videos of BePractical.
