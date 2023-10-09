# © copyright by VoX DoX
from typing import Union
from pydantic import BaseModel


class Service(BaseModel):
	ID: Union[int, str]
	service: int
	category: int
	name: str
	cost: float
	rate: float
	min: int
	max: int
	refill: bool
	cancel: bool
	type: str
	dripfeed: bool
