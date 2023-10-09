import ssl
import certifi
import asyncio
from aiohttp import ClientSession
from typing import Optional, Dict, List

from .models import (
	Balance,
	Refill,
	Order,
	Cancel,
	Service,
	Status
)
from . import WiqAPIError


class WiqAPI:
	"""
	Wiq API class
	Асинхронный класс для работы с Wiq.ru API
	Подробнее об API: https://wiq.ru/api-documentation.php
	:param api_key: ключ авторизации. Нужен для работы с API
	:type api_key: str
	:param url: актуальная ссылка к WIQ API
	:type url: Optional[str]
	"""
	def __init__(
			self,
			api_key: str,
			url: Optional[str] = "https://wiq.ru/api/"
	) -> None:
		self._API_KEY_: str = api_key
		self._BASE_URL_: str = url

		self._SSL_CONTEXT_ = ssl.create_default_context(cafile=certifi.where())
		self.session: ClientSession = ClientSession()

	async def getBalance(
			self
	) -> Balance:
		"""
		Get balance account wiq
		:return: Balance
		"""
		params: dict = {
			"key": self._API_KEY_,
			"action": "balance"
		}
		response = await self._request(
			params=params
		)
		return Balance(**response)

	async def createOrder(
			self,
			order: int,
			quantity: int,
			link: Optional[str],
			posts: int = None
	) -> Order:
		"""
		Create order from api
		:param order: int
		:param quantity: int
		:param link: str
		:param posts: int (Not None auto like and auto views
		:return: Order
		"""
		data = {
			"key": self._API_KEY_,
			"action": "create",
			"service": order,
			"quantity": quantity,
			"link": link,
		}
		if posts is not None:
			data['posts'] = posts

		response = await self._request(
			params=data
		)
		return Order(**response)

	async def getServices(
			self
	) -> List[Service]:
		"""
		Get all service from api
		:return: list Service
		"""
		data = {
			"key": self._API_KEY_,
			"action": "services"
		}
		response = await self._request(
			params=data
		)
		services = []
		for service in response:
			print(service)
			services.append(Service(**service))

		return services

	async def getStatus(
			self,
			order: int
	) -> Status:
		"""
		Get status order
		:param order: int
		:return: Status
		"""
		data = {
			"key": self._API_KEY_,
			"action": "status",
			"order": order
		}
		response = await self._request(
			params=data
		)
		return Status(**response)

	async def getCancel(
			self,
			order: int
	) -> Cancel:
		"""
		Cancel order, return status
		:param order: int
		:return: Cancel
		"""
		data = {
			"key": self._API_KEY_,
			"action": "cancel",
			"order": order
		}
		response = await self._request(
			params=data
		)

		return Cancel(**response)

	async def getRefill(
			self,
			order,
	) -> Refill:
		"""
		restoring unsubscriptions, return status
		:param order:
		:return: Refill.status
		"""
		data = {
			"key": self._API_KEY_,
			"action": "refill",
			"order": order
		}
		response = await self._request(
			params=data
		)

		return Refill(**response)

	async def _request(
			self,
			params: dict,
	) -> Dict:
		"""
		Создание запроса к API
		:param params: параметры запрсоа
		:type params: dict
		:return: Dict
		"""
		request = await self.session.post(
			url=self._BASE_URL_,
			ssl_context=self._SSL_CONTEXT_,
			data=params,
		)
		print(request.status)
		print(await request.text())

		answer: dict = await request.json(content_type="text/html")
		if not type(answer) is list and answer.get("Error"):
			raise WiqAPIError(
				answer['Error']
			)

		return answer

	def get_session(self) -> ClientSession:
		return self.session

	def __del__(self) -> None:
		if not self.session.closed:
			loop = asyncio.get_event_loop()
			loop.create_task(self.session.close())
