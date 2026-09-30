# 📊 CGPA Calculator

A beginner-friendly **CGPA (Cumulative Grade Point Average)** calculator with both a **command-line interface** (Python) and a **web-based interface** (HTML/CSS/JS).

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Web_UI-orange?logo=html5&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | CLI (`cgpa_calculator.py`) | Web (`index.html`) |
|---------|:-:|:-:|
| 10-point scale (Indian universities) | ✅ | ✅ |
| 4-point scale (US / International) | ✅ | ✅ |
| Letter grade & numeric grade input | ✅ | ✅ |
| Per-semester SGPA calculation | ✅ | ✅ |
| Overall CGPA (credit-weighted) | ✅ | ✅ |
| Approximate percentage conversion | ✅ | ✅ |
| Input validation & error handling | ✅ | ✅ |
| Summary table | ✅ | ✅ |
| Export results to CSV | ✅ | ❌ |
| 🎯 Target CGPA calculator | ✅ | ✅ |
| Unit tests (7 test cases) | ✅ | — |
| Beautiful dark-themed UI | — | ✅ |

---

## 🚀 Getting Started

### Option 1: Web Version (No Installation Needed)

1. Open `index.html` directly in your browser — **no server required!**
2. Or serve it locally:
   ```bash
   python -m http.server 8080
   ```
   Then visit → [http://localhost:8080](http://localhost:8080)

### Option 2: Command-Line Version

```bash
# Run the calculator
python cgpa_calculator.py

# Run unit tests
python cgpa_calculator.py --test -v
```

---

## 📖 How It Works

### Grading Scales

**10-Point Scale (Indian Universities)**

| Grade | O | A+ | A | B+ | B | C | P | F |
|-------|---|----|----|----|----|---|---|---|
| Points | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 0 |

**4-Point Scale (US / International)**

| Grade | A+/A | A- | B+ | B | B- | C+ | C | C- | D+ | D | F |
|-------|------|----|----|----|----|----|---|----|----|---|---|
| Points | 4.0 | 3.7 | 3.3 | 3.0 | 2.7 | 2.3 | 2.0 | 1.7 | 1.3 | 1.0 | 0 |

### Formulas

```
SGPA = Σ(Credit × Grade Point) / Σ(Credits)

CGPA = Σ(All Credits × Grade Points) / Σ(All Credits)

Approx. Percentage (10-pt) = CGPA × 9.5
```

---

## 🎯 Target CGPA Calculator

Already know your current CGPA? Use the built-in target calculator to find out:

> *"What SGPA do I need next semester to reach my target CGPA?"*

Available in both the CLI and web versions.

---

## 🧪 Unit Tests

The CLI version includes 7 test cases covering:

- Basic SGPA with equal credits
- Weighted SGPA with unequal credits
- All-fail (F grade) edge case
- Single subject SGPA
- Multi-semester CGPA
- 4-point scale CGPA
- Empty subjects edge case

Run tests:
```bash
python cgpa_calculator.py --test -v
```

---

## 📁 Project Structure

```
CGPA-Calculator-/
├── cgpa_calculator.py   # Command-line CGPA calculator (Python)
├── index.html           # Web-based CGPA calculator (HTML/CSS/JS)
├── cgpa_report.csv      # Sample CSV export output
└── README.md            # This file
```

---

## 🛠️ Tech Stack

- **Python 3** — CLI version (standard library only, no external packages)
- **HTML5 / CSS3 / JavaScript** — Web version (single self-contained file)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

<p align="center">Made with ❤️ by <a href="https://github.com/yashjai334-code">yashjai334-code</a></p>
