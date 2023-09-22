#!/usr/bin/env python3

import re
import sys
import urllib3
import requests
import urllib.parse
from bs4 import BeautifulSoup


class Scanner:
    def __init__(self, url, ignore_links):
        self.links_to_ignore = ignore_links
        self.session = requests.Session()  # session as is if we're still opening the web browser
        self.target_url = url
        self.target_links_list = []
        self.HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/102.0.0.0 Safari/537.36'}  # send the request like browser

    def extract_links(self, website_url):
        try:
            return re.findall('href="(.*?)"', self.session.get(url=website_url, headers=self.HEADERS).text)
        except requests.exceptions.ConnectionError:
            pass

    def crawl(self, url=None):  # this mean we can call crawl method without specifying the url <default parameter>
        if url is None:
            url = self.target_url
        href_links = self.extract_links(website_url=url)
        for link in href_links:
            link = urllib.parse.urljoin(base=url, url=link)

            if "#" in link:  # remove the part that loads different part in the same html page
                link = link.split("#")[0]
            if self.target_url in link and link not in self.target_links_list and link not in self.links_to_ignore:  # remove external links <facebook, linkedin, youtube, etc..>
                self.target_links_list.append(link)
                print(link)
                self.crawl(url=link)  # recursive mapping whole website

    def extract_forms(self, url):
        response = self.session.get(url=url, verify=False, headers=self.HEADERS)
        parsed_html = BeautifulSoup(markup=response.text, features="html.parser")  # parse html code

        return parsed_html.findAll("form")  # extract all form tags in the webpage

    def submit_forms(self, form, value, url):
        action = form.get("action")  # get <action=""> attributes from form tags
        method = form.get("method")  # get <method=""> attributes from form tags
        post_form_url = urllib.parse.urljoin(base=url, url=action)  # combine the base url and the relative path

        post_data = {}
        inputs_list = form.findAll("input")  # extract all input tags in the webpage
        for input in inputs_list:
            input_name = input.get("name")  # get <name=""> attributes from input tags
            input_type = input.get("type")  # get <type=""> attributes from input tags
            input_value = input.get("value")  # get <value=""> attributes from input tags

            if input_type == "text":  # check only the text type input <not includes submit and other types>
                input_value = value
            post_data[input_name] = input_value
            if method == "POST" or "post" or "Post":
                return self.session.post(url=post_form_url, data=post_data, headers=self.HEADERS)  # submit the crafted post request
            else:
                return self.session.get(url=post_form_url, params=post_data, headers=self.HEADERS)  # submit the crafted get request

    def test_xss_in_form(self, url, form):
        xss_script = "<ScriPt>alert(7);</sCripT>"  # change this script whatever you want
        response = self.submit_forms(form=form, url=url, value=xss_script)
        if xss_script in response.text:  # check if the script got injected successfully
            return True

    def test_xss_in_link(self, url):
        xss_script = "<ScriPt>alert(7);</sCripT>"  # change this script whatever you want
        url = url.replace("=", "=" + xss_script)
        response = self.session.get(url=url)
        return xss_script in response.text  # check if the script got injected successfully

    def run(self):
        for link in self.target_links_list:
            forms = self.extract_forms(url=link)

            for form in forms:  # iterate through all extracted forms
                print("[+] testing form in " + link)
                is_vuln_to_xss = self.test_xss_in_form(url=link, form=form)
                if is_vuln_to_xss:
                    print("\n\n[***] xss discovered in " + link + " in this form")
                    print(form)

            if "=" in link:  # testing query parameters exists in links
                print("\n\n[+] testing " + link)
                is_vuln_to_xss = self.test_xss_in_link(url=link)
                if is_vuln_to_xss:
                    print("[***] xss discovered in " + link)
