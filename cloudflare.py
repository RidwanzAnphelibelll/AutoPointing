#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import time
from colorama import init, Fore, Style
from tabulate import tabulate

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_subdomain(subdomain, ip_address, domain, email, api_key, zone_id):
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'A',
        'name': f'{subdomain}.{domain}',
        'content': ip_address,
        'proxied': False
    }
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"\n{Fore.YELLOW}SUBDOMAIN CREATED:")
        print(f"{Fore.GREEN}Subdomain: {subdomain}.{domain}")
        print(f"IP Address: {ip_address}")
    else:
        print(f"{Fore.RED}Failed to create subdomain '{subdomain}.{domain}'.")
        print(response.text)
    exit()

def delete_subdomain(subdomain, domain, email, api_key, zone_id):
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': api_key,
        'Content-Type': 'application/json'
    }
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    params = {
        'name': f'{subdomain}.{domain}',
        'type': 'A'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['result']:
            record_id = data['result'][0]['id']
            delete_url = f'{url}/{record_id}'
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 200:
                print(f"\n{Fore.YELLOW}SUBDOMAIN DELETED:")
                print(f"{Fore.GREEN}Subdomain: {subdomain}.{domain}")
                exit()
                
        else:
            print(f"{Fore.RED}Subdomain '{subdomain}.{domain}' not found.")
            exit()
    else:
        print(f"{Fore.RED}Failed to delete subdomain '{subdomain}.{domain}'.")
        exit()

def list_domains(email, api_key, zone_id):
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': api_key,
        'Content-Type': 'application/json'
    }
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        domains = []
        for record in data['result']:
            domains.append([record['name']])
        print(f"\n{Fore.YELLOW}DOMAIN LIST:")
        print(tabulate(domains, headers=[f"{Fore.GREEN}Subdomain:"], tablefmt="fancy_grid"))
        exit()
        
    else:
        print(f"{Fore.RED}Failed to retrieve domain list.")
        exit()

def main():
    domain = "domain_cloudflare"
    email = "email_cloudflare"
    api_key = "apikey_cloudflare"
    zone_id = "zoneid_cloudflare"

    while True:
        print(f"{Fore.YELLOW}\n1. Create Subdomain")
        print(f"2. Delete Subdomain")
        print(f"3. Domain List")
        print(f"4. Exit")

        choice = input(f"{Fore.YELLOW}Select option (1/2/3/4): ")

        if choice == '1':
            subdomain = input(f"{Fore.YELLOW}Enter Subdomain Name: ")
            ip_address = input(f"Enter IP Address: ")
            create_subdomain(subdomain, ip_address, domain, email, api_key, zone_id)
        elif choice == '2':
            subdomain = input(f"{Fore.YELLOW}Enter Subdomain Name: ")
            delete_subdomain(subdomain, domain, email, api_key, zone_id)
        elif choice == '3':
            list_domains(email, api_key, zone_id)
        elif choice == '4':
            break

        else:
            print(f"{Fore.RED}Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    clear_screen()
    main()