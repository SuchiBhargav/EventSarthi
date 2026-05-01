"""
Webhook Routes
Handles WhatsApp webhook callbacks
"""

from fastapi import APIRouter, Request, Query, Depends
from typing import Optional

from app.dependencies import get_whatsapp_signature, verify_whatsapp_webhook

router = APIRouter()


@router.get("/whatsapp")
async def verify_webhook(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge"),
):
    """
    Verify WhatsApp webhook subscription
    """
    return verify_whatsapp_webhook(hub_mode, hub_verify_token, hub_challenge)


@router.post("/whatsapp")
async def receive_webhook(
    request: Request, signature: Optional[str] = Depends(get_whatsapp_signature)
):
    """
    Receive WhatsApp webhook messages
    """
    try:
        # Get webhook payload
        body = await request.json()

        # Log webhook for debugging (in production, process messages)
        print(f"WhatsApp webhook received: {body}")

        # In production, you would:
        # 1. Verify webhook signature
        # 2. Extract message data
        # 3. Process message with AI
        # 4. Store conversation
        # 5. Send response via WhatsApp API

        # For now, just acknowledge receipt
        return {"status": "received", "message": "Webhook processed successfully"}

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}


# Made with Bob
