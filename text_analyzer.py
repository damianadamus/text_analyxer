import string
import csv
import os
from collections import Counter

def analyze_text(text):
    """Performs statistical analysis on the provided text."""
    if not text.strip():
        return None

    char_count_with_spaces = len(text)
    char_count_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\r", ""))
    lines_count = len(text.splitlines())

    clean_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    words = clean_text.split()
    word_count = len(words)

    word_freq = Counter(words)
    most_common = word_freq.most_common(5)

    avg_word_len = sum(len(word) for word in words) / word_count if word_count > 0 else 0

    return {
        "chars_total": char_count_with_spaces,
        "chars_no_spaces": char_count_no_spaces,
        "words": word_count,
        "lines": lines_count,
        "avg_len": round(avg_word_len, 2),
        "most_common": most_common
    }

def save_to_csv(results, filename):
    """Saves the analysis results to a CSV file."""
    common_words_str = ", ".join([f"{word} ({count})" for word, count in results['most_common']])
    
    headers = [
        "Total Characters", 
        "Characters (no spaces)", 
        "Word Count", 
        "Line Count", 
        "Avg Word Length", 
        "Top Words"
    ]
    
    data = [
        results['chars_total'],
        results['chars_no_spaces'],
        results['words'],
        results['lines'],
        results['avg_len'],
        common_words_str
    ]

    try:
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(headers)
            writer.writerow(data)
        print(f"\n[SUCCESS] Results saved to: {filename}")
    except Exception as e:
        print(f"\n[ERROR] Could not save to file: {e}")

def main():
    print("--- CLI Text Analyzer (v2.1) ---")
    print("1. Enter text manually")
    print("2. Load from .txt file")
    
    choice = input("\nSelect an option (1/2): ")
    
    text = ""
    
    if choice == '1':
        print("Enter/Paste your text (Press Enter, then Ctrl+D (Mac/Linux) or Ctrl+Z (Win) to finish):")
        import sys
        text = sys.stdin.read()
    elif choice == '2':
        filename = input("Enter the filename (e.g., data.txt): ")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print("[ERROR] File not found.")
            return
    else:
        print("[ERROR] Invalid choice.")
        return

    results = analyze_text(text)
    
    if results:
        print("\n" + "="*35)
        print("ANALYSIS RESULTS:")
        print("="*35)
        print(f"Total characters:       {results['chars_total']}")
        print(f"Characters (no spaces): {results['chars_no_spaces']}")
        print(f"Word count:             {results['words']}")
        print(f"Line count:             {results['lines']}")
        print(f"Avg word length:        {results['avg_len']} chars")
        print("\nMost frequent words:")
        for word, count in results['most_common']:
            print(f" - {word}: {count} times")
        print("="*35)

        save_choice = input("\nExport results to CSV? (y/n): ").lower()
        if save_choice == 'y':
            csv_name = input("Enter output filename (default: report.csv): ") or "report.csv"
            if not csv_name.endswith('.csv'):
                csv_name += '.csv'
            save_to_csv(results, csv_name)
    else:
        print("[WARNING] The text is empty.")

if __name__ == "__main__":
    main()