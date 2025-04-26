from datetime import UTC, datetime

from sqlalchemy import TIMESTAMP, Column, Float, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from api.config import Settings

Base = declarative_base()


class ImageMetadata(Base):  # type: ignore
    __tablename__ = "image_metadata"

    image_filename = Column(String, primary_key=True, index=True)
    prompt = Column(String)
    width = Column(Integer)
    height = Column(Integer)

    # 条件画像と各種パラメータ (最大2つまで)
    control_image_filename_1 = Column(String, nullable=True)
    control_image_filename_2 = Column(String, nullable=True)
    controlnet_conditioning_scale_1 = Column(Float, nullable=True)
    controlnet_conditioning_scale_2 = Column(Float, nullable=True)
    control_guidance_end_1 = Column(Float, nullable=True)
    control_guidance_end_2 = Column(Float, nullable=True)

    num_inference_steps = Column(Integer)
    guidance_scale = Column(Float)
    seed = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(UTC))


class SQLiteClient:
    def __init__(self, settings: Settings):
        self.db_url = f"sqlite:///{settings.SQLITE_DB_PATH}"
        self.engine = create_engine(
            self.db_url, connect_args={"check_same_thread": False}
        )
        self.SessionLocal = sessionmaker(bind=self.engine)
        # マイグレーション
        self._migrate()

    def _migrate(self):
        """テーブルが存在しない場合、マイグレーションを実行"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """セッションを取得"""
        return self.SessionLocal()

    def upload_metadata(
        self,
        image_filename: str,
        prompt: str,
        width: int,
        height: int,
        control_image_filename_1: str | None,
        control_image_filename_2: str | None,
        controlnet_conditioning_scale_1: float | None,
        controlnet_conditioning_scale_2: float | None,
        control_guidance_end_1: float | None,
        control_guidance_end_2: float | None,
        num_inference_steps: int,
        guidance_scale: float,
        seed: int,
    ) -> ImageMetadata:
        """メタデータをSQLiteにアップロード"""
        session: Session = self.get_session()

        new_metadata = ImageMetadata(
            image_filename=image_filename,
            prompt=prompt,
            width=width,
            height=height,
            control_image_filename_1=control_image_filename_1,
            control_image_filename_2=control_image_filename_2,
            controlnet_conditioning_scale_1=controlnet_conditioning_scale_1,
            controlnet_conditioning_scale_2=controlnet_conditioning_scale_2,
            control_guidance_end_1=control_guidance_end_1,
            control_guidance_end_2=control_guidance_end_2,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            seed=seed,
        )

        session.add(new_metadata)
        session.commit()
        session.refresh(new_metadata)
        session.close()
        return new_metadata

    def retrieve_metadata_list(self) -> list[ImageMetadata]:
        """メタデータの一覧を取得"""
        session: Session = self.get_session()
        metadata_list = session.query(ImageMetadata).all()
        session.close()
        return metadata_list

    def delete_metadata(self, image_filename: str):
        """画像ファイル名でメタデータを削除"""
        session: Session = self.get_session()
        metadata_to_delete = (
            session.query(ImageMetadata)
            .filter(ImageMetadata.image_filename == image_filename)
            .first()
        )
        if metadata_to_delete:
            session.delete(metadata_to_delete)
            session.commit()
        session.close()
