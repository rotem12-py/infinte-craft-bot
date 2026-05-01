import asyncio
from infinitecraft import InfiniteCraft
from collections import deque
from infinitecraft.errors.clients import ClientResponseError
#from conv import create_out



async def main():
    async with InfiniteCraft() as game:  # automatically start session and end session on async with end
        # read the file to see what already checked
        with open("checked") as f:
            checked = set(f.read().splitlines())

        disc_items = set(game.discoveries)
        # only queue what isn't checked
        queue = deque(item for item in reversed(game.discoveries) if item.name not in checked)

        attempted_pairs = set()
        while queue:
            # get the first item that needs to be used
            a = queue.popleft()
            # pair it with every other item
            for b in list(disc_items):
                # if already paired, skip
                curr_pair = tuple(sorted((a.name, b.name)))

                if curr_pair in attempted_pairs:
                    pass
                #if not paired, pair it
                else:
                    attempted_pairs.add(curr_pair)
                    print(f"Pairing elements: {a} and {b}")
                    result = await game.pair(a, b)
                    print(f"Result: {result}")
                    await asyncio.sleep(0.15)
                    # check for a result, and if new, add the discovery and into the queue
                    if result and result not in disc_items:
                        disc_items.add(result)
                        queue.appendleft(result)




            with open("checked", "a") as f:
                f.write(f"{a.name}\n")


asyncio.run(main())
