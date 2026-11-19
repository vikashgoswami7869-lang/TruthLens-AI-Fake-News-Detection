"""
TruthLens AI - Command-Line Prediction Interface
"""

import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from predictor import predictor_instance


def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("\nEnter news headline or article: ").strip()

    if not text:
        print("Error: Input text is empty.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("TRUTHLENS AI - ANALYZING NEWS ARTICLE...")
    print("=" * 60)

    res = predictor_instance.predict(text, model_type='logistic_regression')
    if not res.get('success'):
        print("Error:", res.get('error'))
        return

    label = res['label']
    confidence = res['confidence']
    badge = "[FAKE / DISINFORMATION]" if label == "Fake" else "[REAL / CREDIBLE]"

    print(f"\nVerdict:           {badge}")
    print(f"Confidence:        {confidence}%")
    print(f"Credibility Score: {res['credibility_score']}/100")
    print(f"Model Algorithm:   {res['model_used']}")
    print(f"Probabilities:     Fake: {res['probabilities']['Fake']}% | Real: {res['probabilities']['Real']}%")

    print("\nLinguistic Features:")
    ling = res['linguistic_analysis']
    print(f" - Words: {ling['word_count']} | Tone: {ling['tone']} | Uppercase: {ling['caps_ratio']}% | Exclamations: {ling['exclamation_count']}")
    print(f" - Sensationalism: {ling['sensational_score']}/100 (Risk: {ling['clickbait_risk']})")
    if ling['sensational_hits']:
        print(f" - Sensational Triggers: {', '.join(ling['sensational_hits'])}")
    if ling['credible_hits']:
        print(f" - Credible Attributions: {', '.join(ling['credible_hits'])}")

    if res['influential_words']:
        print("\nTop Contributing Words:")
        for w in res['influential_words']:
            print(f" - '{w['word']}' -> points to {w['impact']} (weight: {w['score']})")

    print("\nReasoning:")
    for reason in res['explanation']:
        print(f" - {reason}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
