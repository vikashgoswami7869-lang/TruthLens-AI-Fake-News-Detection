<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TruthLens AI &mdash; AI-Based Fake News Detection System</title>
    <link rel="stylesheet" href="/static/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Top Navbar -->
    <header class="app-nav">
        <div class="container nav-wrapper">
            <div class="brand">
                <div class="logo-shield">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                        <path d="m9 12 2 2 4-4"/>
                    </svg>
                </div>
                <div class="brand-text">
                    <span class="brand-name">TruthLens <span class="ai-badge">AI</span></span>
                    <span class="brand-tagline">AI-Based Fake News Detection System</span>
                </div>
            </div>

            <div class="nav-system-status">
                <span class="status-dot"></span>
                <span class="status-text">NLP Pipeline Active</span>
                <span class="model-tag">Dual Classifier Engine</span>
            </div>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="tab-control-bar">
        <div class="container tab-control-wrapper">
            <button class="nav-tab active" data-tab="tab-detector">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                News Verification
            </button>
            <button class="nav-tab" data-tab="tab-analytics">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                Model Benchmarks
            </button>
            <button class="nav-tab" data-tab="tab-history">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="10"/></svg>
                Verification Audit Logs
            </button>
            <button class="nav-tab" data-tab="tab-api">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
                Developer API
            </button>
        </div>
    </div>

    <!-- Main Workspace -->
    <main class="container main-container">

        <!-- ================= TAB 1: NEWS VERIFICATION ================= -->
        <section id="tab-detector" class="tab-pane active">
            <div class="app-grid">
                
                <!-- Left Input Console -->
                <div class="glass-card input-card">
                    <div class="card-head">
                        <div>
                            <h2 class="card-title">Analyze News Content</h2>
                            <p class="card-subtitle">Paste a headline, claim, or complete article paragraph to extract forensic NLP signals</p>
                        </div>
                        <div class="model-select-wrapper">
                            <label for="modelSelect">Algorithm:</label>
                            <select id="modelSelect" class="modern-select">
                                <option value="logistic_regression" selected>Logistic Regression (L2 Regularized)</option>
                                <option value="naive_bayes">Multinomial Naive Bayes</option>
                            </select>
                        </div>
                    </div>

                    <!-- Preset Samples -->
                    <div class="samples-container">
                        <span class="samples-title">Try verified test cases:</span>
                        <div class="sample-pills">
                            <button class="pill pill-real" data-sample="real_space">
                                <span class="pill-dot"></span> Space Discovery (Real)
                            </button>
                            <button class="pill pill-real" data-sample="real_health">
                                <span class="pill-dot"></span> WHO Health Bulletin (Real)
                            </button>
                            <button class="pill pill-real" data-sample="real_transit">
                                <span class="pill-dot"></span> Clean Energy Grid (Real)
                            </button>
                            <button class="pill pill-fake" data-sample="fake_cure">
                                <span class="pill-dot"></span> Cancer Miracle Cure (Fake)
                            </button>
                            <button class="pill pill-fake" data-sample="fake_earth">
                                <span class="pill-dot"></span> Flat Earth Conspiracy (Fake)
                            </button>
                            <button class="pill pill-fake" data-sample="fake_microchip">
                                <span class="pill-dot"></span> 5G Water Nanobots (Fake)
                            </button>
                        </div>
                    </div>

                    <!-- Text Area -->
                    <div class="input-area-box">
                        <textarea id="newsInput" placeholder="Paste news headline, editorial statement, or social media post here..." rows="7"></textarea>
                        <div class="input-tools">
                            <div class="word-counter" id="textStats">0 characters &bull; 0 words &bull; ~0 min read</div>
                            <div class="tool-actions">
                                <button id="pasteBtn" class="btn-tool">Paste</button>
                                <button id="clearBtn" class="btn-tool">Clear</button>
                            </div>
                        </div>
                    </div>

                    <!-- Action Trigger -->
                    <div class="action-footer">
                        <button id="analyzeBtn" class="btn-glow-primary">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                            <span class="btn-label">Run Credibility Analysis</span>
                            <span class="btn-spinner hidden"></span>
                        </button>
                    </div>

                    <!-- Feature Capabilities -->
                    <div class="features-summary-strip">
                        <div class="summary-chip">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m7 11 2-2-2-2"/><path d="M11 13h4"/><rect width="18" height="18" x="3" y="3" rx="2"/></svg>
                            TF-IDF N-Grams (1,2)
                        </div>
                        <div class="summary-chip">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
                            Clickbait Sensationalism Scorer
                        </div>
                        <div class="summary-chip">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
                            Explainable Word Attribution
                        </div>
                    </div>
                </div>

                <!-- Right Output Console -->
                <div class="glass-card result-card" id="resultCard">
                    
                    <!-- Empty State Placeholder -->
                    <div class="empty-state" id="emptyState">
                        <div class="empty-icon-glow">
                            <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                        </div>
                        <h3>Engine Ready for Analysis</h3>
                        <p>Submit any news article or click one of the preset samples on the left to inspect prediction confidence, sensationalism score, and influential keywords.</p>
                    </div>

                    <!-- Live Dynamic Results -->
                    <div class="result-dynamic hidden" id="resultDynamic">
                        
                        <!-- High-Impact Verdict Banner -->
                        <div class="verdict-banner" id="verdictBanner">
                            <div class="verdict-badge-side">
                                <span class="verdict-tag" id="verdictTag">VERDICT CLASSIFICATION</span>
                                <h2 class="verdict-main" id="verdictMain">VERIFIED REAL NEWS</h2>
                                <span class="verdict-desc" id="verdictDesc">Article conforms to objective reporting patterns</span>
                            </div>
                            <div class="credibility-meter">
                                <div class="meter-number" id="credibilityScore">96.4</div>
                                <div class="meter-label">Credibility Index</div>
                            </div>
                        </div>

                        <!-- Probabilities Bar -->
                        <div class="metrics-block">
                            <div class="meter-header">
                                <span>Distribution Assessment:</span>
                                <div class="meter-stats">
                                    <span class="stat-fake">Fake: <strong id="probFake">3.6%</strong></span>
                                    <span class="stat-divider">&bull;</span>
                                    <span class="stat-real">Real: <strong id="probReal">96.4%</strong></span>
                                </div>
                            </div>
                            <div class="dual-progress-bar">
                                <div class="bar-fill-fake" id="barFake" style="width: 4%;"></div>
                                <div class="bar-fill-real" id="barReal" style="width: 96%;"></div>
                            </div>
                        </div>

                        <!-- Forensic Linguistic Metrics -->
                        <div class="forensics-grid">
                            <div class="forensic-tile">
                                <span class="tile-caption">Sensationalism Score</span>
                                <div class="tile-stat" id="lingSensational">12/100</div>
                                <span class="tile-pill" id="lingRisk">Low Risk</span>
                            </div>
                            <div class="forensic-tile">
                                <span class="tile-caption">Emotional Tone</span>
                                <div class="tile-stat small" id="lingTone">Objective</div>
                                <span class="tile-pill neutral">Sentiment</span>
                            </div>
                            <div class="forensic-tile">
                                <span class="tile-caption">Uppercase Ratio</span>
                                <div class="tile-stat" id="lingCaps">6.8%</div>
                                <span class="tile-pill neutral">Grammar</span>
                            </div>
                            <div class="forensic-tile">
                                <span class="tile-caption">Exclamations</span>
                                <div class="tile-stat" id="lingExcl">0</div>
                                <span class="tile-pill neutral">Punctuation</span>
                            </div>
                        </div>

                        <!-- Influential Keywords -->
                        <div class="keyword-attribution-box">
                            <div class="box-head">
                                <span class="box-title">Identified Key Influencers</span>
                                <span class="box-hint">Terms that weighed most on the classification</span>
                            </div>
                            <div class="chips-container" id="keywordChips"></div>
                        </div>

                        <!-- Explainability Reasons -->
                        <div class="reasons-box">
                            <div class="box-head">
                                <span class="box-title">Algorithmic Reasoning</span>
                            </div>
                            <ul class="reasons-list" id="reasonsList"></ul>
                        </div>

                        <!-- Interactive Verification Checklist -->
                        <div class="checklist-box">
                            <div class="box-head">
                                <span class="box-title">Fact-Checking Best Practices</span>
                            </div>
                            <div class="check-items">
                                <label class="check-item">
                                    <input type="checkbox" checked disabled>
                                    <span>Cross-checked against established wire services (Reuters, AP, PTI)</span>
                                </label>
                                <label class="check-item">
                                    <input type="checkbox" checked disabled>
                                    <span>Analyzed headline for emotional manipulation & clickbait keywords</span>
                                </label>
                                <label class="check-item">
                                    <input type="checkbox" checked disabled>
                                    <span>Examined direct quotation authenticity and named source attribution</span>
                                </label>
                            </div>
                        </div>

                    </div>
                </div>

            </div>
        </section>

        <!-- ================= TAB 2: MODEL BENCHMARKS ================= -->
        <section id="tab-analytics" class="tab-pane">
            <div class="glass-card">
                <div class="card-head">
                    <div>
                        <h2 class="card-title">Model Performance & Evaluation Metrics</h2>
                        <p class="card-subtitle">Validated against an independent hold-out test set with balanced ground truth</p>
                    </div>
                    <button id="refreshMetricsBtn" class="btn-outline">Recalculate Metrics</button>
                </div>

                <!-- 4 KPI Cards -->
                <div class="kpi-banner">
                    <div class="kpi-item cyan">
                        <span class="kpi-name">Overall Accuracy</span>
                        <div class="kpi-metric" id="metricAcc">100.0%</div>
                        <span class="kpi-sub">Total correct predictions</span>
                    </div>
                    <div class="kpi-item emerald">
                        <span class="kpi-name">Precision</span>
                        <div class="kpi-metric" id="metricPrec">100.0%</div>
                        <span class="kpi-sub">Reliability of positive real labels</span>
                    </div>
                    <div class="kpi-item purple">
                        <span class="kpi-name">Recall</span>
                        <div class="kpi-metric" id="metricRecall">100.0%</div>
                        <span class="kpi-sub">Coverage of verified articles</span>
                    </div>
                    <div class="kpi-item amber">
                        <span class="kpi-name">F1-Score</span>
                        <div class="kpi-metric" id="metricF1">100.0%</div>
                        <span class="kpi-sub">Balanced harmonic mean</span>
                    </div>
                </div>

                <!-- Confusion Matrix & Architecture -->
                <div class="analytics-split mt-4">
                    <div class="inner-card">
                        <h3>Hold-out Confusion Matrix</h3>
                        <p class="inner-desc">Distribution of actual vs predicted classes on unseen evaluation samples.</p>
                        
                        <div class="cm-wrapper">
                            <div class="cm-table">
                                <div class="cm-cell empty"></div>
                                <div class="cm-cell col-hdr">Pred: Real</div>
                                <div class="cm-cell col-hdr">Pred: Fake</div>

                                <div class="cm-cell row-hdr">True: Real</div>
                                <div class="cm-cell cell-pos" id="cmTP">TP: 11</div>
                                <div class="cm-cell cell-neg" id="cmFN">FN: 0</div>

                                <div class="cm-cell row-hdr">True: Fake</div>
                                <div class="cm-cell cell-neg" id="cmFP">FP: 0</div>
                                <div class="cm-cell cell-pos" id="cmTN">TN: 9</div>
                            </div>
                        </div>
                    </div>

                    <div class="inner-card">
                        <h3>Classifier Comparison</h3>
                        <p class="inner-desc">Comparison between the deployed classification architectures.</p>
                        <table class="benchmark-table">
                            <thead>
                                <tr>
                                    <th>Algorithm</th>
                                    <th>Accuracy</th>
                                    <th>Precision</th>
                                    <th>Recall</th>
                                    <th>F1-Score</th>
                                </tr>
                            </thead>
                            <tbody id="benchmarkBody">
                                <tr>
                                    <td><strong>Logistic Regression (L2)</strong></td>
                                    <td>100.0%</td>
                                    <td>100.0%</td>
                                    <td>100.0%</td>
                                    <td>100.0%</td>
                                </tr>
                                <tr>
                                    <td><strong>Multinomial Naive Bayes</strong></td>
                                    <td>100.0%</td>
                                    <td>100.0%</td>
                                    <td>100.0%</td>
                                    <td>100.0%</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Deep Pipeline Architecture Breakdown -->
                <div class="inner-card mt-4">
                    <h3>Pipeline & Linguistic Architecture</h3>
                    <div class="pipeline-steps-grid">
                        <div class="pipeline-step">
                            <span class="step-num">01</span>
                            <h4>Text Normalization</h4>
                            <p>URL removal, HTML strip, lowercase conversion, and non-alphabet character scrubbing.</p>
                        </div>
                        <div class="pipeline-step">
                            <span class="step-num">02</span>
                            <h4>Tokenization & N-Grams</h4>
                            <p>Stopword filtering, unigrams & bigrams expansion to detect compound misinformation cues.</p>
                        </div>
                        <div class="pipeline-step">
                            <span class="step-num">03</span>
                            <h4>TF-IDF Feature Space</h4>
                            <p>Sublinear term frequency scaling with smooth inverse document frequency and L2 normalization.</p>
                        </div>
                        <div class="pipeline-step">
                            <span class="step-num">04</span>
                            <h4>Linguistic Heuristics</h4>
                            <p>Supervised sensationalism scoring, capitalization ratio, and credible source attribution boosts.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ================= TAB 3: AUDIT LOGS ================= -->
        <section id="tab-history" class="tab-pane">
            <div class="glass-card">
                <div class="card-head">
                    <div>
                        <h2 class="card-title">Verification Audit Logs</h2>
                        <p class="card-subtitle">Real-time log of verified claims and articles stored in local SQLite database</p>
                    </div>
                    <div class="action-btn-group">
                        <button id="refreshHistoryBtn" class="btn-outline">Refresh Logs</button>
                        <button id="clearHistoryBtn" class="btn-danger">Clear All Logs</button>
                    </div>
                </div>

                <!-- Stats summary -->
                <div class="audit-stats-bar">
                    <div class="audit-stat">
                        <span class="audit-num" id="statTotal">0</span>
                        <span class="audit-lbl">Total Checks</span>
                    </div>
                    <div class="audit-stat">
                        <span class="audit-num text-fake" id="statFake">0</span>
                        <span class="audit-lbl">Disinformation Flagged</span>
                    </div>
                    <div class="audit-stat">
                        <span class="audit-num text-real" id="statReal">0</span>
                        <span class="audit-lbl">Verified Credible</span>
                    </div>
                    <div class="audit-stat">
                        <span class="audit-num text-accent" id="statAvgConf">0.0%</span>
                        <span class="audit-lbl">Mean Confidence</span>
                    </div>
                </div>

                <!-- History Table -->
                <div class="table-container mt-3">
                    <table class="benchmark-table">
                        <thead>
                            <tr>
                                <th style="width: 70px;">Record ID</th>
                                <th>Submitted Text Content</th>
                                <th style="width: 140px;">Verdict</th>
                                <th style="width: 130px;">Confidence</th>
                                <th style="width: 180px;">Logged At</th>
                            </tr>
                        </thead>
                        <tbody id="historyBody">
                            <tr><td colspan="5" style="text-align: center; color: #64748b; padding: 25px;">Loading audit logs...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- ================= TAB 4: DEVELOPER API ================= -->
        <section id="tab-api" class="tab-pane">
            <div class="glass-card">
                <div class="card-head">
                    <div>
                        <h2 class="card-title">Developer REST API Specifications</h2>
                        <p class="card-subtitle">Integrate real-time news credibility assessment into web browsers, bots, or apps</p>
                    </div>
                </div>

                <div class="api-container">
                    <div class="api-method-banner">
                        <span class="badge-post">POST</span>
                        <code class="code-url">http://127.0.0.1:5000/api/predict</code>
                    </div>

                    <h4>Request Format (JSON)</h4>
                    <pre><code class="language-json">{
  "text": "NASA James Webb Space Telescope discovers ancient galaxy cluster...",
  "model": "logistic_regression"  // Options: "logistic_regression" | "naive_bayes"
}</code></pre>

                    <h4>Response Payload (JSON)</h4>
                    <pre><code class="language-json">{
  "success": true,
  "label": "Real",
  "confidence": 88.5,
  "credibility_score": 88.5,
  "probabilities": {
    "Real": 88.5,
    "Fake": 11.5
  },
  "model_used": "Logistic Regression",
  "linguistic_analysis": {
    "sensational_score": 4.5,
    "clickbait_risk": "Low",
    "tone": "Objective / Formal",
    "caps_ratio": 7.4,
    "exclamation_count": 0
  },
  "influential_words": [
    {"word": "space", "impact": "Real", "score": 1.035},
    {"word": "cluster", "impact": "Real", "score": 0.474}
  ],
  "explanation": [
    "Identified verified attribution markers: official, research",
    "Article exhibits neutral tone and terminology consistent with credible journalistic standards"
  ]
}</code></pre>

                    <h4 class="mt-4">Integration Code Snippets</h4>
                    
                    <div class="code-tabs">
                        <div class="code-box">
                            <strong>cURL</strong>
                            <pre><code>curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "SHOCKING BREAKING: Secret cure discovered!"}'</code></pre>
                        </div>

                        <div class="code-box mt-3">
                            <strong>Python (requests)</strong>
                            <pre><code>import requests

res = requests.post("http://127.0.0.1:5000/api/predict", json={
    "text": "World Health Organization announces seasonal flu update.",
    "model": "logistic_regression"
})
data = res.json()
print("Verdict:", data['label'], "| Confidence:", data['confidence'])</code></pre>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- App Footer -->
    <footer class="app-footer">
        <div class="container footer-wrapper">
            <p>&copy; 2026 TruthLens AI &bull; AI-Based Fake News Detection System</p>
            <p class="footer-sub">Built with pure Python, NumPy, and Flask REST Architecture</p>
        </div>
    </footer>

    <script src="/static/app.js"></script>
</body>
</html>
