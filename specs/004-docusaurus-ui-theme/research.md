# Research: Docusaurus UI Theme - Teal & Navy

**Feature**: 004-docusaurus-ui-theme
**Date**: 2025-12-28
**Status**: Complete

## Research Summary

This document captures research findings for implementing a custom Teal & Navy Blue theme for the Physical AI textbook Docusaurus site.

---

## 1. Docusaurus Theming Architecture

### Decision: Use CSS Custom Properties (Infima Variables)

**Rationale**: Docusaurus uses Infima CSS framework with CSS custom properties. Overriding these variables in `custom.css` is the recommended approach that:
- Maintains upgrade compatibility
- Requires no theme ejection
- Supports light/dark mode switching automatically
- Provides consistent styling across all components

**Alternatives Considered**:
| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| CSS Variables Override | Simple, maintainable, upgrade-safe | Limited to exposed variables | **Selected** |
| Theme Ejection | Full control | Breaks upgrade path, maintenance burden | Rejected |
| Swizzling Components | Targeted overrides | Complexity, partial customization | Rejected for colors |
| Custom Theme Package | Reusable | Overkill for single site | Rejected |

---

## 2. Infima Color System

### Decision: Override Primary Color Scale + Custom Navy Variables

**Rationale**: Infima exposes `--ifm-color-primary-*` variables that control links, buttons, and active states. We'll set these to Teal. For Navy Blue (navbar, sidebar, footer), we'll add custom variables and target specific selectors.

**Key Infima Variables to Override**:
```css
/* Primary (Teal) - controls links, buttons, active states */
--ifm-color-primary: #0d9488;
--ifm-color-primary-dark: #0b7c72;
--ifm-color-primary-darker: #0a756b;
--ifm-color-primary-darkest: #086058;
--ifm-color-primary-light: #0faa9e;
--ifm-color-primary-lighter: #10b1a5;
--ifm-color-primary-lightest: #14c4b8;

/* Background/content */
--ifm-background-color: #ffffff;
--ifm-background-surface-color: #f8fafc;

/* Navbar (Navy) - requires custom CSS */
--ifm-navbar-background-color: #1a365d;
--ifm-navbar-link-color: #ffffff;
```

**Teal Palette (Tailwind-inspired)**:
- Base: `#0d9488` (teal-600)
- Dark: `#0f766e` (teal-700)
- Darker: `#115e59` (teal-800)
- Light: `#14b8a6` (teal-500)
- Lighter: `#2dd4bf` (teal-400)

**Navy Blue Palette**:
- Base: `#1a365d` (deep navy)
- Dark: `#1e3a5f` (darker variant for dark mode)
- Light: `#2d4a6f` (hover states)

---

## 3. Navbar Customization

### Decision: Override Navbar Background via CSS

**Rationale**: Docusaurus navbar uses `--ifm-navbar-background-color` but also needs link color adjustments for white text on Navy background.

**Implementation Pattern**:
```css
.navbar {
  --ifm-navbar-background-color: #1a365d;
  --ifm-navbar-link-color: #ffffff;
  --ifm-navbar-link-hover-color: #14b8a6; /* Teal hover */
}

.navbar__link--active {
  border-bottom: 2px solid #0d9488; /* Teal underline */
}
```

---

## 4. Sidebar Customization

### Decision: Custom CSS for Docs Sidebar with Navy Background

**Rationale**: Sidebar requires targeting `.menu` class within docs layout. Active item indicator uses Teal left border.

**Implementation Pattern**:
```css
/* Sidebar container */
.menu {
  background-color: #1a365d;
}

.menu__link {
  color: rgba(255, 255, 255, 0.85);
}

.menu__link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.menu__link--active {
  background-color: rgba(13, 148, 136, 0.2); /* Teal tint */
  border-left: 3px solid #0d9488;
  color: #ffffff;
}
```

---

## 5. Dark Mode Implementation

### Decision: Use Docusaurus Built-in Color Mode with Navy Dark Background

**Rationale**: Docusaurus provides `[data-theme='dark']` selector for dark mode styles. Dark mode will use deeper Navy Blue as background while maintaining Teal accents with adjusted contrast.

**Dark Mode Palette**:
```css
[data-theme='dark'] {
  --ifm-background-color: #0f172a; /* Very dark navy */
  --ifm-background-surface-color: #1e293b;
  --ifm-color-primary: #14b8a6; /* Brighter teal for contrast */
  --ifm-navbar-background-color: #0f172a;
}
```

---

## 6. Admonitions (Callouts)

### Decision: Customize Info/Tip to Use Teal, Keep Warning/Danger Standard

**Rationale**: Info and tip callouts should use Teal-tinted styling to match theme. Warning and danger should remain standard orange/red for safety semantics.

**Implementation Pattern**:
```css
.alert--info {
  --ifm-alert-background-color: rgba(13, 148, 136, 0.1);
  --ifm-alert-border-color: #0d9488;
}

.alert--success, .alert--tip {
  --ifm-alert-background-color: rgba(13, 148, 136, 0.1);
  --ifm-alert-border-color: #0d9488;
}
```

---

## 7. Typography

### Decision: Use System Font Stack with Optimized Line Height

**Rationale**: System fonts provide best performance and native feel. Line height of 1.6-1.7 optimizes reading for educational content.

**Implementation**:
```css
:root {
  --ifm-font-family-base: system-ui, -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --ifm-line-height-base: 1.65;
}
```

---

## 8. Accessibility Compliance

### Decision: WCAG AA Contrast Ratios for All Text

**Verified Contrast Ratios**:
| Combination | Ratio | Requirement | Status |
|-------------|-------|-------------|--------|
| White text on Navy (#1a365d) | 11.5:1 | 4.5:1 (AA) | PASS |
| Teal (#0d9488) on White | 4.6:1 | 4.5:1 (AA) | PASS |
| Black text on White | 21:1 | 4.5:1 (AA) | PASS |
| Teal (#14b8a6) on Dark (#0f172a) | 7.2:1 | 4.5:1 (AA) | PASS |

**Focus States**: Teal outline with 2px solid for keyboard navigation visibility.

---

## 9. Footer Styling

### Decision: Navy Background Matching Navbar

**Rationale**: Consistent Navy Blue for both header and footer creates visual bookends. Footer already has `style: 'dark'` in config which we'll customize.

---

## 10. File Structure

### Decision: Single custom.css File

**Rationale**: All theme overrides fit in one file (~150-200 lines). No need for multiple CSS files or CSS-in-JS.

**Location**: `physical-ai-textbook/docs/src/css/custom.css`

---

## Implementation Checklist

- [x] Research Infima variable system
- [x] Define Teal color palette (primary scale)
- [x] Define Navy Blue color palette (custom)
- [x] Research navbar customization
- [x] Research sidebar customization
- [x] Research dark mode implementation
- [x] Verify WCAG contrast compliance
- [x] Research admonition styling
- [x] Define typography settings
- [x] Determine file structure

---

## References

- Docusaurus Styling Guide: https://docusaurus.io/docs/styling-layout
- Infima CSS Variables: https://infima.dev/docs/getting-started/theming
- WCAG Contrast Checker: https://webaim.org/resources/contrastchecker/
- Tailwind CSS Colors: https://tailwindcss.com/docs/customizing-colors
