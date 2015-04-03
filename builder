FROM onedata/base:v5
MAINTAINER Konrad Zemek <konrad.zemek@gmail.com>

# Add custom package sources
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 828AB726
RUN curl -L http://llvm.org/apt/llvm-snapshot.gpg.key | apt-key add -
RUN echo 'deb http://ppa.launchpad.net/george-edison55/cmake-3.x/ubuntu utopic main' > /etc/apt/sources.list.d/cmake.list
RUN echo 'deb http://llvm.org/apt/trusty/ llvm-toolchain-trusty-3.6 main' > /etc/apt/sources.list.d/llvm.list
ADD http://toolkit.globus.org/ftppub/gt6/installers/repo/globus-toolkit-repo_latest_all.deb /root/globus-toolkit-repo_latest_all.deb
RUN dpkg -i /root/globus-toolkit-repo_latest_all.deb

# Install development packages
RUN apt-get update && \
    apt-get install -y clang-3.6 cmake doxygen elixir erlang erlang-src gdb \
                       libboost-all-dev libbotan1.10-dev libfuse-dev \
                       libglobus-common-dev libglobus-gsi-callback-dev \
                       libltdl-dev libprotobuf-dev libpython-dev \
                       libstdc++-4.9-dev libtbb-dev lldb-3.6 ninja-build \
                       pkg-config protobuf-compiler python-dev python-sphinx \
                       rpm subversion build-essential devscripts debhelper libboost1.55-all-dev  && \
    apt-get clean

# Set up the environment
ENV CC=clang-3.6 CXX=clang++-3.6
RUN update-alternatives --install /usr/bin/cc  cc  /usr/bin/clang-3.6   100 && \
    update-alternatives --install /usr/bin/c++ c++ /usr/bin/clang++-3.6 100
RUN echo '    StrictHostKeyChecking no'     >> /etc/ssh/ssh_config && \
    echo '    UserKnownHostsFile /dev/null' >> /etc/ssh/ssh_config
