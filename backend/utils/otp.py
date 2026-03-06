# import pyotp
# from datetime import datetime, timedelta
# from pydantic import EmailStr
# from config.redis import redis_client


# class OTPManager:
#     @staticmethod
#     def generate_otp() -> str:
#         """
#         Generate a secure 6-digit OTP using pyotp
#         """
#         secret = pyotp.random_base32()
#         totp = pyotp.TOTP(secret, digits=6)
#         return totp.now()

#     @staticmethod
#     def store_otp(email: EmailStr, otp: str, expiry_minutes: int = 5) -> None:
#         """
#         Store OTP in Redis with expiration
#         """
#         redis_client.setex(
#             f"otp:{email}",
#             timedelta(minutes=expiry_minutes),
#             otp
#         )

#     @staticmethod
#     def verify_otp(email: EmailStr, otp: str) -> bool:
#         """
#         Verify OTP from Redis
#         """
#         stored_otp = redis_client.get(f"otp:{email}")
#         if stored_otp and stored_otp == otp:
#             redis_client.delete(f"otp:{email}")  # Delete OTP after successful verification
#             return True
#         return False

#     @staticmethod
#     def get_html_template(otp: str) -> str:
#         """
#         Return a professionally styled HTML template for the OTP email
#         """
#         return f"""
#         <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
#             <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
#                 <h2 style="color: #333; margin-bottom: 20px;">Verification Code</h2>
#                 <p style="color: #666; margin-bottom: 30px;">Please use the following code to verify your account. This code will expire in 5 minutes.</p>
#                 <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 30px;">
#                     <h1 style="color: #007bff; font-size: 32px; margin: 0; letter-spacing: 5px;">{otp}</h1>
#                 </div>
#                 <p style="color: #999; font-size: 12px;">If you didn't request this code, please ignore this email.</p>
#             </div>
#         </div>
#         """