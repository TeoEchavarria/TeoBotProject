from pydantic import BaseModel, Field

class Response(BaseModel):
    text: str = Field(description="The main text content")
    image_url: str = Field(description="URL of the image. In the case of existing")
    link_url: str = Field(description="URL of a related link. In the case of existing")