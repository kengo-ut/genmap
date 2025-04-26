import ImageThumbnail from "@/components/ImageThumbnail";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SearchResultsProps } from "@/types";
import { useState } from "react";
import { deleteImagesApiImageDeleteDelete } from "@/gen/image/image";
import { Button } from "@/components/ui/button";

const SearchResults = ({ searchResults, setSearchResults, onRefresh }: SearchResultsProps) => {
  // if (searchResults.length === 0) return null;

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

      onRefresh();
      setSelectedImageFilenames([]);
      setSearchResults(
        searchResults.filter((image) => !selectedImageFilenames.includes(image.image_filename))
      );
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
        <CardTitle className="text-2xl font-semibold mb-4">Search Results</CardTitle>
        <div className="flex justify-center items-center gap-4">
          <Button
            onClick={handleDeleteImages}
            disabled={isDeleting || selectedImageFilenames.length === 0}
            className={`py-2 px-4 rounded text-md font-semibold transition-colors duration-200 ${
              isDeleting || selectedImageFilenames.length === 0
                ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                : "bg-red-500 text-white hover:bg-red-600"
            }`}
          >
            Delete ({selectedImageFilenames.length})
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-4">
        {isDeleting ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : searchResults.length === 0 ? (
          <div className="text-center py-8 text-gray-500">No images found</div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 gap-4">
            {searchResults.map((image, index) => (
              <ImageThumbnail
                key={index}
                image={image}
                isSelected={selectedImageFilenames.includes(image.image_filename)}
                onSelect={() => toggleImageSelection(image.image_filename)}
              />
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default SearchResults;
