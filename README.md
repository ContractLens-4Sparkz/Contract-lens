# 🔎 ContractLens

ContractLens is a hackathon-ready prototype for transparent contract oversight.

## What it does

- Preserves the original contract as a fixed baseline
- Tracks amendments and updates
- Calculates cumulative cost and timeline deviation
- Keeps structural changes visible
- Maintains a Rationale Register
- Connects changes to supporting evidence
- Separates documented reasons from unsupported claims
- Produces a transparent review-attention score

> ContractLens does not assume that every change is improper. It highlights changes where the available evidence may require further review.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Demo

The repository contains synthetic sample data for a Bengaluru urban road project. No real government or contractor records are included.

## Suggested hackathon demo flow

1. Show the original contract baseline.
2. Open the Changes tab.
3. Demonstrate how multiple amendments accumulate.
4. Show the Rationale Register.
5. Point out supported vs. unsupported evidence.
6. Return to Overview and explain the attention factors.

## Tech stack

- Python
- Streamlit
- Pandas
- JSON-based demo data

## Future scope

- PDF/DOCX extraction
- OCR for scanned contracts
- LLM-assisted clause extraction
- Firebase/PostgreSQL storage
- Role-based approval workflow
- Document versioning
- Automated evidence matching
- Audit trail and notifications
