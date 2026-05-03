/* ═══════════════════════════════════════════════════════════════════
   TEAMATRIX — Futuristic Interactions  v2.0
   Detroit: Become Human UI: cursor, canvas, parallax, reveal, DBH art
═══════════════════════════════════════════════════════════════════ */
(function () {
    'use strict';

    const isTouch  = window.matchMedia('(pointer: coarse)').matches;
    const noMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;


    // ──────────────────────────────────────────────────────────────
    // 0. GEOMETRIC ASSEMBLY ANIMATION
    //    Dark canvas overlay with white/gray dots, triangles & lines
    //    assembling on screen, then fading to reveal the page.
    // ──────────────────────────────────────────────────────────────
    (function runAssembly() {
        if (noMotion) return;

        const canvas = document.getElementById('fx-assemble-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        canvas.width  = innerWidth;
        canvas.height = innerHeight;
        const W = canvas.width;
        const H = canvas.height;

        const rnd  = (a, b) => a + Math.random() * (b - a);
        const rndI = (a, b) => Math.floor(rnd(a, b));
        const lerp = (a, b, t) => a + (b - a) * t;
        const easeOut = t => 1 - (1 - t) * (1 - t);
        const easeIn  = t => t * t;

        // Palette: white / light-gray / mid-gray on dark background
        const COLORS = [
            [255, 255, 255],
            [210, 210, 210],
            [170, 170, 170],
            [130, 130, 130],
        ];

        // ── Build particle list ───────────────────────────────────
        const COUNT = isTouch ? 55 : 100;
        const particles = [];
        for (let i = 0; i < COUNT; i++) {
            const type   = rndI(0, 3);           // 0=dot 1=tri 2=line
            const col    = COLORS[rndI(0, COLORS.length)];
            const size   = type === 0 ? rnd(2, 6)
                         : type === 1 ? rnd(8, 26)
                         :              rnd(30, 140);
            const rot    = rnd(0, Math.PI * 2);
            const vrot   = rnd(-0.03, 0.03);
            const alpha  = rnd(0.4, 0.9);
            // Spread from center outward then converge
            const angle  = rnd(0, Math.PI * 2);
            const dist   = rnd(0.1, 0.55) * Math.min(W, H);
            const cx = W / 2 + Math.cos(angle) * dist;
            const cy = H / 2 + Math.sin(angle) * dist;
            particles.push({
                type, col, size, rot, vrot, alpha,
                x: rnd(0, W),  y: rnd(0, H),   // initial scatter
                tx: cx,         ty: cy,           // converge target
            });
        }

        // ── Draw helpers ──────────────────────────────────────────
        function rgba(col, a) {
            return `rgba(${col[0]},${col[1]},${col[2]},${a.toFixed(3)})`;
        }

        function drawDot(p, t) {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = rgba(p.col, p.alpha * t);
            ctx.fill();
        }

        function drawTri(p, t) {
            ctx.beginPath();
            for (let i = 0; i < 3; i++) {
                const a = (Math.PI * 2 / 3) * i + p.rot;
                const px = p.x + p.size * Math.cos(a);
                const py = p.y + p.size * Math.sin(a);
                if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
            }
            ctx.closePath();
            ctx.strokeStyle = rgba(p.col, p.alpha * t);
            ctx.lineWidth   = 1.2;
            ctx.stroke();
            ctx.fillStyle   = rgba(p.col, p.alpha * 0.12 * t);
            ctx.fill();
        }

        function drawLine(p, t) {
            const half = p.size / 2;
            const cx   = Math.cos(p.rot), cy = Math.sin(p.rot);
            ctx.beginPath();
            ctx.moveTo(p.x - cx * half, p.y - cy * half);
            ctx.lineTo(p.x + cx * half, p.y + cy * half);
            ctx.strokeStyle = rgba(p.col, p.alpha * t);
            ctx.lineWidth   = 1;
            ctx.stroke();
            // perpendicular tick
            const tx = -cy * 5, ty = cx * 5;
            ctx.beginPath();
            ctx.moveTo(p.x - tx, p.y - ty);
            ctx.lineTo(p.x + tx, p.y + ty);
            ctx.strokeStyle = rgba(p.col, p.alpha * 0.4 * t);
            ctx.lineWidth   = 0.7;
            ctx.stroke();
        }

        // ── Phases ────────────────────────────────────────────────
        // 0 – 350 ms : dark bg fades in, particles scatter (appear)
        // 350 – 1200 ms: particles converge toward center area
        // 1200 – 1800 ms: particles disperse outward, bg fades out
        const T0 = 350, T1 = 1200, T2 = 1800;

        let start = null;

        function frame(ts) {
            if (!start) start = ts;
            const elapsed = ts - start;

            let bgAlpha, particleT, converge, disperse;

            if (elapsed < T0) {
                // Fade-in dark overlay + particles appear
                const p = elapsed / T0;
                bgAlpha    = easeOut(p);
                particleT  = p;
                converge   = 0;
                disperse   = 0;
            } else if (elapsed < T1) {
                // Converge toward center
                const p = (elapsed - T0) / (T1 - T0);
                bgAlpha   = 1;
                particleT = 1;
                converge  = easeOut(p);
                disperse  = 0;
            } else if (elapsed < T2) {
                // Disperse and fade out overlay
                const p = (elapsed - T1) / (T2 - T1);
                bgAlpha   = 1 - easeIn(p);
                particleT = 1 - p * 0.6;
                converge  = 1;
                disperse  = easeOut(p);
            } else {
                // Done — remove canvas
                canvas.classList.add('fx-assembled');
                triggerBlockMaterialise();
                return;
            }

            // ── Draw dark background ──
            ctx.clearRect(0, 0, W, H);
            ctx.fillStyle = `rgba(8,11,18,${bgAlpha.toFixed(3)})`;
            ctx.fillRect(0, 0, W, H);

            // ── Draw particles ────────
            for (const p of particles) {
                if (converge > 0 && disperse === 0) {
                    p.x = lerp(p.x, p.tx, converge * 0.06);
                    p.y = lerp(p.y, p.ty, converge * 0.06);
                }
                if (disperse > 0) {
                    // Fly outward
                    p.x += (p.x - W / 2) * 0.015;
                    p.y += (p.y - H / 2) * 0.015;
                }
                p.rot += p.vrot * (1 - converge * 0.5);

                if      (p.type === 0) drawDot(p,  particleT);
                else if (p.type === 1) drawTri(p,  particleT);
                else                   drawLine(p, particleT);
            }

            requestAnimationFrame(frame);
        }

        requestAnimationFrame(frame);
    })();


    // ── Per-block flash: brightness desaturate → normal ───────────
    // Does NOT hide content, does NOT use transform/opacity tricks.
    function triggerBlockMaterialise() {
        if (noMotion) return;
        const targets = document.querySelectorAll(
            '.card, section, .navbar, footer, .alert'
        );
        targets.forEach((el, i) => {
            const delay = Math.min(i * 30, 350);
            setTimeout(() => {
                el.classList.add('fx-block-materialise');
                el.addEventListener('animationend', () => {
                    el.classList.remove('fx-block-materialise');
                }, { once: true });
            }, delay);
        });
    }


    // ──────────────────────────────────────────────────────────────
    // 1. PAGE-LOAD PROGRESS BAR
    // ──────────────────────────────────────────────────────────────
    const loader = document.getElementById('fx-loader');
    if (loader) {
        let p = 0;
        const grow = setInterval(() => {
            p += (100 - p) * 0.09;
            loader.style.width = Math.min(p, 90) + '%';
        }, 40);
        window.addEventListener('load', () => {
            clearInterval(grow);
            loader.style.width = '100%';
            setTimeout(() => loader.classList.add('done'), 300);
        });
    }


    // ──────────────────────────────────────────────────────────────
    // 2. CUSTOM CURSOR  (hex dot + lagging direction triangle)
    // ──────────────────────────────────────────────────────────────
    const hexEl = document.getElementById('fx-cursor-hex');
    const triEl = document.getElementById('fx-cursor-tri');

    if (hexEl && triEl && !isTouch) {
        let mX = -300, mY = -300;
        let tX = -300, tY = -300;
        let pX = -300, pY = -300;
        let angle = 0;

        document.addEventListener('mousemove', e => { mX = e.clientX; mY = e.clientY; });
        document.addEventListener('mousedown', () => document.body.classList.add('cx-click'));
        document.addEventListener('mouseup',   () => document.body.classList.remove('cx-click'));

        function targetType(el) {
            if (!el) return '';
            if (el.closest('input[type="text"],input[type="email"],input[type="password"],input[type="search"],textarea,[contenteditable]'))
                return 'text';
            if (el.closest('a,button,label,[role="button"],.btn,.nav-link,.dropdown-item,.card,select'))
                return 'link';
            return '';
        }
        document.addEventListener('mouseover', e => {
            const t = targetType(e.target);
            document.body.classList.toggle('cx-link', t === 'link');
            document.body.classList.toggle('cx-text', t === 'text');
        });

        const lerp = (a, b, t) => a + (b - a) * t;

        (function tick() {
            hexEl.style.left = mX + 'px';
            hexEl.style.top  = mY + 'px';

            tX = lerp(tX, mX, 0.10);
            tY = lerp(tY, mY, 0.10);

            const dx = tX - pX, dy = tY - pY;
            if (Math.abs(dx) + Math.abs(dy) > 0.3)
                angle = Math.atan2(dy, dx) * 180 / Math.PI + 90;

            pX = lerp(pX, mX, 0.10);
            pY = lerp(pY, mY, 0.10);

            triEl.style.left      = tX + 'px';
            triEl.style.top       = tY + 'px';
            triEl.style.transform = `translate(-50%,-65%) rotate(${angle}deg)`;

            requestAnimationFrame(tick);
        })();
    }


    // ──────────────────────────────────────────────────────────────
    // 3. GEOMETRIC BACKGROUND CANVAS
    //    Floating hexagons & triangles, react to mouse
    // ──────────────────────────────────────────────────────────────
    const canvas = document.getElementById('fx-bg-canvas');
    if (canvas && !isTouch && !noMotion) {
        const ctx = canvas.getContext('2d');
        let W = 0, H = 0, mNX = 0, mNY = 0;

        const resize = () => { W = canvas.width = innerWidth; H = canvas.height = innerHeight; };
        window.addEventListener('resize', resize, { passive: true });
        resize();

        document.addEventListener('mousemove', e => {
            mNX = (e.clientX / W - 0.5) * 2;
            mNY = (e.clientY / H - 0.5) * 2;
        });

        const rnd = (a, b) => a + Math.random() * (b - a);

        function hexPath(x, y, r, rot) {
            ctx.beginPath();
            for (let i = 0; i < 6; i++) {
                const a = Math.PI / 3 * i + (rot || 0);
                i ? ctx.lineTo(x + r * Math.cos(a), y + r * Math.sin(a))
                  : ctx.moveTo(x + r * Math.cos(a), y + r * Math.sin(a));
            }
            ctx.closePath();
        }
        function triPath(x, y, r, rot) {
            ctx.beginPath();
            for (let i = 0; i < 3; i++) {
                const a = Math.PI * 2 / 3 * i + rot;
                i ? ctx.lineTo(x + r * Math.cos(a), y + r * Math.sin(a))
                  : ctx.moveTo(x + r * Math.cos(a), y + r * Math.sin(a));
            }
            ctx.closePath();
        }

        const pts = [];
        for (let i = 0; i < 16; i++)
            pts.push({ type:'hex', x:rnd(0,W), y:rnd(0,H), r:rnd(14,52), vx:rnd(-0.10,0.10), vy:rnd(-0.22,-0.04), rot:rnd(0,6.28), vrot:rnd(-0.003,0.003), alpha:rnd(0.025,0.075), hue:rnd(196,216) });
        for (let i = 0; i < 12; i++)
            pts.push({ type:'tri', x:rnd(0,W), y:rnd(0,H), r:rnd(8,30),  vx:rnd(-0.08,0.08), vy:rnd(-0.18,-0.04), rot:rnd(0,6.28), vrot:rnd(-0.005,0.005), alpha:rnd(0.03,0.10),  hue:rnd(200,222) });

        (function draw() {
            ctx.clearRect(0, 0, W, H);
            for (const p of pts) {
                ctx.save();
                ctx.globalAlpha = p.alpha;
                ctx.fillStyle   = `hsl(${p.hue},72%,58%)`;
                p.type === 'hex' ? hexPath(p.x,p.y,p.r,p.rot) : triPath(p.x,p.y,p.r,p.rot);
                ctx.fill();
                ctx.restore();

                p.x += p.vx + mNX * 0.055;
                p.y += p.vy + mNY * 0.035;
                p.rot += p.vrot;

                if (p.y + p.r < 0) { p.y = H + p.r; p.x = rnd(0, W); }
                if (p.y - p.r > H)   p.y = -p.r;
                if (p.x + p.r < 0)   p.x = W + p.r;
                if (p.x - p.r > W)   p.x = -p.r;
            }
            requestAnimationFrame(draw);
        })();
    }


    // ──────────────────────────────────────────────────────────────
    // 4. SCROLL PARALLAX  (data-parallax="speed")
    // ──────────────────────────────────────────────────────────────
    const pxEls = document.querySelectorAll('[data-parallax]');
    if (pxEls.length && !noMotion) {
        window.addEventListener('scroll', () => {
            const sy = scrollY;
            pxEls.forEach(el => {
                const s = parseFloat(el.dataset.parallax) || 0.3;
                el.style.transform = `translateY(${sy * s}px)`;
            });
        }, { passive: true });
    }


    // ──────────────────────────────────────────────────────────────
    // 5. SCROLL REVEAL  (CSS animation, no transition conflict)
    // ──────────────────────────────────────────────────────────────
    if ('IntersectionObserver' in window && !noMotion) {
        const targets = document.querySelectorAll('.card, .fx-reveal');
        targets.forEach((el, i) => {
            el.style.setProperty('--sr-delay', Math.min(i * 0.045, 0.35) + 's');
            el.classList.add('fx-sr');
        });
        const io = new IntersectionObserver(entries => {
            entries.forEach(e => {
                if (!e.isIntersecting) return;
                const el = e.target;
                el.classList.add('fx-sr-in');
                el.addEventListener('animationend', () => {
                    el.classList.remove('fx-sr', 'fx-sr-in');
                    el.style.removeProperty('--sr-delay');
                }, { once: true });
                io.unobserve(el);
            });
        }, { threshold: 0.07, rootMargin: '0px 0px -20px 0px' });
        targets.forEach(el => io.observe(el));
    }


    // ──────────────────────────────────────────────────────────────
    // 6. MOUSE-TILT ON CARDS  (3D perspective)
    //    Reduced to 4° because clip-path flattens 3D anyway
    // ──────────────────────────────────────────────────────────────
    if (!isTouch) {
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mousemove', e => {
                const r = card.getBoundingClientRect();
                if (r.width < 100) return;
                const cx = (e.clientX - r.left) / r.width  - 0.5;
                const cy = (e.clientY - r.top)  / r.height - 0.5;
                card.classList.add('fx-tilting');
                // Subtle tilt — clip-path limits visual 3D depth
                card.style.transform =
                    `perspective(800px) rotateY(${cx * 4}deg) rotateX(${-cy * 4}deg) translateY(-3px)`;
            });
            card.addEventListener('mouseleave', () => {
                card.classList.remove('fx-tilting');
                card.style.transform = '';
            });
        });
    }


    // ──────────────────────────────────────────────────────────────
    // 7. ROBOT MOUSE PARALLAX  (translate composes with animation)
    // ──────────────────────────────────────────────────────────────
    if (!isTouch) {
        const robotWrapper = document.getElementById('robot-float-wrapper');
        if (robotWrapper) {
            document.addEventListener('mousemove', e => {
                const nx = (e.clientX / innerWidth  - 0.5);
                const ny = (e.clientY / innerHeight - 0.5);
                robotWrapper.style.translate = `${nx * 14}px ${ny * 10}px`;
            });
        }
    }


    // ──────────────────────────────────────────────────────────────
    // 8. NAVBAR ACTIVE LINK
    // ──────────────────────────────────────────────────────────────
    const path = location.pathname;
    document.querySelectorAll('.navbar .nav-link[href]').forEach(a => {
        const href = a.getAttribute('href');
        if (href && href !== '/' && path.startsWith(href))
            a.classList.add('active');
    });


    // ──────────────────────────────────────────────────────────────
    // 9. DBH GEOMETRIC ART INJECTION
    //    Adds reticles, hex watermarks, circuit traces, data panels,
    //    triangle clusters and ID tags to page sections.
    // ──────────────────────────────────────────────────────────────

    /** Create an element with className + optional attrs */
    function el(tag, cls, attrs) {
        const e = document.createElement(tag);
        if (cls) e.className = cls;
        if (attrs) Object.entries(attrs).forEach(([k,v]) => e.setAttribute(k,v));
        return e;
    }

    /** Inject a .fx-geo-art container into a section */
    function injectGeoArt(section, isDark) {
        if (section.querySelector('.fx-geo-art')) return;

        const art = el('div', 'fx-geo-art', { 'aria-hidden': 'true' });

        // ── Large hollow hex watermark ──────────────────────
        const hexWm = el('div', 'fx-hex-wm');
        // Position: right side, vertically centered
        hexWm.style.cssText = 'right:-60px; top:50%; transform:translateY(-50%);';
        art.appendChild(hexWm);

        // ── Smaller inner hex (counter-rotating) ──────────
        const hexInner = el('div', 'fx-hex-wm-inner');
        hexInner.style.cssText = 'right:-10px; top:50%; transform:translateY(-50%);';
        art.appendChild(hexInner);

        // ── Circuit horizontal line ────────────────────────
        const cLine = el('div', 'fx-circuit-line');
        cLine.style.cssText = `left:0; right:0; bottom:${20 + Math.floor(Math.random()*40)}px;`;
        art.appendChild(cLine);

        // ── Circuit vertical line ──────────────────────────
        const cLineV = el('div', 'fx-circuit-line-v');
        cLineV.style.cssText = `top:0; bottom:0; right:${120 + Math.floor(Math.random()*80)}px;`;
        art.appendChild(cLineV);

        // ── Circuit node at intersection ──────────────────
        const cNode = el('div', 'fx-circuit-node');
        cNode.style.cssText = `right:${123 + Math.floor(Math.random()*77)}px; bottom:${22 + Math.floor(Math.random()*38)}px;`;
        art.appendChild(cNode);

        // ── Triangle scatter (top-left decoration) ────────
        const tri = el('div', 'fx-tri-scatter');
        tri.style.cssText = 'top:12px; left:12px;';
        const sizes = [8, 12, 6, 10, 7];
        const offsets = [0, 4, 10, 7, 14];
        sizes.forEach((s, i) => {
            const span = document.createElement('span');
            span.style.cssText = `width:${s}px; height:${s*0.87}px; margin-right:${4-i%3}px; margin-bottom:${offsets[i]}px;`;
            tri.appendChild(span);
        });
        art.appendChild(tri);

        // ── Data panel (bottom-right readout) ─────────────
        const panel = el('div', 'fx-data-panel');
        panel.setAttribute('data-id', 'UNIT_' + (Math.random()*900+100|0));
        const lines = isDark
            ? ['STATUS ··· OPERATIONAL', 'VER ···· 0.' + (Math.random()*9|0) + '.' + (Math.random()*9|0), 'CPU ···· ' + (60+Math.random()*30|0) + '%']
            : ['SYS ···· TEAMATRIX', 'NET ···· ONLINE', 'SEC ···· LEVEL_3'];
        panel.innerHTML = lines.join('<br>');
        panel.style.cssText = 'position:absolute; bottom:10px; right:12px;';
        art.appendChild(panel);

        // ── Diagonal art lines ─────────────────────────────
        const diag = el('div', 'fx-diag-art');
        art.appendChild(diag);

        section.appendChild(art);

        // ── Add reticle corners ────────────────────────────
        section.classList.add('fx-reticle');

        // ── Add section ID tag ─────────────────────────────
        const sysNum = String(section.dataset.artId || (Math.random()*90+10|0)).padStart(2,'0');
        const tag = el('div', 'fx-id-tag');
        tag.textContent = `TMX_${sysNum}`;
        tag.setAttribute('aria-hidden', 'true');
        section.appendChild(tag);
    }

    /** Inject circuit traces into the robot section */
    function injectRobotCircuits() {
        const robotSec = document.getElementById('robot-section');
        if (!robotSec) return;
        if (robotSec.querySelector('.fx-geo-art')) return;

        const art = el('div', 'fx-geo-art', { 'aria-hidden': 'true' });

        // Multiple circuit lines radiating from robot
        const linesH = [
            { top: '20%', left: '0', right: '0' },
            { top: '45%', left: '0', right: '0' },
            { top: '70%', left: '0', right: '0' },
        ];
        linesH.forEach((style, i) => {
            const line = el('div', 'fx-circuit-line');
            Object.assign(line.style, style);
            line.style.animationDelay = (i * 0.8) + 's';
            art.appendChild(line);
        });

        // Nodes at intersections
        const nodes = [
            { top: 'calc(20% - 2px)', left: '10%' },
            { top: 'calc(45% - 2px)', left: '25%' },
            { top: 'calc(70% - 2px)', left: '15%' },
            { top: 'calc(20% - 2px)', right: '12%' },
            { top: 'calc(45% - 2px)', right: '22%' },
        ];
        nodes.forEach((style, i) => {
            const node = el('div', 'fx-circuit-node');
            Object.assign(node.style, style);
            node.style.animationDelay = (i * 0.5) + 's';
            art.appendChild(node);
        });

        // Big hex watermark behind robot
        const hexWm = el('div', 'fx-hex-wm');
        hexWm.style.cssText = 'width:500px; height:500px; top:50%; left:50%; transform:translate(-50%,-50%); opacity:0.03;';
        art.appendChild(hexWm);

        robotSec.style.position = 'relative';
        robotSec.insertBefore(art, robotSec.firstChild);
    }

    /** Inject a local scan band + accent bar on dark hero-like divs */
    function injectHeroArt(heroDiv) {
        if (heroDiv.querySelector('.fx-geo-art')) return;

        const art = el('div', 'fx-geo-art', { 'aria-hidden': 'true' });
        heroDiv.style.position = 'relative';
        heroDiv.style.overflow = 'hidden';

        // Hex cluster behind title
        const hexWm = el('div', 'fx-hex-wm');
        hexWm.style.cssText = 'width:240px; height:240px; top:50%; left:50%; transform:translate(-50%,-50%); opacity:0.035;';
        art.appendChild(hexWm);

        // Triangle decoration
        const triL = el('div', 'fx-tri-scatter');
        triL.style.cssText = 'bottom:12px; left:16px; align-items:flex-end;';
        [14, 10, 8, 12, 6].forEach(s => {
            const span = document.createElement('span');
            span.style.cssText = `width:${s}px; height:${s*0.87}px; margin-right:3px;`;
            triL.appendChild(span);
        });
        art.appendChild(triL);

        // Diagonal art
        art.appendChild(el('div', 'fx-diag-art'));

        heroDiv.insertBefore(art, heroDiv.firstChild);

        // Local scan effect
        heroDiv.classList.add('fx-scan-local');
    }

    // ── Run art injection after DOM ready ─────────────────────────
    function runArtInjection() {
        // Dark sections (bg-dark, bg-primary)
        document.querySelectorAll('section.bg-dark, section.bg-primary').forEach((s, i) => {
            s.dataset.artId = String(i + 1).padStart(2, '0');
            injectGeoArt(s, true);
        });

        // Light/border sections
        document.querySelectorAll('section.border, section:not(.bg-dark):not(.bg-primary)').forEach((s, i) => {
            if (s.classList.contains('bg-light') || s.querySelector('h2')) {
                s.dataset.artId = String(i + 10).padStart(2, '0');
                injectGeoArt(s, false);
            }
        });

        // Robot section
        injectRobotCircuits();

        // Hero div (main page title area)
        document.querySelectorAll('[data-hero]').forEach(injectHeroArt);

        // Hero in development page (bg-dark div at top)
        document.querySelectorAll('.px-4.py-5.bg-dark').forEach(injectHeroArt);
    }

    // Run after slight delay to let Bootstrap render
    setTimeout(runArtInjection, 50);


    // ──────────────────────────────────────────────────────────────
    // 10. HEX GRID BG ON DARK SECTIONS
    // ──────────────────────────────────────────────────────────────
    document.querySelectorAll('section.bg-dark, section.bg-primary, #robot-section').forEach(s => {
        s.classList.add('fx-hex-grid-bg');
    });


    // ──────────────────────────────────────────────────────────────
    // 11. STATUS STRIP ANIMATION
    //     Animates .fx-status-pip elements on hover
    // ──────────────────────────────────────────────────────────────
    document.querySelectorAll('.fx-status-strip').forEach(strip => {
        const pips = strip.querySelectorAll('.fx-status-pip');
        strip.addEventListener('mouseenter', () => {
            pips.forEach((pip, i) => {
                setTimeout(() => pip.classList.add('active'), i * 80);
            });
        });
        strip.addEventListener('mouseleave', () => {
            pips.forEach(pip => pip.classList.remove('active'));
        });
    });


    // ──────────────────────────────────────────────────────────────
    // 12. TYPING CURSOR ON data-typewriter elements
    // ──────────────────────────────────────────────────────────────
    document.querySelectorAll('[data-typewriter]').forEach(el => {
        const text  = el.textContent;
        const speed = parseInt(el.dataset.typewriter) || 45;
        el.textContent = '';
        el.style.borderRight = '2px solid var(--fx-blue)';
        let i = 0;
        const t = setInterval(() => {
            el.textContent += text[i++];
            if (i >= text.length) {
                clearInterval(t);
                setTimeout(() => { el.style.borderRight = 'none'; }, 600);
            }
        }, speed);
    });

})();
