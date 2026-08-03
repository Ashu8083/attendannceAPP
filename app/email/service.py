from fastapi_mail import FastMail, MessageSchema, MessageType

from app.email.email_config import conf
from app.core.logging_config import logger

class EmailService:

    async def send_otp(self, email: str, otp: str):

        logger.info(f"trying otp sent On the user's email {email}" )

        message = MessageSchema(
            subject="OTP Verification",
            recipients=[email],
            template_body={
                "otp": otp
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        try:
            await fm.send_message(
            message,
            template_name="otp.html",
            )
            logger.info("OTP sent On the user's email ")
        except Exception as e:
            logger.error(f"we get error while sending mail to {email} | {e}")


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

    async def send_welcome_email(self,email:str):
        message = MessageSchema(
            subject="Welcome Test Email",
            recipients=[email],
            template_body={
                "name": "welcome mail",
            },
           subtype=MessageType.html,
        )
        fm = FastMail(conf)
        await fm.send_message(
            message,
            template_name="welcome.html",
        )
email_service = EmailService()
# all done