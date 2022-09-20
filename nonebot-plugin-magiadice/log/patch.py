import requests
from notion.settings import S3_URL_PREFIX
def upload_file_image(self, path,name,type):
    data = self._client.post(
            "getUploadFileUrl",
            {"bucket": "secure", "name": name, "contentType": type},
        ).json()
    with open(path, "rb") as f:
        response = requests.put(
                data["signedPutUrl"], data=f, headers={"Content-type": type}
            )
        response.raise_for_status()

    self.display_source = data["url"]
    self.source = data["url"]
    self.file_id = data["url"][len(S3_URL_PREFIX) :].split("/")[0]