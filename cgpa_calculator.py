#!/usr/bin/env python3
"""
CGPA Calculator
===============
A beginner-friendly command-line tool that calculates SGPA (Semester Grade
Point Average) and CGPA (Cumulative Grade Point Average) for students.

Supports two grading scales:
  • 10-point scale (common in Indian universities)
  • 4-point scale  (common in US / international universities)

Features:
  - Per-semester SGPA and overall CGPA calculation
  - Input validation with friendly re-prompts
  - Neat summary table using only the standard library
  - Optional CSV export of results
  - "What CGPA do I need next semester?" target calculator
"""

import csv
import os
import sys
import unittest

# Ensure Unicode output works on Windows (piped or not)
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ─────────────────────────────────────────────
# Grade-point mapping tables
# ─────────────────────────────────────────────

# 10-point scale (Indian university convention)
GRADE_MAP_10 = {
    "O":  10.0,
    "A+": 9.0,
    "A":  8.0,
    "B+": 7.0,
    "B":  6.0,
    "C":  5.0,
    "P":  4.0,   # Pass
    "F":  0.0,   # Fail
}

# 4-point scale (US convention)
GRADE_MAP_4 = {
    "A+": 4.0,
    "A":  4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B":  3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C":  2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D":  1.0,
    "F":  0.0,
}


# ─────────────────────────────────────────────
# Input helpers (all validate and re-prompt)
# ─────────────────────────────────────────────

def get_positive_int(prompt: str) -> int:
    """Keep asking until the user enters a positive integer (≥ 1)."""
    while True:
        try:
            value = int(input(prompt))
            if value < 1:
                print("  ✗ Please enter a number ≥ 1.")
                continue
            return value
        except ValueError:
            print("  ✗ Invalid input — enter a whole number.")


def get_positive_float(prompt: str) -> float:
    """Keep asking until the user enters a positive number (> 0)."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  ✗ Credit hours must be greater than 0.")
                continue
            return value
        except ValueError:
            print("  ✗ Invalid input — enter a number.")


def get_grade_point(prompt: str, grade_map: dict, scale_max: float) -> float:
    """
    Accept either a letter grade (looked up in *grade_map*) or a raw
    numeric grade point (must be between 0 and *scale_max*).

    Returns the numeric grade-point value.
    """
    valid_letters = ", ".join(grade_map.keys())
    while True:
        raw = input(prompt).strip().upper()

        # Try letter grade first
        if raw in grade_map:
            return grade_map[raw]

        # Try numeric grade point
        try:
            gp = float(raw)
            if 0 <= gp <= scale_max:
                return gp
            print(f"  ✗ Numeric grade must be between 0 and {scale_max}.")
        except ValueError:
            print(f"  ✗ Invalid grade. Enter a letter ({valid_letters})")
            print(f"    or a number between 0 and {scale_max}.")


def choose_scale() -> tuple:
    """
    Let the user pick 10-point or 4-point grading scale.

    Returns:
        (grade_map, scale_max, scale_label)
    """
    while True:
        print("\nSelect grading scale:")
        print("  [1] 10-point (Indian universities)")
        print("  [2]  4-point (US / international)")
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            return GRADE_MAP_10, 10.0, "10-point"
        elif choice == "2":
            return GRADE_MAP_4, 4.0, "4-point"
        else:
            print("  ✗ Please enter 1 or 2.")


# ─────────────────────────────────────────────
# Core calculation functions
# ─────────────────────────────────────────────

def calculate_sgpa(subjects: list[dict]) -> float:
    """
    Calculate the Semester Grade Point Average.

    Args:
        subjects: list of dicts, each with keys 'credits' and 'grade_point'.

    Returns:
        SGPA (weighted average), or 0.0 if total credits are zero.
    """
    total_credits = sum(s["credits"] for s in subjects)
    if total_credits == 0:
        return 0.0
    weighted_sum = sum(s["credits"] * s["grade_point"] for s in subjects)
    return weighted_sum / total_credits


def calculate_cgpa(semesters: list[dict]) -> tuple:
    """
    Calculate the Cumulative GPA across all semesters.

    Args:
        semesters: list of dicts with keys 'subjects' (list) and 'sgpa'.

    Returns:
        (cgpa, total_credits_earned)
    """
    total_credits = 0
    weighted_sum = 0.0
    for sem in semesters:
        for subj in sem["subjects"]:
            total_credits += subj["credits"]
            weighted_sum += subj["credits"] * subj["grade_point"]
    cgpa = weighted_sum / total_credits if total_credits else 0.0
    return cgpa, total_credits


# ─────────────────────────────────────────────
# Data collection
# ─────────────────────────────────────────────

def collect_semester_data(sem_num: int, grade_map: dict,
                          scale_max: float) -> dict:
    """
    Interactively collect subject data for one semester.

    Returns:
        dict with keys 'semester', 'subjects', 'sgpa'.
    """
    print(f"\n{'─'*40}")
    print(f"  Semester {sem_num}")
    print(f"{'─'*40}")
    num_subjects = get_positive_int("  Number of subjects: ")
    subjects = []
    for j in range(1, num_subjects + 1):
        print(f"\n  --- Subject {j} ---")
        name = input("    Subject name : ").strip() or f"Subject {j}"
        credits = get_positive_float("    Credit hours : ")
        gp = get_grade_point("    Grade        : ", grade_map, scale_max)
        subjects.append({
            "name": name,
            "credits": credits,
            "grade_point": gp,
        })

    sgpa = calculate_sgpa(subjects)
    print(f"\n  ➤ Semester {sem_num} SGPA = {sgpa:.2f}")
    return {"semester": sem_num, "subjects": subjects, "sgpa": sgpa}


# ─────────────────────────────────────────────
# Display helpers
# ─────────────────────────────────────────────

def print_summary(semesters: list[dict], cgpa: float,
                  total_credits: float, scale_label: str,
                  scale_max: float) -> str:
    """
    Print a formatted summary table and return it as a string
    (so it can also be written to a file).
    """
    col_w = [4, 24, 8, 8]  # Sem#, Name, Credits, GP
    hdr = (f"{'Sem':<{col_w[0]}}  {'Subject':<{col_w[1]}}  "
           f"{'Credits':>{col_w[2]}}  {'Grade Pt':>{col_w[3]}}")
    sep = "─" * (sum(col_w) + 10)

    lines = []
    lines.append("")
    lines.append("=" * len(sep))
    lines.append(f"  CGPA REPORT  ({scale_label} scale)")
    lines.append("=" * len(sep))
    lines.append(hdr)
    lines.append(sep)

    for sem in semesters:
        for subj in sem["subjects"]:
            name = subj["name"][:col_w[1]]  # truncate long names
            line = (f"{sem['semester']:<{col_w[0]}}  {name:<{col_w[1]}}  "
                    f"{subj['credits']:>{col_w[2]}.1f}  "
                    f"{subj['grade_point']:>{col_w[3]}.2f}")
            lines.append(line)
        lines.append(f"{'':>{col_w[0]}}  {'SGPA ──▶':>{col_w[1]}}  "
                      f"{'':>{col_w[2]}}  {sem['sgpa']:>{col_w[3]}.2f}")
        lines.append(sep)

    lines.append(f"\n  Total credits earned : {total_credits:.1f}")
    lines.append(f"  Overall CGPA         : {cgpa:.2f} / {scale_max:.0f}")

    # Approximate percentage (common formula for 10-point scale)
    if scale_max == 10.0:
        pct = cgpa * 9.5
        lines.append(f"  Approx. percentage   : {pct:.1f}%  (CGPA × 9.5)")
    else:
        # A rough 4-point → percentage mapping (25 × GPA)
        pct = (cgpa / 4.0) * 100
        lines.append(f"  Approx. percentage   : {pct:.1f}%  (GPA/4 × 100)")

    lines.append("")

    report = "\n".join(lines)
    print(report)
    return report


# ─────────────────────────────────────────────
# Optional features
# ─────────────────────────────────────────────

def save_to_csv(semesters: list[dict], cgpa: float,
                total_credits: float, filepath: str) -> None:
    """Save the results to a CSV file."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Semester", "Subject", "Credits", "Grade Point"])
        for sem in semesters:
            for subj in sem["subjects"]:
                writer.writerow([sem["semester"], subj["name"],
                                 subj["credits"], subj["grade_point"]])
            writer.writerow([f"Sem {sem['semester']} SGPA", "", "",
                             f"{sem['sgpa']:.2f}"])
        writer.writerow([])
        writer.writerow(["Overall CGPA", "", "", f"{cgpa:.2f}"])
        writer.writerow(["Total Credits", "", "", f"{total_credits:.1f}"])
    print(f"\n  ✓ Results saved to {filepath}")


def target_cgpa_calculator(current_cgpa: float, total_credits: float,
                           scale_max: float) -> None:
    """
    Tell the user what SGPA they need next semester to reach a target CGPA.

    Formula:
        target_cgpa = (current_cgpa × total_credits + needed_sgpa × next_credits)
                      / (total_credits + next_credits)

    Solving for needed_sgpa:
        needed_sgpa = (target_cgpa × (total_credits + next_credits)
                       - current_cgpa × total_credits) / next_credits
    """
    print("\n── Target CGPA Calculator ──")
    while True:
        try:
            target = float(input(f"  Enter your target CGPA (0–{scale_max:.0f}): "))
            if not (0 <= target <= scale_max):
                print(f"  ✗ Must be between 0 and {scale_max:.0f}.")
                continue
            break
        except ValueError:
            print("  ✗ Enter a valid number.")

    while True:
        try:
            next_credits = float(input("  Expected credits next semester: "))
            if next_credits <= 0:
                print("  ✗ Must be > 0.")
                continue
            break
        except ValueError:
            print("  ✗ Enter a valid number.")

    needed = ((target * (total_credits + next_credits)
               - current_cgpa * total_credits) / next_credits)

    if needed > scale_max:
        print(f"\n  ⚠ You would need an SGPA of {needed:.2f}, which exceeds "
              f"the maximum ({scale_max:.0f}).")
        print("  This target is not achievable in one semester.")
    elif needed < 0:
        print(f"\n  ✓ You already exceed your target! Any SGPA ≥ 0 will do.")
    else:
        print(f"\n  ➤ You need an SGPA of at least {needed:.2f} next semester "
              f"to reach a CGPA of {target:.2f}.")


# ─────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────

def main() -> None:
    """Run the interactive CGPA calculator loop."""
    print("╔══════════════════════════════════════╗")
    print("║        📊  CGPA CALCULATOR  📊       ║")
    print("╚══════════════════════════════════════╝")

    while True:  # ---- outer "calculate again?" loop ----
        grade_map, scale_max, scale_label = choose_scale()
        num_semesters = get_positive_int("\nHow many semesters? ")

        semesters = []
        for i in range(1, num_semesters + 1):
            sem_data = collect_semester_data(i, grade_map, scale_max)
            semesters.append(sem_data)

        cgpa, total_credits = calculate_cgpa(semesters)
        report = print_summary(semesters, cgpa, total_credits,
                               scale_label, scale_max)

        # ── Optional: save to CSV ──
        save_choice = input("Save results to CSV? (y/n): ").strip().lower()
        if save_choice == "y":
            default_path = "cgpa_report.csv"
            path = input(f"  File path [{default_path}]: ").strip() or default_path
            save_to_csv(semesters, cgpa, total_credits, path)

        # ── Optional: target CGPA feature ──
        target_choice = input("Calculate target CGPA for next semester? "
                              "(y/n): ").strip().lower()
        if target_choice == "y":
            target_cgpa_calculator(cgpa, total_credits, scale_max)

        # ── Again or exit? ──
        again = input("\nCalculate again? (y/n): ").strip().lower()
        if again != "y":
            print("\nGoodbye! 👋")
            break


# ─────────────────────────────────────────────
# Unit tests
# ─────────────────────────────────────────────

class TestCGPACalculations(unittest.TestCase):
    """Verify SGPA and CGPA calculations with known data."""

    def test_sgpa_basic(self):
        """SGPA of three subjects with equal credits."""
        subjects = [
            {"name": "Math",    "credits": 3, "grade_point": 9.0},
            {"name": "Physics", "credits": 3, "grade_point": 8.0},
            {"name": "Chem",    "credits": 3, "grade_point": 7.0},
        ]
        # (3×9 + 3×8 + 3×7) / 9 = 72/9 = 8.0
        self.assertAlmostEqual(calculate_sgpa(subjects), 8.0)

    def test_sgpa_weighted(self):
        """SGPA with unequal credit weights."""
        subjects = [
            {"name": "DSA",  "credits": 4, "grade_point": 10.0},
            {"name": "DBMS", "credits": 3, "grade_point": 8.0},
            {"name": "OS",   "credits": 2, "grade_point": 6.0},
        ]
        # (4×10 + 3×8 + 2×6) / 9 = (40+24+12)/9 ≈ 8.4444
        self.assertAlmostEqual(calculate_sgpa(subjects), 76 / 9)

    def test_sgpa_all_fail(self):
        """All F grades → SGPA should be 0."""
        subjects = [
            {"name": "X", "credits": 3, "grade_point": 0.0},
            {"name": "Y", "credits": 4, "grade_point": 0.0},
        ]
        self.assertAlmostEqual(calculate_sgpa(subjects), 0.0)

    def test_sgpa_single_subject(self):
        """Single subject: SGPA equals its grade point."""
        subjects = [{"name": "Eng", "credits": 2, "grade_point": 7.5}]
        self.assertAlmostEqual(calculate_sgpa(subjects), 7.5)

    def test_cgpa_two_semesters(self):
        """CGPA across two semesters with different credits."""
        sem1_subjects = [
            {"name": "A", "credits": 3, "grade_point": 9.0},
            {"name": "B", "credits": 3, "grade_point": 7.0},
        ]
        sem2_subjects = [
            {"name": "C", "credits": 4, "grade_point": 8.0},
            {"name": "D", "credits": 2, "grade_point": 10.0},
        ]
        semesters = [
            {"semester": 1, "subjects": sem1_subjects,
             "sgpa": calculate_sgpa(sem1_subjects)},
            {"semester": 2, "subjects": sem2_subjects,
             "sgpa": calculate_sgpa(sem2_subjects)},
        ]
        # Total: (3×9 + 3×7 + 4×8 + 2×10) / (3+3+4+2)
        #      = (27 + 21 + 32 + 20) / 12 = 100/12 ≈ 8.3333
        cgpa, total_credits = calculate_cgpa(semesters)
        self.assertAlmostEqual(cgpa, 100 / 12)
        self.assertEqual(total_credits, 12)

    def test_cgpa_four_point_scale(self):
        """Verify CGPA works with 4-point scale values too."""
        subjects = [
            {"name": "Bio", "credits": 3, "grade_point": 4.0},
            {"name": "Art", "credits": 3, "grade_point": 3.0},
        ]
        semesters = [{"semester": 1, "subjects": subjects,
                      "sgpa": calculate_sgpa(subjects)}]
        cgpa, total = calculate_cgpa(semesters)
        # (3×4 + 3×3) / 6 = 21/6 = 3.5
        self.assertAlmostEqual(cgpa, 3.5)
        self.assertEqual(total, 6)

    def test_empty_subjects(self):
        """Edge case: no subjects should give 0 SGPA."""
        self.assertAlmostEqual(calculate_sgpa([]), 0.0)


# ─────────────────────────────────────────────
# Script entry
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # If called with --test, run unit tests instead of the interactive app.
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Remove the flag so unittest doesn't get confused
        sys.argv.pop(1)
        unittest.main()
    else:
        main()
