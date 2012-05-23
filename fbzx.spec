Name:		fbzx
Version:	2.9.0
Release:	%mkrel 1
Summary:	A ZX Spectrum Emulator for FrameBuffer
Group:		Emulators
License:	GPLv3+
URL:		http://www.rastersoft.com/fbzx.html
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	SDL-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pulseaudio-devel
BuildRequires:	desktop-file-utils
Suggests:	spectrum-roms

%description
FBZX is a Sinclair Spectrum emulator, designed to work at full screen using 
the FrameBuffer or under X-Windows.

For ZX Spectrum roms install spectrum-roms package from non-free repository.

%prep
%setup -q

# Patch to use rpm optflags 
sed -i -e "s/^\(CC\ =\ gcc\) [^\`]*/\1 \$(CFLAGS) /" Makefile

# Fix source file permissions
chmod 644 z80free/Z80free.c

# Remove roms as they are non-free
rm -rf spectrum-roms

%build
export CFLAGS="%{optflags}"
%make

%install
rm -rf %{buildroot}

#install application
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{name} %{buildroot}%{_bindir}

# install data
mkdir -p %{buildroot}%{_datadir}/%{name}
install -p -m 644 keymap.bmp %{buildroot}%{_datadir}/%{name}

# install icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 %{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

# install desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --remove-key=Version \
  --add-category=Emulator \
  --add-category=X-MandrivaLinux-MoreApplications-Emulators \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop

%clean
rm -rf %{buildroot}

%files
%doc AMSTRAD CAPABILITIES COPYING FAQ README* TODO VERSIONS
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop

