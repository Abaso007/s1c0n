## 1.1: importing dependencies
from os import path, system, getcwd
import os.path, subprocess, nmap, json, sys, time, re, importlib

# Check if a module is installed, and if not, install it
def check_module(module_name, package_name):
    try:
        importlib.import_module(module_name)
    except ImportError:
        print(f"\n\t   [!] Error on import {module_name}")
        user = os.getuid()
        if user != 0:
            print(f"{co.r}{co.bo}[!] {module_name} module is missing, run me with sudo i will install it{co.re}")
        os.system(f"pip3 install {package_name}")

# Check and install required modules
check_module("nmap", "python-nmap")
check_module("requests", "requests")
check_module("json", "json")

## 1.2: defining classes & functions:
class co:
    re = "\33[0m"
    bo = "\33[1m"
    r = "\33[31m"
    g = "\33[32m"
    ye = "\33[33m"


## 1.4 checking dependencies tools
def check(tool):
    if os.path.exists(f"/usr/bin/{tool}"):
        print(f"{co.g}{co.bo}[*] {tool} exist{co.re}")
        time.sleep(0.2)
    else:
        # checking user privileges
        user = os.getuid()

        if user != 0:
            print(f"{co.r}{co.bo}[!] {tool} is missing, Please run me with sudo to install {tool}{co.re}")
            exit()
        # installing missing requirements
        print(f"{co.r}{co.bo}[!] {tool} missing{co.re}")
        print(f"{co.r}{co.bo}[!] installing {tool}{co.re}")
        time.sleep(0.2)
        system(f"apt install {tool} -y")


# requirements
list_tool = ['nmap','wafw00f','sublist3r','subfinder','assetfinder','amass','dirsearch','httprobe']
for tool in list_tool:
    check(tool)


def break_and_help():
    print("\n\t   [?] Usage example: sicon -u target.com")
    exit()


def remove_list_files(extension):
    system(f"rm -rf .list*.{extension}")


## 1.4: preparing everything
saving_path = f"{getcwd()}/"
port_scan = nmap.PortScanner()


## 1.5: "welcome" screen
system("clear")
print(co.g + co.bo + """
\t          ┏━┓╺┓ ┏━╸┏━┓┏┓╻
\t          ┗━┓ ┃ ┃  ┃┃┃┃┗┫
\t          ┗━┛╺┻╸┗━╸┗━┛╹ ╹ v1.5 (not finish yet)
                
                    Simple Recon
          Coded by """ + co.re+ co.r + co.bo + """root@x-krypt0n-x A.K.A x0r""" + co.r + co.bo + """\n\t          System of Pekalongan""" +
co.re)

## 1.6: getting started
command_arguments = sys.argv[1:]

if (len(command_arguments) > 0):
    flag = command_arguments[0].upper()

    if flag in ["-U", "--URL"]:
        URL_TARGET = command_arguments[1]

    else:
        break_and_help()

else:
    break_and_help()


os.mkdir(f"report_{URL_TARGET}")
## 2.0: Starting recon phase:
print(co.bo + co.g + "\n\t[*] Starting recon on %s:" % URL_TARGET + co.re)

## 2.1: Detect WAF using wafw00f:
# convert to domain using httprobe
get_host = subprocess.check_output(
    f"echo {URL_TARGET} | httprobe -prefer-https", shell=True, text=True
)
detect_waf = subprocess.check_output(
    f"wafw00f {get_host} > /dev/null", shell=True, text=True
)

if ("is behind" in detect_waf):
	## has some WAF
	processed_string = detect_waf[detect_waf.find("is behind"):]
	pre_parser  = processed_string.find("\x1b[1;96m") # process to get valuable results only
	post_parser = processed_string.find("\x1b[0m")
	which_waf   = processed_string[pre_parser:post_parser] # don't include color codes

	print(co.bo + co.g + "\n\t  [+] WAF: DETECTED [ %s ]" % which_waf + co.re)

elif ("No WAF detected" in detect_waf):
	print(co.bo + co.ye + "\n\t  [+] WAF: NOT DETECTED" + co.re)

else:
	print(co.bo + co.r  + "\n\t  [!] FAIL TO DETECT WAF" + co.re)

### 2.2: Scanning ports using nmap
# run NMAP and filter results using GREP
system(f"nmap {URL_TARGET} -o .list_NMAP.txt > /dev/null")
system("cat .list_NMAP.txt | grep open > .list_PORTS.txt")

# open file we just created
with open(".list_PORTS.txt", encoding="utf-8") as file:
	ports_list = file.read().splitlines()

# remove files we just created
remove_list_files("txt")

print(co.bo + co.g + "\n\t  [+] OPENED PORTS: %s" % len(ports_list) + co.re)

for p in ports_list:
	print(co.re+ "\t    " + co.g + "-> " + co.re+ co.bo + p)

### 2.3: Getting subdomains
# this process might take a while, we'll use different scripts for that
system(f"subfinder -d {URL_TARGET} -o .list_subfinder.txt -silent > /dev/null")
system(f"sublist3r -d {URL_TARGET} -o .list_sublist3r.txt > /dev/null")
system(f"assetfinder {URL_TARGET} > .list_assetfinder.txt")
system(f"amass enum -d {URL_TARGET} -o .list_amass.txt -silent")

# concat every output into one file
system("cat .list*.txt > .list_subdomains.txt")

# open "general" file
with open(".list_subdomains.txt", encoding="utf-8") as file:
	subdomain_raw_list = file.read().splitlines()

# drop duplicates
subdomain_list = set(subdomain_raw_list)

cpanel_subdomain = [subdomain_list for subdomain_list in subdomain_list if subdomain_list.startswith(("cpanel.", "webdisk.", "webmail.", "cpcontacts.", "whm.", "autoconfig.", "mail.", "cpcalendars.", "autodiscover."))]

not_cpanel_subdomain = [subdomain_list for subdomain_list in subdomain_list if not subdomain_list.startswith(("cpanel.", "webdisk.", "webmail.", "cpcontacts.", "whm.", "autoconfig.", "mail.", "cpcalendars.", "autodiscover."))]

# Save cpanel subdomains to file
with open(os.path.join(f"report_{URL_TARGET}", "cpanel_subdomain.txt"), "w") as f:
    f.write("\n".join(cpanel_subdomain))

# Save other subdomains to file, creating the file if it does not exist
with open(os.path.join(f"report_{URL_TARGET}", "subdomain.txt"), "w") as f:
    if not_cpanel_subdomain:
        f.write("\n".join(not_cpanel_subdomain))
    else:
        f.write("")

remove_list_files("txt")

print(co.bo + co.g + "\n\t  [+] SUBDOMAINS DETECTED: %s" % len(subdomain_list) + co.re)

for s in subdomain_list:

    # perform quick port scan using nmap
    quick_scan = port_scan.scan(hosts=s, arguments="-F")
    host = list(quick_scan["scan"].keys())

    if host:
        # tcp ports were found
        tcp_open = str(list(quick_scan["scan"][host[0]]["tcp"].keys()))
        print(co.re+ co.g + "\t    -> " + co.re+ co.bo + s +
        								" | " +  co.g + tcp_open + co.re)
    else:
        # port scan failed
        print(co.re+ co.g + "\t    -> " + co.re+ co.bo + s +
        								" | " +  co.r + "HOST OFFLINE" + co.re)

### checking cms 2.4:
wp_regex = re.compile(r'wp-')
joomla_regex = re.compile(r'joomla')

print(co.bo + co.g + "\n\t  [+] CMS DETECTEION: " + co.re)

for url in not_cpanel_subdomain:
    try:
        response = requests.get(f'http://{url}', timeout=5)
        if response.status_code == 200:
            text = response.text
            if wp_regex.search(text):
                print(co.re + co.g + "\t    -> " + co.re+ co.bo + url +" | Wordpress" + co.re)
                with open(os.path.join(f"report_{URL_TARGET}", "wp.txt"), "a") as f:
                    f.write(f"http://{url}" + "\n")
            elif joomla_regex.search(text):
                print(co.re + co.g + "\t    -> " + co.re+ co.bo + url +" | Joomla" + co.re)
                with open(os.path.join(f"report_{URL_TARGET}", "joomla.txt"), "a") as f:
                    f.write(f"http://{url}" + "\n")
            else:
                print(co.re + co.g + "\t    -> " + co.re+ co.bo + url +" | " +  co.r + "FAIL DETECT CMS" + co.re)
        else:
            print(co.re + co.g + "\t    -> " + co.re+ co.bo + url +" | " +  co.r + "HOST OFFLINE WITH CODE "+ str(response.status_code) + co.re)
    except requests.exceptions.RequestException as e:
        print(co.re + co.g + "\t    -> " + co.re+ co.bo + url +" | " +  co.r + "COULD NOT BE REACHED " + co.re)

### 2.5: Bruteforcing json_directory:
system(
    f"dirsearch -u {URL_TARGET} -o {saving_path}.list_json_directory.json --format=json > /dev/null"
)

with open(".list_json_directory.json", encoding="utf-8") as file:
	json_directory = json.load(file)

remove_list_files("json")

host      = str( list(json_directory["results"][0].keys())[0] )
directory = json_directory["results"][0][host]

dir_list = []
for d in directory:
    path = d["path"]
    status = d["status"]

    	# drop other codes
    if status in [200, 403]:
        dir_list.append([status, path])

sorted_directories = sorted(dir_list)

print(co.bo + co.g + "\n\t  [+] DIRECTORIES: %s" % len(sorted_directories) + co.re)

for d in sorted_directories:

	format_host = get_host.replace("\n", "")

	if (d[0] == 200):
		# g alert
		print(co.g + "\t    -> " + co.re+ co.g
				+ str(d[0]) + co.re+ " | " +  co.bo + format_host + d[1] + co.re)

	elif (d[0] == 403):
		print(co.g + "\t    -> " + co.re+ co.ye 
				+ str(d[0]) + co.re+ " | " +  co.bo + format_host + d[1] + co.re)
