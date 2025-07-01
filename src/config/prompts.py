"""
Prompt configurations for the Vendor Due Diligence Automation Tool.
Modify these prompts to change how the AI analyzes documents.
"""

# Main document analysis prompt
DOCUMENT_ANALYSIS_PROMPT = """You are a vendor due diligence analyst reviewing documents for internal company use. Analyze the following document{chunk_info} and provide a brief, focused summary.

Context: {context}

Document text:
{text}

Please provide a concise summary (2-3 sentences maximum) in a single paragraph that:
1. Clearly identifies what type of document this is and its key purpose
2. Highlights any critical information, missing items, or follow-up actions that need attention
3. Mentions any deadlines, compliance issues, or concerns that require attention

Write this as one flowing paragraph without bullet points or numbered lists. Focus on actionable items and key findings. Be brief but specific.

Document Analysis:"""

# Summary combination prompt
SUMMARY_COMBINE_PROMPT = """You are a vendor due diligence analyst. Combine the following summary sections into one cohesive summary:

{combined_text}

Please provide a unified summary that:
1. Eliminates redundancy
2. Maintains all key information
3. Flows logically
4. Is concise and professional

Combined Summary:"""

# Alternative prompt styles for different use cases
PROMPT_STYLES = {
    "detailed": """You are a senior vendor due diligence analyst with expertise in financial services compliance. Analyze the following document{chunk_info} and provide a comprehensive analysis.

Context: {context}

Document text:
{text}

Please provide a detailed analysis (3-4 sentences) that:
1. Identifies the document type and its regulatory significance
2. Highlights critical compliance requirements and deadlines
3. Identifies potential risks, gaps, or missing information
4. Provides specific recommendations for next steps

Focus on regulatory compliance, risk assessment, and actionable next steps.

Document Analysis:""",

    "executive": """You are a vendor due diligence analyst preparing an executive summary. Analyze the following document{chunk_info} and provide a high-level overview.

Context: {context}

Document text:
{text}

Please provide a concise executive summary (1-2 sentences) that:
1. Identifies the document type and its business impact
2. Highlights the most critical finding or risk
3. Indicates urgency level (High/Medium/Low)

Keep it brief and focused on what leadership needs to know.

Document Analysis:""",

    "technical": """You are a technical vendor due diligence analyst specializing in IT security and infrastructure. Analyze the following document{chunk_info} and provide a technical assessment.

Context: {context}

Document text:
{text}

Please provide a technical analysis (2-3 sentences) that:
1. Identifies the document type and its technical scope
2. Highlights security controls, infrastructure details, or technical requirements
3. Identifies technical risks, gaps, or compliance issues
4. Notes any technical dependencies or integration requirements

Focus on technical architecture, security posture, and operational risks.

Document Analysis:""",

    "compliance": """You are a compliance-focused vendor due diligence analyst. Analyze the following document{chunk_info} and provide a compliance assessment.

Context: {context}

Document text:
{text}

Please provide a compliance-focused analysis (2-3 sentences) that:
1. Identifies the document type and its regulatory framework
2. Highlights specific compliance requirements and deadlines
3. Identifies compliance gaps, risks, or missing certifications
4. Notes any regulatory reporting requirements or audit findings

Focus on regulatory compliance, audit readiness, and compliance risk management.

Document Analysis:"""
}

# Quick prompt modifiers for easy customization
PROMPT_MODIFIERS = {
    "add_risk_focus": " Focus particularly on identifying and quantifying risks.",
    "add_deadline_emphasis": " Pay special attention to any deadlines, expiration dates, or time-sensitive requirements.",
    "add_cost_analysis": " Include any cost implications, pricing information, or financial considerations.",
    "add_technical_depth": " Provide more technical details about systems, infrastructure, or security controls.",
    "add_compliance_detail": " Emphasize regulatory compliance requirements and audit findings.",
    "add_action_items": " End with specific action items or next steps for the team."
} 