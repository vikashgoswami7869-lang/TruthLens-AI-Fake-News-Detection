/**
 * TruthLens AI - Frontend Interactive Controller
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const newsInput = document.getElementById('newsInput');
    const textStats = document.getElementById('textStats');
    const clearBtn = document.getElementById('clearBtn');
    const pasteBtn = document.getElementById('pasteBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const modelSelect = document.getElementById('modelSelect');

    const emptyState = document.getElementById('emptyState');
    const resultDynamic = document.getElementById('resultDynamic');
    const verdictBanner = document.getElementById('verdictBanner');
    const verdictMain = document.getElementById('verdictMain');
    const verdictDesc = document.getElementById('verdictDesc');
    const credibilityScore = document.getElementById('credibilityScore');

    const probFake = document.getElementById('probFake');
    const probReal = document.getElementById('probReal');
    const barFake = document.getElementById('barFake');
    const barReal = document.getElementById('barReal');

    const lingSensational = document.getElementById('lingSensational');
    const lingRisk = document.getElementById('lingRisk');
    const lingTone = document.getElementById('lingTone');
    const lingCaps = document.getElementById('lingCaps');
    const lingExcl = document.getElementById('lingExcl');

    const keywordChips = document.getElementById('keywordChips');
    const reasonsList = document.getElementById('reasonsList');

    // Preset Sample News
    const PRESETS = {
        real_space: "NASA James Webb Space Telescope discovers ancient galaxy cluster forming in the early universe, confirming cosmological models of galactic evolution.",
        real_health: "World Health Organization publishes global influenza surveillance update noting regional seasonal infection trends and vaccine distribution recommendations.",
        real_transit: "Ministry of Power synchronizes ten gigawatt ultra-mega solar power park with national power transmission grid.",
        fake_cure: "SHOCKING BREAKING: Secret miracle vegetable cures all stage four cancers in 24 hours, Big Pharma is desperately trying to ban this video!",
        fake_earth: "UNBELIEVABLE: NASA admits Earth is completely flat and fake satellite photos were created in Hollywood basement to deceive humanity!",
        fake_microchip: "LEAKED DOCUMENTS: Bill Gates installs mind-control microchips inside daily tap water supplies to track everyone's thoughts via 5G towers!"
    };

    // 1. Tab Switching
    const tabButtons = document.querySelectorAll('.nav-tab');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-tab');
            tabButtons.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetPane = document.getElementById(targetId);
            if (targetPane) {
                targetPane.classList.add('active');
            }

            if (targetId === 'tab-history') {
                loadHistory();
            } else if (targetId === 'tab-analytics') {
                loadMetrics();
            }
        });
    });

    // 2. Character & Word Counting
    function updateTextStats() {
        const text = newsInput.value;
        const chars = text.length;
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        const readTime = Math.max(1, Math.ceil(words / 200));
        textStats.textContent = `${chars} characters • ${words} words • ~${readTime} min read`;
    }
    newsInput.addEventListener('input', updateTextStats);

    // 3. Paste from Clipboard
    if (pasteBtn) {
        pasteBtn.addEventListener('click', async () => {
            try {
                const text = await navigator.clipboard.readText();
                if (text) {
                    newsInput.value = text;
                    updateTextStats();
                }
            } catch (err) {
                alert('Clipboard access denied. Please paste directly using Ctrl+V.');
            }
        });
    }

    // 4. Clear Input
    clearBtn.addEventListener('click', () => {
        newsInput.value = '';
        updateTextStats();
        emptyState.classList.remove('hidden');
        resultDynamic.classList.add('hidden');
    });

    // 5. Presets
    document.querySelectorAll('.pill').forEach(pill => {
        pill.addEventListener('click', () => {
            const sampleKey = pill.getAttribute('data-sample');
            if (PRESETS[sampleKey]) {
                newsInput.value = PRESETS[sampleKey];
                updateTextStats();
                runAnalysis();
            }
        });
    });

    // 6. Run Analysis
    analyzeBtn.addEventListener('click', runAnalysis);

    async function runAnalysis() {
        const text = newsInput.value.trim();
        if (!text) {
            alert('Please paste or type a news headline or article to analyze.');
            newsInput.focus();
            return;
        }

        const model = modelSelect.value;
        analyzeBtn.disabled = true;
        const btnLabel = analyzeBtn.querySelector('.btn-label');
        const originalText = btnLabel.textContent;
        btnLabel.textContent = 'Processing Forensic NLP...';

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, model })
            });

            const data = await response.json();
            if (!data.success) {
                alert('Analysis Error: ' + (data.error || 'Server error'));
                return;
            }

            renderResults(data);
        } catch (err) {
            console.error(err);
            alert('Unable to connect to TruthLens AI backend service.');
        } finally {
            analyzeBtn.disabled = false;
            btnLabel.textContent = originalText;
        }
    }

    // 7. Render Analysis Results
    function renderResults(data) {
        emptyState.classList.add('hidden');
        resultDynamic.classList.remove('hidden');

        const isFake = data.label === 'Fake';
        verdictBanner.className = 'verdict-banner ' + (isFake ? 'fake' : 'real');
        verdictMain.textContent = isFake ? '🚨 DISINFORMATION / FAKE NEWS' : '✅ VERIFIED REAL NEWS';
        verdictDesc.textContent = isFake
            ? 'Article contains high sensationalism, unverified claims, or disinformation cues'
            : 'Article conforms to objective journalistic vocabulary and reporting standards';

        credibilityScore.textContent = data.credibility_score.toFixed(1);

        // Probabilities Bar
        const pFake = data.probabilities.Fake;
        const pReal = data.probabilities.Real;
        probFake.textContent = pFake.toFixed(1) + '%';
        probReal.textContent = pReal.toFixed(1) + '%';
        barFake.style.width = pFake + '%';
        barReal.style.width = pReal + '%';

        // Linguistic Forensics
        const ling = data.linguistic_analysis;
        lingSensational.textContent = `${ling.sensational_score}/100`;
        lingRisk.textContent = `${ling.clickbait_risk} Risk`;
        lingRisk.className = 'tile-pill ' + (ling.clickbait_risk === 'Low' ? 'low' : '');
        lingTone.textContent = ling.tone || 'Neutral';
        lingCaps.textContent = `${ling.caps_ratio}%`;
        lingExcl.textContent = ling.exclamation_count;

        // Keyword Attribution Chips
        keywordChips.innerHTML = '';
        if (data.influential_words && data.influential_words.length > 0) {
            data.influential_words.forEach(item => {
                const span = document.createElement('span');
                span.className = 'chip ' + (item.impact === 'Real' ? 'real' : 'fake');
                span.innerHTML = `<strong>${item.word}</strong> <small>(${item.impact}: ${item.score})</small>`;
                keywordChips.appendChild(span);
            });
        } else {
            keywordChips.innerHTML = '<span style="color:#64748b; font-size:0.82rem;">Standard journalistic vocabulary detected.</span>';
        }

        // Reasons
        reasonsList.innerHTML = '';
        if (data.explanation && data.explanation.length > 0) {
            data.explanation.forEach(exp => {
                const li = document.createElement('li');
                li.textContent = exp;
                reasonsList.appendChild(li);
            });
        }
    }

    // 8. Load Audit Logs (Tab 3)
    async function loadHistory() {
        const historyBody = document.getElementById('historyBody');
        const statTotal = document.getElementById('statTotal');
        const statFake = document.getElementById('statFake');
        const statReal = document.getElementById('statReal');
        const statAvgConf = document.getElementById('statAvgConf');

        try {
            const res = await fetch('/api/history');
            const data = await res.json();
            if (!data.success) return;

            statTotal.textContent = data.stats.total_predictions;
            statFake.textContent = data.stats.fake_predictions;
            statReal.textContent = data.stats.real_predictions;
            statAvgConf.textContent = data.stats.average_confidence + '%';

            if (!data.history || data.history.length === 0) {
                historyBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:#64748b; padding:25px;">No verification logs recorded in SQLite database yet.</td></tr>';
                return;
            }

            historyBody.innerHTML = '';
            data.history.forEach(item => {
                const tr = document.createElement('tr');
                const isFake = item.predicted_label === 'Fake';
                const badgeColor = isFake ? '#fb7185' : '#34d399';
                tr.innerHTML = `
                    <td style="font-family:'JetBrains Mono'; color:#64748b;">#${item.id}</td>
                    <td style="max-width:420px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${item.input_text}">
                        ${item.input_text}
                    </td>
                    <td><strong style="color:${badgeColor};">${item.predicted_label === 'Fake' ? '🚨 Fake' : '✅ Real'}</strong></td>
                    <td style="font-family:'JetBrains Mono';">${item.confidence}%</td>
                    <td style="color:#94a3b8; font-size:0.8rem;">${item.timestamp}</td>
                `;
                historyBody.appendChild(tr);
            });
        } catch (err) {
            console.error('Audit load error:', err);
        }
    }

    document.getElementById('refreshHistoryBtn').addEventListener('click', loadHistory);
    document.getElementById('clearHistoryBtn').addEventListener('click', async () => {
        if (!confirm('Are you sure you want to clear all verification audit logs?')) return;
        try {
            await fetch('/api/clear-history', { method: 'POST' });
            loadHistory();
        } catch (err) {
            console.error(err);
        }
    });

    // 9. Load Benchmark Metrics (Tab 2)
    async function loadMetrics() {
        try {
            const res = await fetch('/api/metrics');
            const data = await res.json();
            if (!data.success) return;

            const lr = data.metrics.logistic_regression;
            const nb = data.metrics.naive_bayes;

            document.getElementById('metricAcc').textContent = lr.accuracy.toFixed(1) + '%';
            document.getElementById('metricPrec').textContent = lr.precision.toFixed(1) + '%';
            document.getElementById('metricRecall').textContent = lr.recall.toFixed(1) + '%';
            document.getElementById('metricF1').textContent = lr.f1_score.toFixed(1) + '%';

            document.getElementById('cmTP').textContent = `TP: ${lr.confusion_matrix.tp}`;
            document.getElementById('cmTN').textContent = `TN: ${lr.confusion_matrix.tn}`;
            document.getElementById('cmFP').textContent = `FP: ${lr.confusion_matrix.fp}`;
            document.getElementById('cmFN').textContent = `FN: ${lr.confusion_matrix.fn}`;

            const benchmarkBody = document.getElementById('benchmarkBody');
            benchmarkBody.innerHTML = `
                <tr>
                    <td><strong>Logistic Regression (L2)</strong></td>
                    <td>${lr.accuracy.toFixed(1)}%</td>
                    <td>${lr.precision.toFixed(1)}%</td>
                    <td>${lr.recall.toFixed(1)}%</td>
                    <td>${lr.f1_score.toFixed(1)}%</td>
                </tr>
                <tr>
                    <td><strong>Multinomial Naive Bayes</strong></td>
                    <td>${nb.accuracy.toFixed(1)}%</td>
                    <td>${nb.precision.toFixed(1)}%</td>
                    <td>${nb.recall.toFixed(1)}%</td>
                    <td>${nb.f1_score.toFixed(1)}%</td>
                </tr>
            `;
        } catch (err) {
            console.error('Metrics load error:', err);
        }
    }

    document.getElementById('refreshMetricsBtn').addEventListener('click', loadMetrics);

    updateTextStats();
});
