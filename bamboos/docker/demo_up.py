#!/usr/bin/env python

import os
from environment import common, docker

uid = common.generate_uid()
dns, dns_output = common.set_up_dns('auto', 'onedata')

gr_name = 'gr_onedata'
gr = docker.run(
    image='onedata/sl_builder:v1',
    hostname='gr.onedata.dev.docker',
    detach=True,
    interactive=True,
    tty=True,
    workdir='/root',
    name=gr_name,
    volumes=[('/home/lichon/IdeaProjects/globalregistry/packages', '/root/pkg', 'ro'),
             ('/home/lichon/IdeaProjects/oneprovider/dev_scripts/cfg', '/root/cfg', 'ro')],
    dns_list=dns,
    # link={db_dockername: db_hostname},
    command='yum install -y pkg/globalregistry-Linux.x86_64.rpm && sleep 5 && onepanel_admin --install /root/cfg/gr.cfg ; bash')

provider1 = docker.run(
    image='onedata/worker',
    hostname='provider1.onedata.dev.docker',
    detach=True,
    interactive=True,
    tty=True,
    workdir='/root',
    name='provider1_onedata',
    volumes=[('/home/lichon/IdeaProjects/oneprovider/releases', '/root/pkg', 'ro'),
             ('/home/lichon/IdeaProjects/oneprovider/dev_scripts/cfg', '/root/cfg', 'ro')],
    dns_list=dns,
    link={gr_name: 'onedata.org'},
    command='''dpkg -i pkg/oneprovider_2.5.0.6.deb || apt-get -y install -f
sed -i \"s/{239, 255, 0, 1}/{238, 255, 0, 1}/g\" /opt/oneprovider/nodes/onepanel/etc/app.config
apt-get -y install libnspr4-dev
sleep 5
onepanel_admin --install /root/cfg/prov1.cfg
bash''')

provider2 = docker.run(
    image='onedata/worker',
    hostname='provider2.onedata.dev.docker',
    detach=True,
    interactive=True,
    tty=True,
    workdir='/root',
    name='provider2_onedata',
    volumes=[('/home/lichon/IdeaProjects/oneprovider/releases', '/root/pkg', 'ro'),
             ('/home/lichon/IdeaProjects/oneprovider/dev_scripts/cfg', '/root/cfg', 'ro')],
    dns_list=dns,
    link={gr_name: 'onedata.org'},
    command='''dpkg -i pkg/oneprovider_2.5.0.6.deb || apt-get -y install -f
apt-get -y install libnspr4-dev
sleep 5
onepanel_admin --install /root/cfg/prov2.cfg
bash''')

os.system("sed -i \"s/.*onedata.org$/`docker inspect --format '{{ .NetworkSettings.IPAddress }}' gr_onedata`\tonedata.org/g\" /etc/hosts")
os.system("sed -i \"s/.*provider1.onedata.dev.docker$/`docker inspect --format '{{ .NetworkSettings.IPAddress }}' provider1_onedata`\tprovider1.onedata.dev.docker/g\" /etc/hosts")
os.system("sed -i \"s/.*provider2.onedata.dev.docker$/`docker inspect --format '{{ .NetworkSettings.IPAddress }}' provider2_onedata`\tprovider2.onedata.dev.docker/g\" /etc/hosts")

print([gr, provider1, provider2])