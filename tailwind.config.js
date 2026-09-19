/* Tailwind build config for the five Tailwind-styled pages.
 *
 * The site used to load https://cdn.tailwindcss.com (the Play CDN), which compiles in the
 * visitor's browser: ~400 KB of JS on every page view, and every visitor's IP handed to a
 * third-party CDN. That contradicted the site's own privacy stance, so the CSS is now built
 * here and committed as assets/tailwind.css (~16 KB, ~4 KB gzipped). Nothing is fetched at
 * runtime. See assets/fonts/ for the same move applied to the webfonts.
 *
 * REGENERATE AFTER CHANGING ANY TAILWIND CLASS IN THE PAGES BELOW — a new class that isn't
 * in the built file simply has no styles, and the page silently renders wrong:
 *
 *     npx tailwindcss@3.4.17 -c tailwind.config.js -o assets/tailwind.css --minify
 *
 * Pin 3.4.17: that is the exact version the Play CDN was serving, so the output matches what
 * the site rendered before. The default theme is intentional — the CDN ran with no inline
 * tailwind.config, so there was never any customization to carry over.
 *
 * The demo and glass-box pages do NOT use Tailwind (hand-written CSS only) — don't add them.
 */
module.exports = {
  content: [
    "./index.html",
    "./gallery.html",
    "./success.html",
    "./blog/unsteady-ring.html",
    "./pd/index.html",
  ],
  theme: { extend: {} },
  plugins: [],
}
