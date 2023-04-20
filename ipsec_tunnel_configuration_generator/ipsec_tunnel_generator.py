import jinja2
import json
import os
import random
import string

template_file = "ipsec_tunnel_template.j2"
json_parameter_file = "ipsec_tunnel.json"
output_directory = "output"

# read the contents from the JSON files
print("Read JSON parameter file...")
config_parameters = json.load(open(json_parameter_file))

# Generate info to complete our template
local = config_parameters['firewalls'][0]
remote = config_parameters['firewalls'][1]
local_ike_crypto_profile = f"{local['site']}-{remote['site']}-IKE-Crypto"
remote_ike_crypto_profile = f"{remote['site']}-{local['site']}-IKE-Crypto"
local_ipsec_crypto_profile = f"{remote['site']}-IPSEC-Crypto"
remote_ipsec_crypto_profile = f"{local['site']}-IPSEC-Crypto"
local_ike_gateway = f"{local['site']}-{remote['site']}-IKE-GW"
remote_ike_gateway = f"{remote['site']}-{local['site']}-IKE-GW"
local_ipsec_tunnel = f"{local['site']}-{remote['site']}-IPSEC-Tunnel"
remote_ipsec_tunnel = f"{remote['site']}-{local['site']}-IPSEC-Tunnel"
local_zone = f"VPN-{local['site']}-{remote['site']}"
remote_zone = f"VPN-{remote['site']}-{local['site']}"

config_parameters['firewalls'][0]['ike_crypto_profile'] = local_ike_crypto_profile
config_parameters['firewalls'][1]['ike_crypto_profile'] = remote_ike_crypto_profile
config_parameters['firewalls'][0]['ipsec_crypto_profile'] = local_ipsec_crypto_profile
config_parameters['firewalls'][1]['ipsec_crypto_profile'] = remote_ipsec_crypto_profile
config_parameters['firewalls'][0]['ike_gateway'] = local_ike_gateway
config_parameters['firewalls'][1]['ike_gateway'] = remote_ike_gateway
config_parameters['firewalls'][0]['ipsec_tunnel'] = local_ipsec_tunnel
config_parameters['firewalls'][1]['ipsec_tunnel'] = remote_ipsec_tunnel
config_parameters['firewalls'][0]['zone'] = local_zone
config_parameters['firewalls'][1]['zone'] = remote_zone

print("Create Jinja2 environment...")
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."),
                         trim_blocks=True,
                         lstrip_blocks=True)
tunnel_template = env.get_template(template_file)

#Generate pre-shared-key using random generator
length = 16
lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits
all = lower + upper + num 
temp = random.sample(all,length)
pre_shared_key = "".join(temp)
config_parameters['firewalls'][0]['pre_shared_key'] = pre_shared_key
config_parameters['firewalls'][1]['pre_shared_key'] = pre_shared_key

# we will make sure that the output directory exists
if not os.path.exists(output_directory):
    os.mkdir(output_directory)
# now create the templates
print("Generating Firewall Configuration...")

for firewall in config_parameters['firewalls']:
    result = tunnel_template.render(firewall)
    f = open(os.path.join(output_directory, firewall['hostname'] + ".conf"), "w")
    f.write(result)
    f.close()
    print("Configuration '%s' created..." % (firewall['hostname'] + ".conf"))


