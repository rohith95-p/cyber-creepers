import logging
import json
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineNo": record.lineno
        }
        if hasattr(record, "client_id"):
            log_record["client_id"] = record.client_id
        if hasattr(record, "action"):
            log_record["action"] = record.action
            
        return json.dumps(log_record)

def setup_logger(name="ivy_wealth", log_file="logs/ivy.log", level=logging.INFO):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        # File Handler (Daily Rotation)
        file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=30)
        file_handler.setFormatter(JSONFormatter())
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

audit_logger = setup_logger("ivy_audit", "logs/audit.log")

def log_audit_action(client_id, action, details):
    """Audit trail for compliance."""
    audit_logger.info(details, extra={"client_id": client_id, "action": action})
