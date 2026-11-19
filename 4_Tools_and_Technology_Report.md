# Tools & Technology Stack Technical Report

**Project Name:** TruthLens AI &mdash; AI-Based Fake News Detection System  
**Document Category:** Technology Stack, Library Ecosystem & Mathematical Formulations  
**PDF Document:** [Tools_and_Technology_Report.pdf](file:///C:/Users/Vikash/.gemini/antigravity/scratch/fake-news-detector/docs_and_reports/Tools_and_Technology_Report.pdf)  

---

## 1. Complete Technology Inventory

| Layer | Component | Version | Description & Role |
| :--- | :--- | :--- | :--- |
| **Language Runtime** | Python | 3.14.7 | Primary server-side execution environment |
| **Mathematical Engine** | NumPy | 2.5.4 | Vectorized linear algebra, array broadcasting, and L2 norms |
| **Web Application** | Flask | 3.1.3 | Lightweight WSGI web framework & REST routing |
| **Embedded Database** | SQLite | 3.x | File-based ACID relational database (`truthlens.db`) |
| **PDF Engine** | fpdf2 | 2.8.9 | Programmatic PDF document compilation |
| **Frontend Markup** | HTML5 | Living Std | Semantic, accessible DOM structure |
| **Styling & Theme** | CSS3 | Living Std | Responsive grid, flexbox, glassmorphic filters, CSS variables |
| **Client Scripting** | JavaScript | ES6+ | Asynchronous Fetch API, DOM manipulation, state sync |

---

## 2. Natural Language Processing (NLP) Pipeline (`nlp_pipeline.py`)

### A. Text Normalization (`clean_text`)
Raw textual inputs are sanitized using compiled regular expressions:
1. **URL Removal:** `re.sub(r'http\S+|www\.\S+', ' ', text)` removes URLs.
2. **HTML Stripping:** `re.sub(r'<.*?>', ' ', text)` strips HTML markup.
3. **Punctuation Normalization:** `re.sub(r'[^a-zA-Z\s]', ' ', text)` retains alphabetic characters and spaces.
4. **Lowercasing & Whitespace Collapsing:** Converts text to lowercase and removes duplicate spaces.

### B. Stopword Filtering & N-Gram Tokenization (`tokenize`)
- Words matching 120+ standard English stopwords (e.g. `and`, `the`, `is`, `which`) are filtered out.
- Unigrams ($N=1$) and Bigrams ($N=2$, e.g., `secret_cure`, `flat_earth`) are generated. Bigrams are critical for capturing deceptive compound phrases.

### C. TF-IDF Vectorization (`TfidfVectorizerModel`)
Implemented purely with NumPy to avoid blocked native C-extension DLLs:
1. **Sublinear Term Frequency:**
   $$\text{TF}(t, d) = 1 + \ln(\text{count}(t, d))$$
2. **Smooth Inverse Document Frequency:**
   $$\text{IDF}(t) = \ln\left(\frac{1 + N}{1 + \text{DF}(t)}\right) + 1$$
3. **L2 Vector Normalization:**
   $$v_{\text{norm}} = \frac{v}{\|v\|_2} = \frac{v}{\sqrt{\sum v_i^2}}$$

### D. Stylistic Forensics Scorer (`extract_linguistic_features`)
- **Capitalization Ratio:** Percentage of uppercase characters (alarmist screaming).
- **Urgency Punctuation:** Count of exclamation marks (`!`) and question marks (`?`).
- **Sensationalism Score (0–100):** Weighted frequency of high-probability misinformation trigger words (`shocking`, `miracle`, `secret`, `banned`, `they don't want you to know`).

---

## 3. Machine Learning Algorithms (`ml_models.py`)

### Algorithm 1: Logistic Regression Classifier with L2 Regularization
- **Hypothesis Function:**
  $$P(y=1|x) = \sigma(w^T x + b) = \frac{1}{1 + e^{-(w^T x + b)}}$$
- **Objective Function (Binary Cross-Entropy with L2 Penalty):**
  $$J(w, b) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)} \ln(p^{(i)}) + (1 - y^{(i)}) \ln(1 - p^{(i)}) \right] + \frac{\lambda}{2} \|w\|_2^2$$
- **Optimization:** Gradient Descent with Momentum ($\beta=0.85$, Learning Rate $\alpha=0.8$).

### Algorithm 2: Multinomial Naive Bayes Classifier
- **Posterior Probability Formulation:**
  $$\log P(c|d) \propto \log P(c) + \sum_{i=1}^n x_i \log P(w_i|c)$$
- **Laplace Additive Smoothing ($\alpha=1.0$):**
  $$P(w_i|c) = \frac{\sum x_{i, c} + \alpha}{\sum_{k} \sum x_{k, c} + \alpha \cdot |V|}$$
- Softmax is applied to log-probabilities to compute well-calibrated confidence scores.
