## Idea

We can create websocket subscription for market/ticker/orderbook data from most of the exchanges
If we will use it we will not PULL useless data if there is no update, we will not write again same data on disk

We can create a service for all the exchanges to connect by websocket and send data into Redis DB
Redis was chosen because it's fast solution to read/write data a lot, we should not store it in long term, so we should not save it into SSD/HDD at all.

We can pack all the services in docker and maybe run them on different servers? And they all will be connected to redis database, we will read order book or other information from Redis DB for use it in future

![Screenshot](/Screenshot.png)


## Running locally

You should have docker installed on your system before you will start to work with that code

Pull redis docker image:
```
docker pull redis
```

Run redis container
```
docker run --name redis -d -p 6379:6379 redis redis-server --requirepass "redispw"
```

Build container for parser
```
docker build -t gemini_to_redis .
```

Run the parser (here we are using 192.168.0.20 as machine local address because we are running redis in another container so 127.0.0.1 will not work fine because there is no redis inside our gemini docker image)
```
docker run -e REDIS_HOST=192.168.0.20 -e REDIS_PORT=6379 -e REDIS_PASSWORD=redispw gemini_to_redis

```

## Check information stored inside Redis
You can open console inside your docker image by command:
```
docker exec -it redis /bin/bash
```

Open redis CLI
```
redis-cli -a redispw

```
You can get all the prices for order book asks
```
HKEYS GEMINI_BTCUSD_ask
```
You can get coins amount for that price by
```
HGET GEMINI_BTCUSD_ask "51007.78"
```
