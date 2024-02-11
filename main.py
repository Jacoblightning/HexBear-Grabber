import requests
import lxml.html
import json
import os

MAX_IN_A_ROW = 10
lines = []

current_row = 0
current_overlap = 0
last_len = 0

if os.path.exists("progress.json"):
    print("Previous progress found, restoring")
    with open("progress.json") as fd:
        lines = json.load(fd)
        assert issubclass(type(lines), list)
    print(f"Restored {len(lines)} lines")
    last_len = len(lines)

try:
    while True:
        response = requests.get("https://hexbear.net/", stream=True)
        try:
            response.raw.decode_content = True
            tree = lxml.html.parse(response.raw)

            tagline: str = tree.xpath("/html/body/div/div/div[2]/div/div/div/main/div[1]/p")[0].text_content()

            if tagline in lines:
                current_row += 1
                current_overlap += 1
                print(f"Overlapping tagline found. \n{current_row} in a row.\n{current_overlap} in total.")
                if current_row > MAX_IN_A_ROW:
                    break
            else:
                current_row = 0
                lines.append(tagline)
                print(f"# of taglines: {len(lines)}")
        finally:
            response.close()
except (Exception, KeyboardInterrupt):
    if not len(lines):
        raise
    print("Exception!!! Saving progress")
    with open("progress.json", "w") as fd:
        json.dump(lines, fd)
    print(f"Saved {len(lines)} lines.")
    raise
