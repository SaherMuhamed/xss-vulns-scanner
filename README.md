# XSS Vulnerabilities Finder

This Python script performs a web vulnerability scan for cross-site scripting (XSS) on a specified target website. It utilizes various techniques to identify potential vulnerabilities within the target site.

## Screenshot
<video src="https://github.com/SaherMuhamed/xss-vulns-scanner/blob/main/screenshots/2023-09-22%2023-22-58.mp4" controls title="Title"></video>

## Usage
- Ensure you have Python 3.0 or later installed to run this script. Use the following command to execute the script:

    ```commandline
    python3 vulns_scanner.py <url>
    ```

- Replace `url` with the target website's URL.

## Prerequisites
- Python 3.0 or later
- Required Python packages: `requests`, `beautifulsoup4`
- Install the necessary packages using pip:

    ```commandline
    pip install requests beautifulsoup4
    ```

## How It Works

- The script performs the following steps to identify XSS vulnerabilities:

    1. **Crawling the Website:** The script starts by crawling the target website to identify all accessible links.
  
    2. **Extracting Forms:** It extracts HTML forms from the web pages to identify potential injection points.
  
    3. **Testing XSS in Forms:** For each form identified, it tests for XSS vulnerabilities by injecting a simple XSS script.
       
    4. **Testing XSS in Links:** It tests links with query parameters for XSS vulnerabilities by injecting a simple XSS script.
       
    5. **Displaying Results:** If an XSS vulnerability is detected, it displays information about the vulnerable form or link.

## Disclaimer
This script is intended for educational purposes and should only be used with explicit consent from the owner of the target website. Unauthorized use is strictly prohibited. I am not responsible for any misuse or damage caused by this script that I made.

## Author
**Saher Muhamed @ 20/9/2023**
