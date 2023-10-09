# © copyright by VoX DoX
from pydantic import BaseModel


class Order(BaseModel):
	id: int


class Cancel(BaseModel):
	"""
	Cancel order model Wiq
	"""
	id: int
	status: str


class Refill(BaseModel):
	"""
	Refill order model Wiq
	"""
	status: str


class Status(BaseModel):
	"""
	Get status order model Wiq
	"""
	status: str
	link: str
	quantity: int
	start_count: int
	remains: int
	charge: int

