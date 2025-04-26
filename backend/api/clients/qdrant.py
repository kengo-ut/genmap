import uuid

import numpy as np
from fastapi import HTTPException
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from api.config import Settings
from api.schema import SimpleMetadata


class QdrantClientManager:
    def __init__(self, settings: Settings):
        self.qdrant = QdrantClient(path=settings.QDRANT_DB_PATH)
        self.collection_name = settings.COLLECTION_NAME
        self.embedding_dim = settings.EMBEDDING_DIM
        self._init_collection()

    def _init_collection(self):
        """コレクションの初期化 (存在しなければ作成)"""
        collection_names = [
            collection.name for collection in self.qdrant.get_collections().collections
        ]

        if self.collection_name not in collection_names:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "image": VectorParams(
                        size=self.embedding_dim, distance=Distance.COSINE
                    ),
                    "text": VectorParams(
                        size=self.embedding_dim, distance=Distance.COSINE
                    ),
                },
            )

    def upload_point(
        self,
        image_embedding: np.ndarray,
        text_embedding: np.ndarray,
        image_filename: str,
        prompt: str,
    ):
        """ポイント (画像・テキストのembeddingとメタデータ)をQdrantにアップロード"""
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector={"image": image_embedding.tolist(), "text": text_embedding.tolist()},
            payload={"image_filename": image_filename, "prompt": prompt},
        )

        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=[point],
        )

    def search_points(
        self,
        query_embedding: np.ndarray,
        topk: int = 5,
    ) -> list[SimpleMetadata]:
        """指定したembeddingに基づいてQdrantからポイントを検索"""
        results = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            using="image",
            with_payload=True,
            with_vectors=False,
            limit=topk,
        ).points

        simple_metadata_list = []
        for result in results:
            if result is None or result.payload is None:
                raise HTTPException(
                    status_code=404, detail="No points found in Qdrant."
                )
            metadata: SimpleMetadata = SimpleMetadata(**result.payload)
            simple_metadata_list.append(metadata)

        return simple_metadata_list

    def delete_point(self, image_filename: str):
        """指定した画像ファイル名のポイントをQdrantから削除"""
        points = self.qdrant.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="image_filename",
                        match=MatchValue(value=image_filename),
                    )
                ]
            ),
            limit=1,
        )
        if not points or not points[0]:
            raise HTTPException(
                status_code=404,
                detail=f"Image with filename {image_filename} not found in Qdrant.",
            )
        point_id = points[0][0].id
        self.qdrant.delete(
            collection_name=self.collection_name,
            points_selector=[point_id],
        )
