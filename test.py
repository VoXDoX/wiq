import asyncio
from wiq import WiqAPI


async def start():
	wiq = WiqAPI(
		api_key="c75583c3ab54330ab1b95d9be08155cf"
	)
	# получаем актуальный баланс Wiq (в долларах)
	balance = await wiq.getBalance()
	print(balance.balance)
	print(balance.currency)  # валюта, она одна USD

	# создаем заказ накрутки, 502 - айди просмотров ютуба
	create = await wiq.createOrder(
		order=502,  # айди сервиса накрутки
		quantity=400,  # количество услуги
		link="ссылка на видео"  # ссылка на соц сеть, видео, пост
	)
	print(create.id)  # выведет ID заказа

	#  отменяем заказ, если есть возможность сервиса
	cancel = await wiq.getCancel(
		order=444948  # айди заказа для отмены
	)
	print(cancel.id)
	print(cancel.status)  # выведет статус отмены

	# закрываем неоплаченный счет
	services = await wiq.getServices()
	for service in services:
		print(service.ID)  # id услуги
		print(service.category)  # id категории услуги
		print(service.name)  # название услуги на англ
		print(service.cost)  # стоимость услуги
		print(service.min)  # минимальное количество для заказа
		print(service.max)  # максимальное количество для заказа
		print(service.refill)  # можно ли вернуть отписки (bool)
		print(service.cancel)  # можно ли отменять услугу (bool)


if __name__ == "__main__":
	asyncio.run(start())
