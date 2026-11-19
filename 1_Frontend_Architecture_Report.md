# Frontend Architecture & User Interface Design Report

**Project Name:** TruthLens AI &mdash; AI-Based Fake News Detection System  
**Document Category:** Technical Architecture & Client-Side Design  
**Tech Stack:** HTML5, CSS3 Glassmorphism, Vanilla ES6+ JavaScript  
**PDF Document:** [Frontend_Architecture_Report.pdf](file:///C:/Users/Vikash/.gemini/antigravity/scratch/fake-news-detector/docs_and_reports/Frontend_Architecture_Report.pdf)  

---

## 1. Executive Summary & Design Philosophy
The frontend of TruthLens AI is designed to deliver a high-velocity, responsive, and cognitively intuitive interface for verifying news authenticity. Rather than relying on heavy client-side frameworks with complex compilation overhead, the application is engineered with pure **semantic HTML5**, **CSS3 Custom Properties (Variables)**, and **Vanilla ES6+ JavaScript**.

### Key Design Priorities
- **Sub-10ms UI Responsiveness:** Zero compilation or bundle overhead ensures instantaneous rendering.
- **Glassmorphic Cyberpunk Theme:** A modern dark slate canvas (`#060911`) paired with subtle backdrop blurs (12px), translucent panels, and vibrant accent colors.
- **Dual Visual Signaling:** Green (`#10b981`) for Verified Real News and Rose/Crimson (`#f43f5e`) for Disinformation Flags.
- **Zero-Refresh Workflow:** Asynchronous Fetch API enables dynamic verification without full-page reloads.

---

## 2. Component Hierarchy & User Interface Layout

```
├── Top Navigation Bar (Header)
│   ├── TruthLens Shield Logo & Gradient AI Badge
│   ├── Subtitle: "AI-Based Fake News Detection System"
│   └── Live System Status Pill ("NLP Pipeline Active • Dual Classifier Engine")
│
├── Tab Control Navigation
│   ├── [1] News Verification (Main Workspace)
│   ├── [2] Model Benchmarks (Confusion Matrix & Evaluation)
│   ├── [3] Verification Audit Logs (SQLite History)
│   └── [4] Developer API (Endpoint Specs & Code Samples)
│
├── Main Interactive Workspace
│   ├── Left Column: Input Console
│   │   ├── Model Algorithm Selector Dropdown
│   │   ├── 6 One-Click Curated Preset Test Pills
│   │   ├── Text Input Area with Auto-Focus
│   │   ├── Live Counter: Characters, Words & Read Time
│   │   └── Primary Action Button ("Run Credibility Analysis")
│   │
│   └── Right Column: Dynamic Output Console
│       ├── Empty State Placeholder (Pre-run)
│       ├── Verdict Banner (Real / Fake with Radial Glow)
│       ├── Credibility Index (0 - 100 Meter)
│       ├── Dual Progress Bar: Real % vs Fake %
│       ├── Forensics Grid (Sensationalism, Tone, Caps Ratio, Exclamations)
│       ├── Explainable AI (XAI) Colored Keyword Chips
│       ├── Algorithmic Reasoning Explanations
│       └── Interactive Fact-Checking Action Checklist
│
└── Application Footer
    └── Copyright, System Version & Architecture Attribution
```

---

## 3. Curated 1-Click Test Presets
The UI includes 6 built-in test pills to enable immediate demonstration of diverse journalistic domains:

| Preset Button | Category | Domain | Expected Behavior |
| :--- | :--- | :--- | :--- |
| **Space Discovery** | Real News | Astronomy & Deep Space | Formal vocabulary, NASA citations, low sensationalism (0-10) |
| **WHO Health Bulletin** | Real News | Public Health | Official epidemiological indicators, neutral tone |
| **Clean Energy Grid** | Real News | Power & Infrastructure | Departmental press style, zero clickbait triggers |
| **Cancer Miracle Cure** | Fake News | Health Misinformation | High clickbait score (90+), flags *secret*, *miracle*, *24 hours* |
| **Flat Earth Conspiracy** | Fake News | Pseudoscience Hoax | High uppercase shouting ratio, flags conspiracy terms |
| **5G Water Nanobots** | Fake News | Tech Paranoia | Detects conspiracy patterns (*Bill Gates*, *nanobots*, *mind-control*) |

---

## 4. CSS Architecture & Theme Tokens

The application stylesheet (`static/style.css`) defines central theme tokens:

```css
:root {
    --bg-base: #060911;           /* Deep obsidian main background */
    --bg-surface: #0c121e;        /* Dark slate card container */
    --bg-card: #111a2d;           /* Glassmorphic panel background */
    --border: #1e2c47;            /* Subtle card border */
    --text-primary: #f8fafc;      /* High-contrast body text */
    --text-secondary: #94a3b8;    /* Muted label text */
    --real: #10b981;              /* Verified Green */
    --real-glow: rgba(16, 185, 129, 0.25);
    --fake: #f43f5e;              /* Alert Crimson */
    --fake-glow: rgba(244, 63, 94, 0.28);
}
```

---

## 5. JavaScript Asynchronous Event Flow (`static/app.js`)
1. **Input Listener:** Listens to `input` event on textarea and calculates words, characters, and estimated read time.
2. **Preset Pill Click:** Automatically populates textarea and invokes `runAnalysis()`.
3. **API Dispatch:** Dispatches asynchronous `fetch('/api/predict', { method: 'POST', body: JSON.stringify({ text, model }) })`.
4. **State Transition:** Toggles UI from `#emptyState` to `#resultDynamic`.
5. **DOM Mutation:** Dynamically constructs and injects keyword chips, reasons list, updates meter widths, and animates credibility score.
