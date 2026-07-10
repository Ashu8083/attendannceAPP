
from app.email.service import EmailService
email_service = EmailService()

await email_service.send_otp(
    email="test@gmail.com",
    otp="123456",
    name="Ashutosh",
)