#!/bin/bash
# vim: set et ts=4 sw=4 noai relativenumber:

WORKDIR=$(pwd)

rm -rfv "$WORKDIR/dist"
rm -rfv ~/RPM

__install_rpm_build() {
    sudo apt-get update
    sudo apt-get install -y rpm-build
}

__install_rpmdevtools() {
    sudo apt-get update
    sudo apt-get install -y rpmdevtools
}

__install_prereq() {
    rpm --quiet -q rpm-build || __install_rpm_build
    rpm --quiet -q rpmdevtools || __install_rpmdevtools
    [ ! -f /usr/lib/rpm/check-buildroot ] && {
        sudo curl -qLo /usr/lib/rpm/check-buildroot https://raw.githubusercontent.com/rpm-software-management/rpm/refs/heads/master/scripts/check-buildroot; sudo chmod +x /usr/lib/rpm/check-buildroot;
    }
}

__make_hier() {
    cd "${WORKDIR}/dist"
    rpmdev-setuptree
    ln -s ~/RPM rpmbuild
    cd -
}

__copy_files() {
    cp -vf * "${WORKDIR}/dist/rpmbuild/SOURCES/"
    rm -vf "${WORKDIR}/dist/rpmbuild/SOURCES/build.sh"
    mv -vf "${WORKDIR}/dist/rpmbuild/SOURCES/c2-ec2-netutils.spec" "${WORKDIR}/dist/rpmbuild/SPECS/"
}

__build_dist() {
    cd "${WORKDIR}/dist"
    rpmbuild -ba rpmbuild/SPECS/c2-ec2-netutils.spec
    cd -
}

set -x

__install_prereq

mkdir -p "${WORKDIR}/dist"
__make_hier
__copy_files
__build_dist

set +x

echo; echo
echo "Done!"
ls -1 ${WORKDIR}/dist/rpmbuild/RPMS/*/*.rpm
echo; echo
