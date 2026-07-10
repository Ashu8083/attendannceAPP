# from fastapi_mail import FastMail, MessageSchema, MessageType
# class EmailService:
#
#     async def send_otp(self, email: str, otp: str, name: str):
#
#         message = MessageSchema(
#
#             subject="OTP Verification",
#
#             recipients=[email],
#
#             template_body={
#
#                 "otp": otp,
#
#                 "name": name,
#
#             },
#
#             subtype=MessageType.html,
#
#         )
#
#         fm = FastMail(conf)
#
#         await fm.send_message(
#
#             message,
#
#             template_name="otp.html",
#
#         )