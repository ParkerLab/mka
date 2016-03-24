APP = mka
CAPAPP = MKA
VERSION = 0.1.2
MODULEFILES_ROOT = /lab/sw/modulefiles
MODULES_ROOT = /lab/sw/modules
PREFIX = $(MODULES_ROOT)/$(APP)/$(VERSION)
MODULEFILE = $(MODULEFILES_ROOT)/$(APP)/$(VERSION)

define MODULEFILE_TEMPLATE
#%Module1.0
set           version          $(VERSION)
set           app              $(APP)
set           modroot          $(MODULES_ROOT)/$$app/$$version
setenv        $(CAPAPP)_MODULE $$modroot

prepend-path  PATH             $$modroot/bin

conflict      $(APP)

module-whatis "ParkerLab analysis template $$version."
module-whatis "URL:  https://github.com/ParkerLab/$$app"
module-whatis "Installation directory: $$modroot"
endef
export MODULEFILE_TEMPLATE


install:
	@mkdir -p $(PREFIX)/bin $(PREFIX)/template
	@install -m 0755 bin/* $(PREFIX)/bin
	@rsync -a template/ $(PREFIX)/template
	@find $(PREFIX)/template -type d -exec chmod 755 {} \;
	@find $(PREFIX)/template -type f -exec chmod 644 {} \;

	@mkdir -p `dirname $(MODULEFILE)`
	@echo "$$MODULEFILE_TEMPLATE" > $(MODULEFILE)
