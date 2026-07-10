# app/email/router.py

from fastapi import APIRouter

from app.email.service import EmailService

router_email = APIRouter(prefix="/email", tags=["Email"])

email_service = EmailService()


@router_email.get("/test")
async def test_email():

    await email_service.send_test_email(
        "your_email@gmail.com"
    )

    return {"message": "Email sent successfully"}