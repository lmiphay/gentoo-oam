
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

FILES=\
	oam-clean \
	oam-depclean \
	oam-emptytree \
	oam-fetch \
	oam-flow \
	oam-glsa \
	oam-kernel \
	oam-layman \
	oam-merge \
	oam-mussh \
	oam-newuse \
	oam-qcheck \
	oam-sync \
	oam-unmask-write \
	oam-unused \
	oam-update

.PHONY: install
install:
	install -d $(DESTDIR)/usr/sbin
	for i in $(FILES); do install $$i $(DESTDIR)/usr/sbin || exit 1; done
