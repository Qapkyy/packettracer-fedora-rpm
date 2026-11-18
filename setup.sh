sudo dnf install -y rpm-build rpmdevtools binutils tar xz zstd
ar x $1
mkdir control data
for i in control data; do tar -xJvf $i.tar.xz -C $i; done
for i in _gpg* debian* *.tar.xz; do rm $i; done
rpmdev-setuptree
cp packettracer.spec ~/rpmbuild/SPECS/.
mkdir -p ~/rpmbuild/SOURCES/packettracer-9.0.1
cp -a data/* ~/rpmbuild/SOURCES/packettracer-9.0.1
rpmbuild -bb ~/rpmbuild/SPECS/packettracer.spec
mv "$(find ~/rpmbuild -name packettracer*.rpm)" .
rm -rf control data
clear
echo "Done :)"
echo "If you're not packager redhat ecosystem, please rm -rf ~/rpmbuild. Manual..."
