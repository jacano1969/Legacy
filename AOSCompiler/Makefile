# Makefile for aoscompiler
# By: lithid
SHELL := /bin/bash
NAME := aoscompiler
VERSION := $(shell grep "Version" share/desktop/$(NAME).desktop |cut -d"=" -f2)
TYPE := $(shell dpkg-architecture |grep "DEB_BUILD_ARCH=" |cut -d"=" -f2)

# Help
help:
	@echo
	@echo "//* $(NAME): $(VERSION)-$(TYPE) *\\"
	@echo
	@echo "Usage: make"
	@echo "debian or [deb-pack|deb-build|deb-clean]"
	@echo "archlinux or [arch-pack|arch-build|arch-clean]"
	@echo

# Definitions
debian: deb-pack deb-install deb-clean
archlinux: arch-pack arch-install arch-clean

#
# Start debian setup
#
deb-pack:
ifeq ($(wildcard /etc/debian_version),)
	@echo "Not debian, leaving"
	exit 1
else
	@echo "Building $(NAME): $(VERSION)-$(TYPE)"
	-dpkg-buildpackage -rfakeroot
endif

deb-install:
ifeq ($(wildcard /etc/debian_version),)
	@echo "Not debian, leaving"
	exit 1
else
	@echo "Installing $(NAME): $(VERSION)-$(TYPE)"
	-sudo dpkg -i ../${NAME}_${VERSION}_${TYPE}.deb
endif

deb-clean:
ifeq ($(wildcard /etc/debian_version),)
	@echo "Not debian, leaving"
	exit 1
else
	@echo "Cleaning up $(NAME): $(VERSION)-$(TYPE)"
	-rm -rf debian/$(NAME)
	-rm -rf debian/$(NAME).substvars
	-rm -rf debian/*.log
	-rm -rf debian/files
	-rm -rf debian/*debhelper
	-rm -rf ../$(NAME)_*
endif

#
# Start archlinux setup
#
arch-pack:
ifeq ($(wildcard /etc/rc.conf),)
	@echo "Not archlinux, leaving"
	exit 1
else
	@echo "Building $(NAME): $(VERSION)-$(TYPE)"
	-export VERZ=$(VERSION); cd archlinux/; makepkg; cd ../
endif

arch-install:
ifeq ($(wildcard /etc/rc.conf),)
	@echo "Not archlinux, leaving"
	exit 1
else
	@echo "Installing $(NAME): $(VERSION)-$(TYPE)"
	-sudo pacman -U archlinux/*tar.xz
endif

arch-clean:
ifeq ($(wildcard /etc/rc.conf),)
	@echo "Not archlinux, leaving"
	exit 1
else
	@echo "Cleaning up $(NAME): $(VERSION)-$(TYPE)"
endif

