#!/usr/bin/env python3
"""
Simple demo to show prompt modification on the fly.
Run this to demonstrate how easy it is to change the AI prompt.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.summarizer import Summarizer


def show_current_prompt():
    """Show the current prompt being used."""
    print("=" * 80)
    print("🎯 CURRENT AI PROMPT (from src/core/summarizer.py)")
    print("=" * 80)
    
    # Read and display the current prompt from the file
    with open("src/core/summarizer.py", "r") as f:
        content = f.read()
    
    # Find the prompt section
    start_marker = "# ============================================================================"
    end_marker = "# ============================================================================"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        # Find the second occurrence of the end marker to get the full prompt section
        second_end_idx = content.find(end_marker, end_idx + len(end_marker))
        if second_end_idx != -1:
            prompt_section = content[start_idx:second_end_idx + len(end_marker)]
            print(prompt_section)
        else:
            print("Could not find end of prompt section.")
    else:
        print("Could not find prompt section in the file.")


def show_how_to_modify():
    """Show how to modify the prompt."""
    print("\n" + "=" * 80)
    print("📝 HOW TO MODIFY THE PROMPT ON THE FLY")
    print("=" * 80)
    
    print("\n1. Open the file: src/core/summarizer.py")
    print("2. Look for the section marked with: 🎯 MAIN PROMPT")
    print("3. Modify the text inside the triple quotes")
    print("4. Save the file")
    print("5. Run: python main.py")
    
    print("\nExample modifications you can make:")
    print("- Change '2-3 sentences' to '1 sentence' for shorter summaries")
    print("- Add 'Focus on security risks' to emphasize security")
    print("- Change 'Xponance team' to 'compliance team'")
    print("- Add 'Include cost implications' to focus on financial aspects")


def demo_sample_modifications():
    """Show sample prompt modifications."""
    print("\n" + "=" * 80)
    print("💡 SAMPLE PROMPT MODIFICATIONS")
    print("=" * 80)
    
    print("\nMODIFICATION 1: Executive Summary Style")
    print("-" * 50)
    print("Change the prompt to:")
    print("""Please provide a concise executive summary (1 sentence) that:
1. Identifies the document type and business impact
2. Highlights the most critical risk or finding
3. Indicates urgency level (High/Medium/Low)""")
    
    print("\nMODIFICATION 2: Risk-Focused Analysis")
    print("-" * 50)
    print("Add this to the prompt:")
    print("""Focus particularly on:
- Risk quantification (High/Medium/Low)
- Compliance gaps and missing requirements
- Specific mitigation recommendations""")
    
    print("\nMODIFICATION 3: Technical Deep Dive")
    print("-" * 50)
    print("Change the prompt to:")
    print("""Please provide a technical analysis (3-4 sentences) that:
1. Identifies technical architecture and security controls
2. Highlights infrastructure details and dependencies
3. Notes any technical risks or integration requirements
4. Provides technical recommendations""")
    
    print("\nMODIFICATION 4: Compliance-Focused")
    print("-" * 50)
    print("Change the prompt to:")
    print("""Please provide a compliance assessment (2-3 sentences) that:
1. Identifies regulatory framework and requirements
2. Highlights compliance gaps and audit findings
3. Notes regulatory reporting requirements
4. Provides compliance risk mitigation steps""")


def main():
    """Run the demo."""
    print("VENDOR DUE DILIGENCE - PROMPT MODIFICATION DEMO")
    print("This shows how easy it is to modify the AI prompt on the fly")
    
    show_current_prompt()
    show_how_to_modify()
    demo_sample_modifications()
    
    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETE")
    print("=" * 80)
    print("\nKey points for your boss:")
    print("✓ The prompt is clearly marked with 🎯 in the code")
    print("✓ It's just a big text block that's easy to find and modify")
    print("✓ Changes take effect immediately when you save and run")
    print("✓ No complex configuration - just edit the text directly")
    print("✓ The prompt is human-readable and self-documenting")


if __name__ == "__main__":
    main() 