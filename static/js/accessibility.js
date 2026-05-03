document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const panel = document.getElementById('accessibility-panel');
    const toggleBtn = document.getElementById('acc-toggle-btn');
    const closeBtn = document.getElementById('acc-close');
    const resetBtn = document.getElementById('acc-reset');
    const imagesBtn = document.getElementById('acc-images-toggle');

    function load() {
        return JSON.parse(localStorage.getItem('acc_settings') || '{}');
    }

    function save(s) {
        localStorage.setItem('acc_settings', JSON.stringify(s));
    }

    function apply(s) {
        // Font size — apply to <html> so rem-based Bootstrap components scale too
        const html = document.documentElement;
        body.classList.remove('acc-font-normal', 'acc-font-large', 'acc-font-xlarge');
        html.classList.remove('acc-font-normal', 'acc-font-large', 'acc-font-xlarge');
        if (s.font && s.font !== 'normal') {
            body.classList.add('acc-font-' + s.font);
            html.classList.add('acc-font-' + s.font);
        }

        // Theme
        body.classList.remove('acc-theme-bw', 'acc-theme-wb', 'acc-theme-blue');
        if (s.theme && s.theme !== 'normal') {
            body.classList.add('acc-theme-' + s.theme);
        }

        // Images
        if (s.imagesOff) {
            body.classList.add('acc-no-images');
            imagesBtn.classList.add('active');
        } else {
            body.classList.remove('acc-no-images');
            imagesBtn.classList.remove('active');
        }

        // Panel visibility
        if (s.panelOpen) {
            panel.classList.add('open');
            body.classList.add('acc-active');
        } else {
            panel.classList.remove('open');
            body.classList.remove('acc-active');
        }

        // Active buttons
        panel.querySelectorAll('[data-font]').forEach(function (btn) {
            btn.classList.toggle('active', btn.dataset.font === (s.font || 'normal'));
        });
        panel.querySelectorAll('[data-theme]').forEach(function (btn) {
            btn.classList.toggle('active', btn.dataset.theme === (s.theme || 'normal'));
        });
    }

    // Toggle panel
    toggleBtn.addEventListener('click', function () {
        var s = load();
        s.panelOpen = !s.panelOpen;
        save(s);
        apply(s);
    });

    closeBtn.addEventListener('click', function () {
        var s = load();
        s.panelOpen = false;
        save(s);
        apply(s);
    });

    // Font buttons
    panel.querySelectorAll('[data-font]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var s = load();
            s.font = btn.dataset.font;
            save(s);
            apply(s);
        });
    });

    // Theme buttons
    panel.querySelectorAll('[data-theme]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var s = load();
            s.theme = btn.dataset.theme;
            save(s);
            apply(s);
        });
    });

    // Images toggle
    imagesBtn.addEventListener('click', function () {
        var s = load();
        s.imagesOff = !s.imagesOff;
        save(s);
        apply(s);
    });

    // Reset
    resetBtn.addEventListener('click', function () {
        var s = { panelOpen: true };
        save(s);
        apply(s);
    });

    // Apply saved settings on load
    apply(load());
});
