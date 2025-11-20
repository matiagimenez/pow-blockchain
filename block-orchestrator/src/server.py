import ast
import json
import sys
from redis import exceptions as redis_exceptions
from pika import exceptions as rabbitmq_exceptions
from flask import jsonify, request
from datetime import datetime
from model.block import Block
from infrastructure.rabbitmq import RabbitMQClient
from plugins.redis import redis_connect
from plugins.scheduler import start_cronjob
from src.utils import Settings

redis = redis_connect()


async def build_block(transactions):
    async with RabbitMQClient() as channel:
        exchange = await channel.get_exchange(Settings.RABBITMQ_EXCHANGE)
        if (len(transactions) > 0):
            try:
                # Obtengo el id del último bloque de la blockchain
                last_block_hash = redis.zrange(
                    'block_hashes', -1, -1, withscores=True)

                if (len(last_block_hash) == 0):
                    # Si last_block = [] se crea el bloque genesis
                    previous_hash = 0
                    last_index = 0
                else:
                    # Obtengo el último bloque de la blochain
                    last_index = redis.zcount('block_hashes', '-inf', '+inf')
                    previous_hash = last_block_hash[0][0]

                print(f"{datetime.now()}: Building transactions block...",
                    file=sys.stdout, flush=True)

                block = {
                    'index': last_index,
                    'previous_hash': previous_hash,
                    'data': transactions,
                    "timestamp": f"{round(datetime.now().timestamp())}",
                    'nonce': 0,
                    'hash': "",
                }

                new_block = Block(
                    block["data"], block["timestamp"], block["hash"], block["previous_hash"], block["nonce"], block["index"])

                await exchange.publish(
                    routing_key='bl',
                    message=json.dumps({"challenge": str(hash_challenge), "block": new_block.to_dict()}))

                print(
                    f"{datetime.now()}: Block {new_block.index} [{new_block.previous_hash}] created ...")
            except redis_exceptions.RedisError as error:
                print(f"Redis error: {error}", file=sys.stderr, flush=True)
            except rabbitmq_exceptions.AMQPError as error:
                print(f"RabbitMQ error: {error}", file=sys.stderr, flush=True)
            except Exception as e:
                print(f"Unexpected error: {e}", file=sys.stderr, flush=True)

        else:
            print(f"{datetime.now()}: There is no transactions",
                file=sys.stdout, flush=True)


def process_transactions():
    # Procesa hasta 50 transacciones o hasta que pase 1 segundo sin que se agreguen transacciones a la queue
    transactions = []
    try:
        for method, properties, body in rabbitmq.consume('transactions', inactivity_timeout=1):
            if method and len(transactions) < 50:
                transaction = ast.literal_eval(body.decode("utf-8"))
                transactions.append(transaction)
                rabbitmq.basic_ack(method.delivery_tag)
            else:
                build_block(transactions)
                break
    except rabbitmq_exceptions.AMQPError as error:
        print(f"RabbitMQ error: {error}", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr, flush=True)


# Inicia el cronjob para crear bloques
start_cronjob(process_transactions, 60)

@ app.route("/result", methods=['POST'])
def validateBlock():
    try:
        block = ast.literal_eval(request.get_data().decode("utf-8"))

        timestamp = block["timestamp"]
        block_hash = block["hash"]
        previous_hash = block["previous_hash"]
        data = block["data"]
        index = block["index"]
        nonce = block["nonce"]

        new_block = Block(
            data, timestamp, block_hash, previous_hash, nonce, index)

        block_is_valid = new_block.validate()

        # Si el bloque no es valido, descarto.
        if (not block_is_valid):
            return jsonify({
                "status": "400",
                "description": f"The hash {new_block.hash} is not valid",
            })

        # Verifica si el bloque ya existe en redis
        block_id = f"blockchain:{new_block.previous_hash}"
        block_exists = redis.hexists(block_id, "hash")
        if block_exists:
            # Si ya existe descarto está request, porque ya un minero completo la tarea antes
            return jsonify({
                "status": "200",
                "description": f"Block {new_block.index} already exists",
            })

        # Guardo el hash del nuevo bloque en el sorted set
        redis.zadd('block_hashes', {
                   new_block.hash: datetime.now().timestamp()})
        # Guardo el bloque en la blockchain, asociandoló con el bloque anterior
        redis.hset(block_id, mapping=new_block.to_dict())

        return jsonify({
            "status": "200",
            "description": f"Block {new_block.index} created",
        })
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr, flush=True)
        return jsonify({
            "status": "500",
            "description": "Internal server error"
        })
