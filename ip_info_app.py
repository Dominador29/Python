"""
IP Address Information Application
Project Activity 3 - Option 2
Team: THE DREAM TEAM

This application retrieves and displays public IPv4/IPv6 address information
including geolocation, ISP details, and network information.

Version: 1.0.0
Author: Team THE DREAM TEAM
Date: October 2024
"""

import requests
import json
from datetime import datetime
import time
import sys

__version__ = "2.0.0"
__author__ = "Team THE DREAM TEAM"      
__date__ = "October 2024"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Display application banner with version info"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}")
    print("        IP ADDRESS INFORMATION TOOL")
    print("              Team Quizzle")
    print(f"              Version {__version__}")
    print(f"{'='*60}{Colors.END}\n")

def get_ipv4_info():
    """
    Fetch IPv4 address using ipify.org
    Returns: IPv4 address string or None if error
    """
    try:
        print(f"{Colors.YELLOW}Fetching IPv4 address...{Colors.END}")
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        
        if response.status_code != 200:
            print(f"{Colors.RED}Error: Unable to fetch IPv4 (Status: {response.status_code}){Colors.END}")
            return None
            
        ipv4 = response.json()['ip']
        print(f"{Colors.GREEN}IPv4 retrieved: {ipv4}{Colors.END}")
        return ipv4
        
    except requests.exceptions.Timeout:
        print(f"{Colors.RED}Error: Request timed out for IPv4{Colors.END}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}Error: Connection failed for IPv4{Colors.END}")
        return None
    except Exception as e:
        print(f"{Colors.RED}Error fetching IPv4: {str(e)}{Colors.END}")
        return None

def get_ipv6_info():
    """
    Fetch IPv6 address using ipify.org
    Returns: IPv6 address string or None if not available
    """
    try:
        print(f"{Colors.YELLOW}Checking for IPv6 address...{Colors.END}")
        response = requests.get('https://api64.ipify.org?format=json', timeout=10)
        
        if response.status_code == 200:
            ipv6 = response.json()['ip']
            if ':' in ipv6:
                print(f"{Colors.GREEN}IPv6 retrieved: {ipv6}{Colors.END}")
                return ipv6
            else:
                print(f"{Colors.YELLOW}IPv6 not available (IPv4-only connection){Colors.END}")
                return None
        return None
        
    except Exception as e:
        print(f"{Colors.YELLOW}IPv6 not available{Colors.END}")
        return None

def get_detailed_info(ip_address):
    """
    Fetch detailed IP information using ip-api.com
    Args: ip_address - IP address to lookup
    Returns: Dictionary containing IP information or None if error
    """
    try:
        print(f"{Colors.YELLOW}Fetching location details...{Colors.END}")

        fields = "status,message,continent,continentCode,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,query"
        url = f"http://ip-api.com/json/{ip_address}?fields={fields}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"{Colors.GREEN}Location details retrieved{Colors.END}")
                return data
            else:
                error_msg = data.get('message', 'Unknown error')
                print(f"{Colors.RED}API Error: {error_msg}{Colors.END}")
                return None
        elif response.status_code == 429:
            print(f"{Colors.RED}Error: API rate limit reached. Please wait a minute.{Colors.END}")
            return None
        else:
            print(f"{Colors.RED}Error: HTTP {response.status_code}{Colors.END}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"{Colors.RED}Error: Request timed out{Colors.END}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}Error: Connection failed{Colors.END}")
        return None
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
        return None

def get_all_ip_info():
    """
    Fetch both IPv4 and IPv6 information
    Returns: Dictionary containing all IP information or None if error
    """
    ipv4 = get_ipv4_info()
    if not ipv4:
        return None
    
    time.sleep(1) 
    
    ipv6 = get_ipv6_info()
    
    time.sleep(1)  
    
    detailed_info = get_detailed_info(ipv4)
    if not detailed_info:
        return None
    
    # Combine all information
    return {
        'ipv4': ipv4,
        'ipv6': ipv6 if ipv6 else 'Not Available',
        'network': detailed_info.get('as', 'N/A'),
        'asn': detailed_info.get('asname', 'N/A'),
        'org': detailed_info.get('org', 'N/A'),
        'city': detailed_info.get('city', 'N/A'),
        'region': detailed_info.get('regionName', 'N/A'),
        'region_code': detailed_info.get('region', 'N/A'),
        'country_name': detailed_info.get('country', 'N/A'),
        'country_code': detailed_info.get('countryCode', 'N/A'),
        'continent': detailed_info.get('continent', 'N/A'),
        'continent_code': detailed_info.get('continentCode', 'N/A'),
        'postal': detailed_info.get('zip', 'N/A'),
        'latitude': detailed_info.get('lat', 'N/A'),
        'longitude': detailed_info.get('lon', 'N/A'),
        'timezone': detailed_info.get('timezone', 'N/A'),
        'isp': detailed_info.get('isp', 'N/A'),
        'query_ip': detailed_info.get('query', 'N/A'),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def display_ip_info(data):
    """
    Display formatted IP information
    Args: data - Dictionary containing IP information
    """
    if not data:
        print(f"{Colors.RED}No data to display.{Colors.END}")
        return
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}IP INFORMATION RETRIEVED SUCCESSFULLY{Colors.END}")
    print(f"{Colors.CYAN}Timestamp: {data.get('timestamp', 'N/A')}{Colors.END}\n")
    
    # IP Addresses
    print(f"{Colors.BLUE}{Colors.BOLD}{'─'*60}")
    print("IP ADDRESSES")
    print(f"{'─'*60}{Colors.END}")
    print(f"  IPv4 Address    : {Colors.CYAN}{data.get('ipv4', 'N/A')}{Colors.END}")
    
    ipv6_status = data.get('ipv6', 'N/A')
    if ipv6_status == 'Not Available':
        print(f"  IPv6 Address    : {Colors.YELLOW}{ipv6_status}{Colors.END}")
    else:
        print(f"  IPv6 Address    : {Colors.CYAN}{ipv6_status}{Colors.END}")
    
    # Network Information
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'─'*60}")
    print("NETWORK INFORMATION")
    print(f"{'─'*60}{Colors.END}")
    print(f"  Network         : {data.get('network', 'N/A')}")
    print(f"  ASN Name        : {data.get('asn', 'N/A')}")
    print(f"  Organization    : {data.get('org', 'N/A')}")
    print(f"  ISP             : {data.get('isp', 'N/A')}")
    
    # Location Information
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'─'*60}")
    print("LOCATION INFORMATION")
    print(f"{'─'*60}{Colors.END}")
    print(f"  City            : {data.get('city', 'N/A')}")
    print(f"  Region          : {data.get('region', 'N/A')} ({data.get('region_code', 'N/A')})")
    print(f"  Country         : {data.get('country_name', 'N/A')} ({data.get('country_code', 'N/A')})")
    print(f"  Continent       : {data.get('continent', 'N/A')} ({data.get('continent_code', 'N/A')})")
    print(f"  Postal Code     : {data.get('postal', 'N/A')}")
    print(f"  Coordinates     : {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}")
    print(f"  Timezone        : {data.get('timezone', 'N/A')}")
    
    print(f"\n{Colors.BLUE}{'─'*60}{Colors.END}\n")

def save_to_file(data, file_format='json'):
    """
    Save IP information to a file
    Args: 
        data - Dictionary containing IP information
        file_format - Format to save (json or txt)
    Returns: True if successful, False otherwise
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if file_format == 'json':
            filename = f"ip_info_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        else:  # txt format
            filename = f"ip_info_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write("IP ADDRESS INFORMATION REPORT\n")
                f.write("="*60 + "\n")
                f.write(f"Generated: {data.get('timestamp', 'N/A')}\n\n")
                
                f.write("IP ADDRESSES\n")
                f.write("-"*60 + "\n")
                f.write(f"IPv4: {data.get('ipv4', 'N/A')}\n")
                f.write(f"IPv6: {data.get('ipv6', 'N/A')}\n\n")
                
                f.write("NETWORK INFORMATION\n")
                f.write("-"*60 + "\n")
                f.write(f"Network: {data.get('network', 'N/A')}\n")
                f.write(f"ASN: {data.get('asn', 'N/A')}\n")
                f.write(f"Organization: {data.get('org', 'N/A')}\n")
                f.write(f"ISP: {data.get('isp', 'N/A')}\n\n")
                
                f.write("LOCATION INFORMATION\n")
                f.write("-"*60 + "\n")
                f.write(f"City: {data.get('city', 'N/A')}\n")
                f.write(f"Region: {data.get('region', 'N/A')}\n")
                f.write(f"Country: {data.get('country_name', 'N/A')} ({data.get('country_code', 'N/A')})\n")
                f.write(f"Continent: {data.get('continent', 'N/A')}\n")
                f.write(f"Postal: {data.get('postal', 'N/A')}\n")
                f.write(f"Coordinates: {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}\n")
                f.write(f"Timezone: {data.get('timezone', 'N/A')}\n")
        
        print(f"{Colors.GREEN}Data saved to: {filename}{Colors.END}")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}Error saving file: {str(e)}{Colors.END}")
        return False

def display_menu():
    """Display main menu options"""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}MENU OPTIONS:{Colors.END}")
    print("  [1] View IP Information")
    print("  [2] Save to JSON File")
    print("  [3] Save to Text File")
    print("  [4] Refresh Data")
    print("  [5] About")
    print("  [6] Exit")
    print(f"{Colors.BLUE}{'─'*60}{Colors.END}")

def display_about():
    """Display information about the application"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}ABOUT THIS APPLICATION{Colors.END}")
    print(f"{Colors.BLUE}{'─'*60}{Colors.END}")
    print(f"  Application : IP Address Information Tool")
    print(f"  Version     : {__version__}")
    print(f"  Team        : {__author__}")
    print(f"  Date        : {__date__}")
    print(f"  Project     : DEVASC Project Activity 3 - Option 2")
    print(f"\n{Colors.YELLOW}Features:{Colors.END}")
    print("  • IPv4 and IPv6 address detection")
    print("  • Geolocation information")
    print("  • ISP and network details")
    print("  • Save results to JSON or TXT format")
    print("  • Color-coded terminal output")
    print(f"\n{Colors.YELLOW}APIs Used:{Colors.END}")
    print("  • ipify.org - IP address detection")
    print("  • ip-api.com - Geolocation and ISP data")
    print(f"{Colors.BLUE}{'─'*60}{Colors.END}\n")

def get_valid_choice():
    """
    Get and validate user input
    Returns: Valid choice string or None if invalid
    """
    valid_choices = ['1', '2', '3', '4', '5', '6']
    choice = input(f"\n{Colors.CYAN}Enter your choice (1-6): {Colors.END}").strip()
    return choice if choice in valid_choices else None

def main():
    """Main application function with menu-driven interface"""
    print_banner()
    
    ip_data = None
    
    # Welcome message
    print(f"{Colors.GREEN}Welcome! This tool will help you retrieve your public IP information.{Colors.END}")
    print(f"{Colors.YELLOW}Note: Some connections may not have IPv6 available.{Colors.END}")
    
    while True:
        display_menu()
        choice = get_valid_choice()
        
        if choice == '1':
            # View IP Information
            if ip_data is None:
                print(f"\n{Colors.CYAN}Fetching IP information...{Colors.END}\n")
                ip_data = get_all_ip_info()
            
            if ip_data:
                display_ip_info(ip_data)
            else:
                print(f"{Colors.RED}Failed to retrieve IP information. Please check your internet connection.{Colors.END}")
        
        elif choice == '2':
            # Save to JSON
            if ip_data is None:
                print(f"{Colors.YELLOW}Please fetch IP information first (Option 1).{Colors.END}")
            else:
                save_to_file(ip_data, 'json')
        
        elif choice == '3':
            # Save to TXT
            if ip_data is None:
                print(f"{Colors.YELLOW}Please fetch IP information first (Option 1).{Colors.END}")
            else:
                save_to_file(ip_data, 'txt')
        
        elif choice == '4':
            # Refresh Data
            print(f"\n{Colors.CYAN}Refreshing IP information...{Colors.END}\n")
            ip_data = get_all_ip_info()
            if ip_data:
                print(f"{Colors.GREEN}Data refreshed successfully!{Colors.END}")
                display_ip_info(ip_data)
            else:
                print(f"{Colors.RED}Failed to refresh data.{Colors.END}")
        
        elif choice == '5':
            # About
            display_about()
        
        elif choice == '6':
            # Exit
            print(f"\n{Colors.GREEN}Thank you for using IP Address Information Tool!{Colors.END}")
            print(f"{Colors.CYAN}Developed by Team Quizzle - {__date__}{Colors.END}\n")
            sys.exit(0)
        
        else:
            print(f"{Colors.RED}Invalid choice. Please enter a number between 1-6.{Colors.END}")

if __name__ == "__main__":
    """Entry point of the application"""
    try:
        # Check if requests library is installed
        import requests
        main()
    except ImportError:
        print(f"{Colors.RED}{'='*60}")
        print("ERROR: 'requests' library not found!")
        print(f"{'='*60}{Colors.END}")
        print("\nPlease install it using:")
        print(f"{Colors.CYAN}  pip install requests{Colors.END}")
        print("\nOr install all dependencies:")
        print(f"{Colors.CYAN}  pip install -r requirements.txt{Colors.END}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Program interrupted by user.{Colors.END}")
        print(f"{Colors.GREEN}Thank you for using IP Address Information Tool!{Colors.END}\n")
        sys.exit(0)