
# CertNode CLI Entry Point

import argparse
from main import run_certnode_pipeline

def main():
    parser = argparse.ArgumentParser(description="CertNode Logic Validation CLI")
    parser.add_argument("input_file", help="Path to input text file for validation")
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        input_text = f.read()

    result = run_certnode_pipeline(input_text)
    print("\n[Certification Result]\n")
    print(f"Logic Tier: {result['tier']}")
    print(f"ICS Hash: {result['hash']}")
    print(f"Certified Output:\n{result['certified_output']}")
    print(f"Reflexive Analysis: {result['reflex']}")
    print(f"Audit Trail: {result['audit']}")

if __name__ == "__main__":
    main()
