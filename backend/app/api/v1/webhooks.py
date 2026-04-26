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
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge")
):
    """
    Verify WhatsApp webhook subscription
    """
    return verify_whatsapp_webhook(hub_mode, hub_verify_token, hub_challenge)


@router.post("/whatsapp")
async def receive_webhook(
    request: Request,
    signature: Optional[str] = Depends(get_whatsapp_signature)
):
    """
    Receive WhatsApp webhook messages
    """
    # TODO: Implement webhook message processing
    return {"message": "Webhook received - to be implemented"}

# Made with Bob
