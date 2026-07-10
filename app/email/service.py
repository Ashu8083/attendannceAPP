from fastapi_mail import FastMail, MessageSchema, MessageType

from app.email.email_config import conf


class EmailService:

    async def send_otp(self, email: str, otp: str):

        message = MessageSchema(
            subject="OTP Verification",
            recipients=[email],
            template_body={
                "otp": otp
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)

        await fm.send_message(
            message,
            template_name="otp.html",
        )

    async def send_test_email(self, recipient: str):
        message = MessageSchema(

            subject="FastAPI Mail Test",

            recipients=[recipient],

            template_body={

                "name": "Ashutosh",

                "otp": "123456",

            },

            subtype=MessageType.html,

        )

        fm = FastMail(conf)

        await fm.send_message(

            message,

            template_name="test.html",

        )
email_service = EmailService()