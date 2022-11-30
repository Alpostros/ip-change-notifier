import sys, subprocess, os
import schedule, time
import sendmail
import uuid
from datetime import date

today = date.today()
dt = today.strftime("%b-%d-%Y")
current_ip_address = str(sys.argv[1])

def create_vpn_profile():
    profile_name = uuid.uuid4().hex + dt # Random name with date for VPN profile name
    profile_password = "verysecure"
    profile_ttl = "1080"
    os.system("pivpn add -n "+profile_name+" -p "+profile_password+" -d "+ profile_ttl)
    return profile_name, profile_password

def check_ip_address():
    global current_ip_address
    proc=subprocess.Popen("dig +short txt ch whoami.cloudflare @1.0.0.1", shell=True, stdout=subprocess.PIPE, )
    latest_ip_address = str(proc.communicate()[0])
    latest_ip_address = latest_ip_address.split("\"")[1]

    if latest_ip_address != current_ip_address:
        current_ip_address = latest_ip_address
        profile_name, profile_password = create_vpn_profile()
        print("IP Address has been changed, notifying master")
        sendmail.prep_mail(latest_ip_address, profile_name, profile_password)

    else:
        print("IP Address unchanged.")

schedule.every(15).seconds.do(check_ip_address)
while(True):
    schedule.run_pending()
    time.sleep(1)
