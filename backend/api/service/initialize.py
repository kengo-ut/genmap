from api.clients import (
    CLIPClient,
    DiffusionClient,
    LocalStorageClient,
    QdrantClientManager,
    SQLiteClient,
)
from api.config.settings import settings
from api.service.image import ImageService

diffusion_client = DiffusionClient(settings)
clip_client = CLIPClient(settings)
qdrant_client = QdrantClientManager(settings)
sqlite_client = SQLiteClient(settings)
local_storage_client = LocalStorageClient(settings)

image_service = ImageService(
    diffusion_client=diffusion_client,
    clip_client=clip_client,
    qdrant_client=qdrant_client,
    sqlite_client=sqlite_client,
    local_storage_client=local_storage_client,
    settings=settings,
)
