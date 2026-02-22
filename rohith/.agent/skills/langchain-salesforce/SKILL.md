---
name: langchain-salesforce
description: Salesforce CRM integration via LangChain — all AI outputs land as Draft/Pending Review
---

# LangChain Salesforce CRM Skill

## Purpose
This skill provides **Salesforce CRM integration** via the LangChain Salesforce toolkit, enabling the wealth management pipeline to read client portfolios and write back AI-generated reports.

## Reference Codebase
The full langchain-salesforce source is located at `references/` and contains the LangChain toolkit, Salesforce API wrappers, and authentication utilities.

## Operations

### Read: Retrieve Client Portfolio
```python
# Fetch client record and portfolio assets by Client ID
client = salesforce_toolkit.query(
    "SELECT Id, Name, Portfolio_Assets__c FROM Account WHERE Id = :client_id"
)
```

### Write: Push Draft Report to CRM
```python
# Write the AI-generated report back to the CRM
salesforce_toolkit.update("Account", client_id, {
    "Wealth_Report__c": final_report_markdown,
    "Status": "Pending Review"    # ← MANDATORY — see compliance mandate below
})
```

---

> ⚠️ **FINRA/SEC COMPLIANCE MANDATE**
>
> **ALL AI-generated records written to Salesforce MUST include the field
> `Status: "Pending Review"`.** The AI has **NO authority** to:
> - Execute trades
> - Send client-facing emails
> - Set any record to `"Approved"` or `"Active"`
>
> Every output is a **draft** that requires human advisor review and explicit
> approval before any client action is taken. Violation of this mandate is a
> regulatory breach.

---

## Authentication
Salesforce credentials (`SF_USERNAME`, `SF_PASSWORD`, `SF_SECURITY_TOKEN`, `SF_DOMAIN`) must be defined in the project-root `.env` file.
