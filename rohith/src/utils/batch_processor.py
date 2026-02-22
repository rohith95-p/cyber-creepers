import logging
from concurrent.futures import ThreadPoolExecutor
from src.orchestration.supervisor_graph import app
import time

logger = logging.getLogger(__name__)

def process_client_batch(client_ids: list, max_workers: int = 4):
    """
    Optimization 3: Batch Processing.
    Processes multiple clients efficiently using a ThreadPool.
    """
    logger.info(f"Starting batch process for {len(client_ids)} clients.")
    results = {}
    
    def run_single(client_id):
        try:
            initial_state = {
                "client_id": client_id,
                "portfolio_assets": [],
                "market_data": {},
                "risk_metrics": {},
                "final_report": "",
                "compliance_status": "Processing..."
            }
            logger.info(f"Processing client: {client_id}")
            final_state = app.invoke(initial_state)
            return {"status": "success", "report_length": len(final_state.get("final_report", ""))}
        except Exception as e:
            logger.error(f"Failed processing {client_id}: {e}")
            return {"status": "error", "message": str(e)}

    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_client = {executor.submit(run_single, cid): cid for cid in client_ids}
        for future in future_to_client:
            cid = future_to_client[future]
            try:
                data = future.result()
                results[cid] = data
            except Exception as exc:
                results[cid] = {"status": "error", "message": str(exc)}
                
    elapsed = time.time() - start_time
    logger.info(f"Batch completed in {elapsed:.2f} seconds.")
    
    return results
