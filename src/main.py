
import requests, random
import io, os, json
from PIL import Image

# insert your own api key here!
API_KEY = "Your api key"

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {API_KEY}"}

def listToString(lst):
    ret = ""
    for i in lst:
         ret += i
    return ret 

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

def generate(prompt, seed = random.randint(1000,9999), name = "Image.png"):
    image_bytes = query({
        "inputs": f"{prompt} {random.randint(1000,9999)}",
    })
    image = Image.open(io.BytesIO(image_bytes))
    image.save(name)

def main(source = "data.json"):
    try:
        failedCtr = 0
        idx = 0
        with open(source, "r") as f:
            data = json.load(f)["data"]

        failed = []
        run = True
        while (run):
            try:
                prompt = data[idx]
            except:
                print("Done!")
                run = False

            if not(run):
                break
                
            print(prompt)
            try:
                generate(prompt, name = os.path.join("out", str(prompt)+".png"))
                failedCtr = 0
            except BaseException as e:
                print(f"Error occured with prompt: {prompt}\nerror: "+str(e))
                failed.append(prompt)
                with open("missed.json", "w") as f:
                    json.dump({"data":failed}, f)
                failedCtr += 1

            idx += 1

            if failedCtr >= 60:
                for i in data[idx:-1]:
                    failed.append(i)
                with open("missed.json", "w") as f:
                    json.dump({"data":failed}, f)
                print("\n\nFailed 60 times in a row.\nExited program and dumped unused prompts.\n\n")
                exit()

        with open("missed.json", "w") as f:
            json.dump({"data":failed})

    except KeyboardInterrupt:
        with open("missed.json", "w") as f:
            json.dump({"data":failed}, f)
            print("KEYBOARDINTERRUPT ^C")
            exit()


if __name__ == '__main__':
    main("missed.json")