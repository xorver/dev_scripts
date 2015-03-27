About
=====

Scripts for starting demo environment.

Getting Started
---------------

1. Run make to build docker **sl_builder** and **builder**
2. Prepare globalregistry rpm (run on cloud: 'make rpm', or take it from 'scp -i ~/.ssh/id_bamboo root@172.16.67.107:~/globalregistry-Linux.x86_64.rpm .')
3. Prepare oneprovider deb ('./make.py --image onedata/builder:v7 deb', make.py from this package can be used)
4. Add routing for **onedata.org**, **provider1.onedata.dev.docker**, **provider2.onedata.dev.docker** to /etc/hosts, IPs can be set to 127.0.0.1, as they get overridden by script
5. Edit **bamboos/docker/demo_up.py** input vars
6. Kill all dockers: 'docker kill $(docker ps -q) ; docker rm $(docker ps -aq)'
7. Run 'sudo ./bamboos/docker/demo.up'
8. You may chceck logs, or attach to **gr.onedata.dev.docker**, **provider1.onedata.dev.docker** **provider2.onedata.dev.docker** dockers, installation takes a while
9. 'https://onedata.org' is up, 'https://provider1.onedata.dev.docker:9443' and 'https://provider2.onedata.dev.docker:9443' need registration.

NOTE:
onedata.org will redirect you to 'https://[alias].onedata.org/[...]'. You need either redirect this to adequate IP, or replace '[alias].onedata.org' with 'provider1.onedata.dev.docker' manually

