#!/usr/bin/env python

import os
from environment import common, docker

# ===== input =======
sl_builder_image = 'onedata/sl_builder:v2'
builder_image = 'onedata/builder'

config_dir = '/home/lichon/IdeaProjects/oneprovider/dev_scripts/cfg'

globalregistry_pkg_dir = '/home/lichon/IdeaProjects/globalregistry/rel'
globalregistry_pkg_name = 'globalregistry-Linux.x86_64.rpm'

provider_pkg_dir = '/home/lichon/IdeaProjects/oneprovider/releases'
provider_pkg_name = 'oneprovider_2.5.0.53.deb'
# ===================

dns, dns_output = common.set_up_dns('auto', 'onedata')
gr_name = 'gr_onedata'
gr = docker.run(
    image=sl_builder_image,
    hostname='gr.onedata.dev.docker',
    detach=True,
    interactive=True,
    tty=True,
    workdir='/root',
    name=gr_name,
    volumes=[(globalregistry_pkg_dir, '/root/pkg', 'ro'),
             (config_dir, '/root/cfg', 'ro')],
    dns_list=dns,
    run_params=['--privileged=true'],
    command='yum install -y pkg/' + globalregistry_pkg_name + ' && sleep 5 && onepanel_admin --install /root/cfg/gr.cfg ; bash')

provider1 = docker.run(
    image=builder_image,
    hostname='provider1.onedata.dev.docker',
    detach=True,
    interactive=True,
    tty=True,
    workdir='/root',
    name='provider1_onedata',
    volumes=[(provider_pkg_dir, '/root/pkg', 'ro'),
             (config_dir, '/root/cfg', 'ro')],
    dns_list=dns,
    link={gr_name: 'onedata.org'},
    run_params=['--privileged=true'],
    command='dpkg -i pkg/' + provider_pkg_name + ''' || apt-get -y install -f
sed -i \"s/{239, 255, 0, 1}/{238, 255, 0, 1}/g\" /opt/oneprovider/nodes/onepanel/etc/app.config
apt-get -y install libnspr4-dev
sleep 5
onepanel_admin --install /root/cfg/prov1.cfg
bash''')

provider2 = docker.run(
    image=builder_image,
    hostname='provider2.onedata.dev.docker',
    detach=True,
    interactive=True,
    tty=True,
    workdir='/root',
    name='provider2_onedata',
    volumes=[(provider_pkg_dir, '/root/pkg', 'ro'),
             (config_dir, '/root/cfg', 'ro')],
    dns_list=dns,
    link={gr_name: 'onedata.org'},
    run_params=['--privileged=true'],
    command='dpkg -i pkg/' + provider_pkg_name + ''' || apt-get -y install -f
apt-get -y install libnspr4-dev
sleep 5
onepanel_admin --install /root/cfg/prov2.cfg
bash''')

# Replace onedata.org, provider1.onedata.dev.docker, provider2.onedata.dev.docker routing in /etc/hosts
os.system("sed -i \"s/.*onedata.org$/`docker inspect --format '{{ .NetworkSettings.IPAddress }}' gr_onedata`\tonedata.org/g\" /etc/hosts")
os.system("sed -i \"s/.*provider1.onedata.dev.docker$/`docker inspect --format '{{ .NetworkSettings.IPAddress }}' provider1_onedata`\tprovider1.onedata.dev.docker/g\" /etc/hosts")
os.system("sed -i \"s/.*provider2.onedata.dev.docker$/`docker inspect --format '{{ .NetworkSettings.IPAddress }}' provider2_onedata`\tprovider2.onedata.dev.docker/g\" /etc/hosts")

print([gr, provider1, provider2])