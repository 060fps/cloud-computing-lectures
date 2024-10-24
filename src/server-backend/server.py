import asyncio
import json
import logging
from websockets import serve

logging.basicConfig(level=logging.INFO)

USERS = set()  # This will store connected WebSocket clients
VALUE = 0  # Shared value


def user_event():
    """Create a JSON message with the current user count."""
    return json.dumps({"type": "users", "count": len(USERS)})


def value_event():
    """Create a JSON message with the current value."""
    return json.dumps({"type": "value", "value": VALUE})


async def broadcast(message):
    """Send a message to all connected clients."""
    if USERS:  # Only broadcast if there are connected users
        await asyncio.wait([user.send(message) for user in USERS])


async def counter(websocket):
    global USERS, VALUE
    try:
        # Register user
        USERS.add(websocket)
        await broadcast(user_event())  # Inform others a new user has joined

        # Send current state to the new user
        await websocket.send(value_event())

        # Manage state changes based on user input
        async for message in websocket:
            event = json.loads(message)
            if event["action"] == "minus":
                VALUE -= 1
                await broadcast(value_event())
            elif event["action"] == "plus":
                VALUE += 1
                await broadcast(value_event())
            else:
                logging.error("unsupported event: %s", event)

    finally:
        # Unregister user
        USERS.remove(websocket)
        await broadcast(user_event())  # Inform others a user has left


async def main():
    async with serve(counter, "0.0.0.0", 8000):
        await asyncio.get_running_loop().create_future()  # Keep server running


if __name__ == "__main__":
    asyncio.run(main())
