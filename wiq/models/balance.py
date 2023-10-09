# © copyright by VoX DoX
from pydantic import BaseModel


class Balance(BaseModel):
	"""
	Balance model Wiq
	"""
	balance: float
	currency: str
