import asyncio
from infinitecraft import InfiniteCraft
from collections import deque
import math



async def main():
    async with InfiniteCraft() as game:  # automatically start session and end session on async with end
        # read the file to see what already checked

        try:
            with open("checked.txt") as f:
                checked = set(f.read().splitlines())
        except FileNotFoundError:
            with open("checked.txt", 'w'):
                checked = set()

        disc_items = set(game.discoveries)
        disc_items_ordered = list(game.discoveries)
        # only queue what isn't checked
        queue = deque(item for item in game.discoveries if item.name not in checked)


        attempted_pairs = set()
        banned = set()
        while queue:
            fail_limit = int(20 + 50 * math.log(1 + len(checked) / 100) / math.log(1 + 3000 / 100))
            fail = 0
            print(f"Fail limit: {fail_limit}")
            count = 0
            # get the first item that needs to be used
            a = queue.popleft()
            # pair it with every other item
            for b in disc_items_ordered:
                # if already paired, skip
                curr_pair = tuple(sorted((a.name, b.name)))

                if curr_pair in attempted_pairs:
                    continue
                #if not paired, pair it
                else:
                    try:
                        attempted_pairs.add(curr_pair)
                        if fail < fail_limit:
                            print(f"Pairing elements: {a} and {b}")
                            result = await game.pair(a, b)
                            print(f"Result: {result}")
                            await asyncio.sleep(0.15)
                            # check for a result, and if new, add the discovery and into the queue


                            if result and result not in disc_items:
                                disc_items.add(result)
                                queue.append(result)
                                disc_items_ordered.append(result)
                                count += 1
                                print(f"New item. {len(game.discoveries)} items total. {count} new items for this item")
                                fail = 0
                            else:
                                fail += 1
                        else:
                            banned.add(a)
                            break
                    except PermissionError:
                        await asyncio.sleep(2)
                        continue



            with open("checked.txt", "a") as f:
                f.write(f"{a.name}\n")


asyncio.run(main())
