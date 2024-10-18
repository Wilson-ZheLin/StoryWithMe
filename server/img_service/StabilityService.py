import json
import os
import requests
import time
import yaml

class StabilityService:

    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.stability_key = self.config["stability_key"]
        self.generation_host = self.config["generation_host"]

    def generate_image(self, prompt, filename, negative_prompt="", aspect_ratio="16:9", seed=42, output_format='webp'):
        params = {
            "prompt": prompt,
            "negative_prompt": negative_prompt, # elements to exclude from the image
            "aspect_ratio": aspect_ratio, # 16:9 1:1 21:9 2:3 3:2 4:5 5:4 9:16 9:21
            "seed": seed,
            "output_format": output_format,
        }

        # Send request
        response = self.send_generation_request(self.generation_host, params)
        if response.headers.get("finish-reason") == 'CONTENT_FILTERED':
            raise Warning("Generation failed NSFW classifier")
        output_image = response.content

        # Save image
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # server dir
        img_dir = os.path.join(base_dir, "static", "img") # img dir
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        generated = os.path.join(img_dir, f"{filename}.{output_format}")
        with open(generated, "wb") as f:
            f.write(output_image)

    def send_generation_request(self, host, params):
        headers = {
            "Accept": "image/*",
            "Authorization": f"Bearer {self.stability_key}"
        }

        # Encode parameters
        files = {}
        image = params.pop("image", None)
        mask = params.pop("mask", None)
        if image is not None and image != '':
            files["image"] = open(image, 'rb')
        if mask is not None and mask != '':
            files["mask"] = open(mask, 'rb')
        if len(files)==0:
            files["none"] = ''

        # Send request
        print(f"Sending REST request to {host}...")
        response = requests.post(
            host,
            headers=headers,
            files=files,
            data=params
        )
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

        return response

    def send_async_generation_request(self, host, params):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.stability_key}"
        }

        # Encode parameters
        files = {}
        if "image" in params:
            image = params.pop("image")
            files = {"image": open(image, 'rb')}

        # Send request
        print(f"Sending REST request to {host}...")
        response = requests.post(
            host,
            headers=headers,
            files=files,
            data=params
        )
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

        # Process async response
        response_dict = json.loads(response.text)
        generation_id = response_dict.get("id", None)
        assert generation_id is not None, "Expected id in response"

        # Loop until result or timeout
        timeout = int(os.getenv("WORKER_TIMEOUT", 500))
        start = time.time()
        status_code = 202
        while status_code == 202:
            response = requests.get(
                f"{host}/result/{generation_id}",
                headers={
                    **headers,
                    "Accept": "image/*"
                },
            )

            if not response.ok:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            status_code = response.status_code
            time.sleep(10)
            if time.time() - start > timeout:
                raise Exception(f"Timeout after {timeout} seconds")

        return response
    
if __name__ == "__main__":
    stability_service = StabilityService()
    stability_service.generate_image("Snow White's Castle", "test_generation_img")