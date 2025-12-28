# Quickstart: Docusaurus UI Theme - Teal & Navy

**Feature**: 004-docusaurus-ui-theme
**Date**: 2025-12-28
**Estimated Implementation Time**: 2-3 hours

## Overview

This guide provides step-by-step instructions to implement the Teal & Navy theme for the Physical AI textbook Docusaurus site.

---

## Prerequisites

- [ ] Docusaurus site running locally (`npm run start`)
- [ ] Access to `physical-ai-textbook/docs/src/css/custom.css`
- [ ] Access to `physical-ai-textbook/docs/docusaurus.config.ts`

---

## Quick Implementation Steps

### Step 1: Update CSS Variables (custom.css)

Replace the contents of `src/css/custom.css` with the theme CSS:

```css
/**
 * Physical AI Textbook Theme - Teal & Navy
 * Infima CSS variable overrides for Docusaurus
 */

/* ============================
   LIGHT MODE (Default)
   ============================ */

:root {
  /* Primary Color Scale - Teal */
  --ifm-color-primary: #0d9488;
  --ifm-color-primary-dark: #0b7c72;
  --ifm-color-primary-darker: #0a756b;
  --ifm-color-primary-darkest: #086058;
  --ifm-color-primary-light: #0faa9e;
  --ifm-color-primary-lighter: #14b8a6;
  --ifm-color-primary-lightest: #2dd4bf;

  /* Custom Navy Palette */
  --theme-navy-base: #1a365d;
  --theme-navy-dark: #0f172a;
  --theme-navy-light: #2d4a6f;

  /* Typography */
  --ifm-font-color-base: #334155;
  --ifm-heading-color: #0f172a;
  --ifm-line-height-base: 1.65;
  --ifm-code-font-size: 95%;

  /* Code Highlighting */
  --docusaurus-highlighted-code-line-bg: rgba(13, 148, 136, 0.1);
}

/* ============================
   DARK MODE
   ============================ */

[data-theme='dark'] {
  /* Primary Color Scale - Brighter Teal for Contrast */
  --ifm-color-primary: #14b8a6;
  --ifm-color-primary-dark: #0d9488;
  --ifm-color-primary-darker: #0b7c72;
  --ifm-color-primary-darkest: #086058;
  --ifm-color-primary-light: #2dd4bf;
  --ifm-color-primary-lighter: #5eead4;
  --ifm-color-primary-lightest: #99f6e4;

  /* Navy Background */
  --ifm-background-color: #0f172a;
  --ifm-background-surface-color: #1e293b;

  /* Typography */
  --ifm-font-color-base: #e2e8f0;
  --ifm-heading-color: #f8fafc;

  /* Code Highlighting */
  --docusaurus-highlighted-code-line-bg: rgba(20, 184, 166, 0.2);
}

/* ============================
   NAVBAR - Navy Background
   ============================ */

.navbar {
  background-color: var(--theme-navy-base);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.navbar__title {
  color: #ffffff;
}

.navbar__link {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.navbar__link:hover,
.navbar__link--active {
  color: #14b8a6;
}

.navbar__link--active {
  border-bottom: 2px solid #0d9488;
}

/* Dark mode navbar */
[data-theme='dark'] .navbar {
  background-color: var(--theme-navy-dark);
}

/* Mobile navbar toggle */
.navbar__toggle {
  color: #ffffff;
}

/* ============================
   SIDEBAR - Navy Background
   ============================ */

.menu {
  background-color: var(--theme-navy-base);
  padding: 1rem 0;
}

.menu__link {
  color: rgba(255, 255, 255, 0.85);
  border-radius: 0;
  padding: 0.5rem 1rem;
}

.menu__link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.menu__link--active {
  background-color: rgba(13, 148, 136, 0.2);
  border-left: 3px solid #0d9488;
  color: #ffffff;
  font-weight: 600;
}

.menu__list-item-collapsible:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

/* Category labels */
.menu__list-item--collapsed .menu__link,
.menu__list-item--collapsed .menu__caret {
  color: rgba(255, 255, 255, 0.7);
}

/* Dark mode sidebar */
[data-theme='dark'] .menu {
  background-color: var(--theme-navy-dark);
}

/* ============================
   FOOTER - Navy Background
   ============================ */

.footer {
  background-color: var(--theme-navy-base);
}

.footer__title {
  color: #ffffff;
}

.footer__link-item {
  color: rgba(255, 255, 255, 0.85);
}

.footer__link-item:hover {
  color: #14b8a6;
}

.footer__copyright {
  color: rgba(255, 255, 255, 0.6);
}

[data-theme='dark'] .footer {
  background-color: var(--theme-navy-dark);
}

/* ============================
   LINKS
   ============================ */

a {
  transition: color 150ms ease-in-out;
}

a:hover {
  text-decoration: underline;
}

/* ============================
   BUTTONS
   ============================ */

.button--primary {
  background-color: #0d9488;
  border-color: #0d9488;
  color: #ffffff;
}

.button--primary:hover {
  background-color: #0b7c72;
  border-color: #0b7c72;
}

.button--secondary {
  background-color: transparent;
  border-color: #0d9488;
  color: #0d9488;
}

.button--secondary:hover {
  background-color: rgba(13, 148, 136, 0.1);
}

/* ============================
   ADMONITIONS (Callouts)
   ============================ */

/* Info and Tip - Teal themed */
.alert--info {
  --ifm-alert-background-color: rgba(13, 148, 136, 0.1);
  --ifm-alert-border-color: #0d9488;
  --ifm-alert-color: var(--ifm-font-color-base);
}

.alert--success,
.admonition-tip {
  --ifm-alert-background-color: rgba(13, 148, 136, 0.1);
  --ifm-alert-border-color: #0d9488;
}

/* Keep warning and danger standard */
.alert--warning {
  --ifm-alert-background-color: rgba(217, 119, 6, 0.1);
  --ifm-alert-border-color: #d97706;
}

.alert--danger {
  --ifm-alert-background-color: rgba(220, 38, 38, 0.1);
  --ifm-alert-border-color: #dc2626;
}

/* ============================
   CODE BLOCKS
   ============================ */

pre {
  background-color: #f1f5f9;
  border: 1px solid #e2e8f0;
}

[data-theme='dark'] pre {
  background-color: #1e293b;
  border-color: #334155;
}

code {
  background-color: rgba(13, 148, 136, 0.1);
  border-radius: 0.25rem;
  padding: 0.125rem 0.375rem;
}

[data-theme='dark'] code {
  background-color: rgba(20, 184, 166, 0.15);
}

/* ============================
   TABLE OF CONTENTS
   ============================ */

.table-of-contents__link:hover,
.table-of-contents__link--active {
  color: #0d9488;
}

/* ============================
   FOCUS STATES (Accessibility)
   ============================ */

*:focus-visible {
  outline: 2px solid #0d9488;
  outline-offset: 2px;
}

/* ============================
   PAGINATION
   ============================ */

.pagination-nav__link {
  border-color: #e2e8f0;
}

.pagination-nav__link:hover {
  border-color: #0d9488;
}

.pagination-nav__sublabel {
  color: #64748b;
}

/* ============================
   SEARCH (if using Algolia)
   ============================ */

.DocSearch-Button {
  background-color: rgba(255, 255, 255, 0.1);
}

.DocSearch-Button:hover {
  background-color: rgba(255, 255, 255, 0.2);
}
```

### Step 2: Verify Configuration (docusaurus.config.ts)

Ensure footer style is set to 'dark' (already configured):

```typescript
footer: {
  style: 'dark',
  // ... rest of footer config
}
```

### Step 3: Test the Theme

1. **Restart dev server**: `npm run start`
2. **Check light mode**:
   - [ ] Navy navbar with white text
   - [ ] Teal links throughout content
   - [ ] White content background
   - [ ] Navy sidebar with teal active indicators
3. **Check dark mode** (toggle in navbar):
   - [ ] Dark navy background
   - [ ] Bright teal links visible
   - [ ] Text is readable
4. **Check responsive**:
   - [ ] Mobile hamburger menu works
   - [ ] Colors consistent across viewports

### Step 4: Build and Verify

```bash
npm run build
npm run serve
```

Verify production build renders correctly.

---

## Validation Checklist

### Visual Verification

- [ ] Navbar: Navy background, white text, teal hover
- [ ] Sidebar: Navy background, teal active indicator
- [ ] Links: Teal color, lighter on hover
- [ ] Buttons: Teal primary, proper hover states
- [ ] Footer: Navy background matching navbar
- [ ] Admonitions: Teal for info/tip, standard for warning/danger
- [ ] Code blocks: Light gray background (light mode), dark gray (dark mode)

### Accessibility Verification

- [ ] Run Lighthouse accessibility audit (score > 90)
- [ ] Verify focus states visible with keyboard navigation
- [ ] Check color contrast with browser dev tools

### Cross-Browser Testing

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

### Responsive Testing

- [ ] Desktop (1920px)
- [ ] Tablet (768px)
- [ ] Mobile (375px)

---

## Troubleshooting

### Colors not applying

1. Clear browser cache
2. Restart dev server
3. Check for CSS syntax errors in console

### Sidebar not styled

Ensure `.menu` class is targeted correctly. Docusaurus wraps sidebar in this class.

### Dark mode toggle not working

Verify `colorMode` config in `docusaurus.config.ts`:
```typescript
colorMode: {
  respectPrefersColorScheme: true,
}
```

### Focus states not visible

Check if any global CSS is overriding `outline` styles.

---

## File Locations

| File | Purpose |
|------|---------|
| `src/css/custom.css` | All theme overrides |
| `docusaurus.config.ts` | Footer style, color mode config |

---

## Next Steps After Implementation

1. Run full accessibility audit
2. Test with actual textbook content
3. Get user feedback on readability
4. Document any additional component styling needs
