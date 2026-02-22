import re

def redact_pii(text: str) -> str:
    """
    Redacts Personally Identifiable Information (PII) like emails, phone numbers, and SSNs.
    """
    if not text:
        return text
        
    # Redact Emails
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    redacted = re.sub(email_pattern, '[REDACTED_EMAIL]', text)
    
    # Redact Phone numbers (basic format)
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    redacted = re.sub(phone_pattern, '[REDACTED_PHONE]', redacted)
    
    # Redact SSN
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    redacted = re.sub(ssn_pattern, '[REDACTED_SSN]', redacted)
    
    return redacted

def audit_node_wrapper(node_func):
    """Middleware decorator for tracking graph node execution."""
    def wrapper(state):
        client_id = state.get("client_id", "Unknown")
        node_name = node_func.__name__
        from .logging import log_audit_action
        
        log_audit_action(client_id, f"STARTED_{node_name.upper()}", f"Node '{node_name}' execution started.")
        
        try:
            result = node_func(state)
            log_audit_action(client_id, f"COMPLETED_{node_name.upper()}", f"Node '{node_name}' executed successfully.")
            return result
        except Exception as e:
            log_audit_action(client_id, f"FAILED_{node_name.upper()}", f"Node '{node_name}' failed: {str(e)}")
            raise e
            
    return wrapper
