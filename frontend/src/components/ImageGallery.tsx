import React, { useState } from "react";
import { deleteImagesApiImageDeleteDelete } from "@/gen/image/image";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import ImageThumbnail from "./ImageThumbnail";
import { Button } from "@/components/ui/button";
import { ImageGalleryProps } from "@/types";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";

const ImageGallery: React.FC<ImageGalleryProps> = ({ images, isLoading, onRefresh }) => {
  const [selectedImageFilenames, setSelectedImageFilenames] = useState<string[]>([]);
  const [isDeleting, setIsDeleting] = useState(false);

  // Toggle image selection
  const toggleImageSelection = (imageFilename: string) => {
    setSelectedImageFilenames((prev) =>
      prev.includes(imageFilename)
        ? prev.filter((filename) => filename !== imageFilename)
        : [...prev, imageFilename]
    );
  };

  // Delete selected images
  const handleDeleteImages = async () => {
    if (selectedImageFilenames.length === 0) {
      alert("select images to delete");
      return;
    }

    if (!confirm(`delete ${selectedImageFilenames.length} images?`)) {
      return;
    }

    setIsDeleting(true);
    try {
      await deleteImagesApiImageDeleteDelete({
        image_filenames: selectedImageFilenames,
      });

      // Refresh the image list and clear selection
      onRefresh();
      setSelectedImageFilenames([]);
    } catch (error) {
      console.error("Error deleting images:", error);
      alert("failed to delete images");
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <Card className="shadow-lg border border-gray-200 rounded-lg">
      <CardHeader className="p-4">
        <CardTitle className="text-2xl font-semibold mb-4">Gallery</CardTitle>
        <div className="flex justify-center items-center gap-4">
          <Button
            onClick={onRefresh}
            disabled={isLoading || isDeleting}
            className={`py-2 px-4 rounded text-md font-semibold ${
              isLoading || isDeleting
                ? "bg-gray-300 text-gray-500"
                : "bg-blue-500 text-white hover:bg-blue-600"
            }`}
          >
            Refresh
          </Button>

          <Button
            onClick={handleDeleteImages}
            disabled={isLoading || isDeleting || selectedImageFilenames.length === 0}
            className={`py-2 px-4 rounded text-md font-semibold transition-colors duration-200 ${
              isLoading || isDeleting || selectedImageFilenames.length === 0
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-red-500 text-white hover:bg-red-600"
            }`}
          >
            Delete ({selectedImageFilenames.length})
          </Button>
        </div>
      </CardHeader>

      <CardContent className="p-4">
        {isLoading || isDeleting ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : images.length === 0 ? (
          <div className="text-center py-8 text-gray-500">No images found</div>
        ) : (
          <ScrollArea className="h-80">
            <div className="flex w-max space-x-4 p-4">
              {images.map((image, index) => (
                <ImageThumbnail
                  key={index}
                  image={image}
                  isSelected={selectedImageFilenames.includes(image.image_filename)}
                  onSelect={() => toggleImageSelection(image.image_filename)}
                />
              ))}
            </div>
            <ScrollBar orientation="horizontal" />
          </ScrollArea>
        )}
      </CardContent>
    </Card>
  );
};

export default ImageGallery;
