%global debug_package %{nil}
%global __os_install_post %{nil}
%global _build_id_links none
%global __strip /bin/true
AutoReqProv: no

Name:           packettracer
Version:        9.0.1
Release:        1%{?dist}
Summary:        Cisco Packet Tracer
License:        Proprietary
ExclusiveArch:  x86_64
Source0:        packettracer-%{version}
Requires:       fuse-libs, libzstd, pcre2, xdg-utils, gtk-update-icon-cache
Vendor:		Cisco Systems
URL:		https://www.netacad.com

%description
Cisco Packet Tracer 9.0.1

%prep

%build

%install
mkdir -p %{buildroot}/opt/pt
install -m 0755 %{SOURCE0}/opt/pt/packettracer.AppImage \
    %{buildroot}/opt/pt/packettracer.AppImage

mkdir -p %{buildroot}%{_bindir}
ln -s /opt/pt/packettracer.AppImage %{buildroot}%{_bindir}/packettracer

%files
%dir /opt/pt
%attr(0755,root,root) /opt/pt/packettracer.AppImage
%{_bindir}/packettracer

%post
echo "ATTENTION! Run this command in Command Line for activated EULA: packettracer --pt-activate"

%postun
if [ "$1" -eq 0 ]; then
    getent passwd | awk -F: '$3 >= 1000 && $3 < 60000 {print $1":"$6}' | while IFS=: read -r user home; do
        d="$home/.local/share"
        [ -d "$d" ] || continue

        # desktop entry
        rm -f "$d/applications/CiscoPacketTracer-9.0.1.desktop"
        rm -f "$d/applications/CiscoPacketTracerPtsa-9.0.1.desktop"

        # MIME: source and result compilation
        rm -f "$d"/mime/packages/cisco-pka.xml "$d"/mime/packages/cisco-pks.xml \
              "$d"/mime/packages/cisco-pksz.xml "$d"/mime/packages/cisco-pkt.xml \
              "$d"/mime/packages/cisco-pkz.xml
        rm -f "$d"/mime/application/x-pka.xml "$d"/mime/application/x-pks.xml \
              "$d"/mime/application/x-pksz.xml "$d"/mime/application/x-pkt.xml \
              "$d"/mime/application/x-pkz.xml

        # icon applications and icon MIME
        find "$d/icons" \( -type f -o -type l \) \( \
            -name 'Cisco_Packet_Tracer*' -o \
            -name 'application-x-pka.png' -o -name 'application-x-pks.png' -o \
            -name 'application-x-pksz.png' -o -name 'application-x-pkt.png' -o \
            -name 'application-x-pkz.png' -o \
            -name 'gnome-mime-application-x-pka.png' -o -name 'gnome-mime-application-x-pks.png' -o \
            -name 'gnome-mime-application-x-pksz.png' -o -name 'gnome-mime-application-x-pkt.png' -o \
            -name 'gnome-mime-application-x-pkz.png' \) -delete 2>/dev/null

        for t in gnome Adwaita hicolor; do
            td="$d/icons/$t"
            [ -d "$td" ] || continue
            find "$td" -depth -type d -empty -delete 2>/dev/null
            [ -d "$td" ] || continue
            others=$(find "$td" \( -type f -o -type l \) ! -name icon-theme.cache ! -name index.theme | wc -l)
            if [ "$others" -eq 0 ]; then
                rm -f "$td/icon-theme.cache"
                [ -L "$td/index.theme" ] && rm -f "$td/index.theme"
                find "$td" -depth -type d -empty -delete 2>/dev/null
            fi
        done

        runuser -u "$user" -- update-mime-database "$d/mime" >/dev/null 2>&1 || true
        runuser -u "$user" -- update-desktop-database "$d/applications" >/dev/null 2>&1 || true

	rm -rf "$home/.local/.packettracer"
	rm -rf "$home"/.local/.CiscoPacketTracer-*-log.txt

    done
fi

%changelog
* Thu Nov 19 2026 Mulky Fauzan <qapkyy3@gmail.com> - 9.0.1-1
- Repackage from .deb
