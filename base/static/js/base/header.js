document.addEventListener("DOMContentLoaded", function() {
    const nav = document.querySelector(".main-nav");
    const mobileToggle = nav?.querySelector(".main-nav__mobile-toggle");
    const mobilePanel = nav?.querySelector(".main-nav__mobile-panel");
    const dropdowns = document.querySelectorAll(".main-nav__dropdown");
    const mobileBreakpoint = window.matchMedia("(max-width: 1200px)");
    const hoverCloseTimers = new WeakMap();

    function setDropdownExpanded(dropdown, expanded) {
        dropdown.querySelectorAll("[aria-expanded]").forEach(function(toggle) {
            toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
        });
    }

    function hasStateValue(state, key) {
        return Object.prototype.hasOwnProperty.call(state, key);
    }

    function setDropdownState(dropdown, state) {
        if (hasStateValue(state, "open")) {
            dropdown.classList.toggle("is-open", state.open);
        }

        if (hasStateValue(state, "hovered")) {
            dropdown.classList.toggle("is-hovered", state.hovered);
        }

        setDropdownExpanded(
            dropdown,
            dropdown.classList.contains("is-open") || dropdown.classList.contains("is-hovered")
        );
    }

    function closeDropdown(dropdown) {
        setDropdownState(dropdown, { open: false, hovered: false });
    }

    function closeHoverDropdown(dropdown) {
        setDropdownState(dropdown, { hovered: false });
    }

    function openClickDropdown(dropdown) {
        setDropdownState(dropdown, { open: true });
    }

    function openHoverDropdown(dropdown) {
        setDropdownState(dropdown, { hovered: true });
    }

    function closeOtherDropdowns(currentDropdown) {
        dropdowns.forEach(function(dropdown) {
            if (dropdown !== currentDropdown) {
                closeDropdown(dropdown);
            }
        });
    }

    function clearHoverCloseTimer(dropdown) {
        window.clearTimeout(hoverCloseTimers.get(dropdown));
        hoverCloseTimers.delete(dropdown);
    }

    function scheduleHoverClose(dropdown) {
        clearHoverCloseTimer(dropdown);

        hoverCloseTimers.set(
            dropdown,
            window.setTimeout(function() {
                closeHoverDropdown(dropdown);
                hoverCloseTimers.delete(dropdown);
            }, 220)
        );
    }

    function getActiveDropdown(currentDropdown) {
        return Array.from(dropdowns).find(function(dropdown) {
            return dropdown !== currentDropdown
                && (
                    dropdown.classList.contains("is-open")
                    || dropdown.classList.contains("is-hovered")
                );
        });
    }

    function setMobileMenu(open, animate = true) {
        if (!nav || !mobileToggle) {
            return;
        }

        nav.classList.toggle("is-mobile-animated", animate);
        nav.classList.toggle("is-mobile-open", open);
        document.body.classList.toggle("main-nav-open", open);
        mobileToggle.setAttribute("aria-expanded", open ? "true" : "false");
        mobileToggle.setAttribute("aria-label", open ? "Закрыть меню" : "Открыть меню");

        if (!open) {
            dropdowns.forEach(closeDropdown);
        }
    }

    function toggleDropdown(dropdown, toggle) {
        const shouldOpen = !dropdown.classList.contains("is-open");

        closeOtherDropdowns(dropdown);

        if (shouldOpen) {
            clearHoverCloseTimer(dropdown);
            openClickDropdown(dropdown);
        } else {
            closeDropdown(dropdown);
            toggle.blur();
        }
    }

    function scheduleDesktopHoverClose(dropdown) {
        if (!mobileBreakpoint.matches && !dropdown.classList.contains("is-open")) {
            scheduleHoverClose(dropdown);
        }
    }

    function keepActiveDropdownOpen(dropdown) {
        if (mobileBreakpoint.matches) {
            return;
        }

        const activeDropdown = getActiveDropdown(dropdown);
        if (activeDropdown) {
            clearHoverCloseTimer(activeDropdown);
        }
    }

    function openDesktopHoverDropdown(dropdown) {
        if (mobileBreakpoint.matches) {
            return;
        }

        const activeDropdown = getActiveDropdown(dropdown);
        if (activeDropdown) {
            clearHoverCloseTimer(activeDropdown);
            closeDropdown(activeDropdown);
        }

        clearHoverCloseTimer(dropdown);
        closeOtherDropdowns(dropdown);
        openHoverDropdown(dropdown);
    }

    function closeActiveDropdownOnDesktop(dropdown) {
        if (mobileBreakpoint.matches) {
            return;
        }

        const activeDropdown = getActiveDropdown(dropdown);
        if (activeDropdown) {
            clearHoverCloseTimer(activeDropdown);
            closeDropdown(activeDropdown);
        }
    }

    function setupMegaDropdown(dropdown, toggle, megaMenu) {
        dropdown.addEventListener("mouseenter", function() {
            keepActiveDropdownOpen(dropdown);
        });

        toggle.addEventListener("mouseenter", function() {
            openDesktopHoverDropdown(dropdown);
        });

        toggle.addEventListener("mouseleave", function() {
            scheduleDesktopHoverClose(dropdown);
        });

        megaMenu.addEventListener("mouseenter", function() {
            if (!mobileBreakpoint.matches) {
                clearHoverCloseTimer(dropdown);
            }
        });

        megaMenu.addEventListener("mouseleave", function() {
            scheduleDesktopHoverClose(dropdown);
        });
    }

    function setupSimpleDropdown(dropdown, toggle, dropdownLink) {
        function closeActiveDropdown() {
            closeActiveDropdownOnDesktop(dropdown);
        }

        dropdownLink?.addEventListener("mouseenter", closeActiveDropdown);
        toggle.addEventListener("mouseenter", closeActiveDropdown);
    }

    function setupDropdown(dropdown) {
        const toggle = dropdown.querySelector(".main-nav__dropdown-toggle, .main-nav__mega-toggle");
        const dropdownLink = dropdown.querySelector(".main-nav__dropdown-link");
        const megaMenu = dropdown.querySelector(".main-nav__mega-menu");

        if (!toggle) {
            return;
        }

        if (megaMenu) {
            setupMegaDropdown(dropdown, toggle, megaMenu);
        } else {
            setupSimpleDropdown(dropdown, toggle, dropdownLink);
        }

        toggle.addEventListener("click", function(event) {
            event.preventDefault();
            toggleDropdown(dropdown, toggle);
        });
    }

    function setupMegaPanels(megaMenu) {
        const triggers = megaMenu.querySelectorAll("[data-mega-panel-trigger]");
        const panels = megaMenu.querySelectorAll("[data-mega-panel]");
        const fixedPanelIndex = megaMenu.querySelector("[data-mega-fixed-panel]")?.getAttribute("data-mega-fixed-panel");

        function setActivePanel(panelIndex) {
            const visiblePanelIndex = fixedPanelIndex || panelIndex;
            const activePanel = megaMenu.querySelector(`[data-mega-panel="${visiblePanelIndex}"]`);

            triggers.forEach(function(trigger) {
                trigger.classList.toggle(
                    "is-active",
                    trigger.getAttribute("data-mega-panel-trigger") === panelIndex
                );
            });

            panels.forEach(function(panel) {
                panel.classList.toggle(
                    "is-active",
                    panel.getAttribute("data-mega-panel") === visiblePanelIndex
                );
            });

            return Boolean(activePanel);
        }

        triggers.forEach(function(trigger) {
            function activate() {
                if (mobileBreakpoint.matches) {
                    return;
                }

                setActivePanel(trigger.getAttribute("data-mega-panel-trigger"));
            }

            trigger.addEventListener("mouseenter", activate);
            trigger.addEventListener("focus", activate);
            trigger.addEventListener("click", function(event) {
                if (mobileBreakpoint.matches) {
                    return;
                }

                const panelIndex = trigger.getAttribute("data-mega-panel-trigger");
                const isAlreadyActive = trigger.classList.contains("is-active");

                if (setActivePanel(panelIndex) && !isAlreadyActive) {
                    event.preventDefault();
                }
            });
        });
    }

    mobileToggle?.addEventListener("click", function() {
        setMobileMenu(!nav.classList.contains("is-mobile-open"));
    });

    dropdowns.forEach(setupDropdown);
    document.querySelectorAll(".main-nav__mega-menu").forEach(setupMegaPanels);

    mobilePanel?.querySelectorAll("a").forEach(function(link) {
        link.addEventListener("click", function() {
            setMobileMenu(false);
        });
    });

    nav?.querySelector(".main-nav__actions .button__cta")?.addEventListener("click", function() {
        setMobileMenu(false);
    });

    document.addEventListener("click", function(event) {
        if (!event.target.closest(".main-nav__dropdown")) {
            dropdowns.forEach(closeDropdown);
        }
    });

    document.addEventListener("keydown", function(event) {
        if (event.key === "Escape") {
            dropdowns.forEach(closeDropdown);
            setMobileMenu(false);
        }
    });

    mobileBreakpoint.addEventListener("change", function(event) {
        nav?.classList.remove("is-mobile-animated");

        if (!event.matches) {
            setMobileMenu(false, false);
        }
    });
});
