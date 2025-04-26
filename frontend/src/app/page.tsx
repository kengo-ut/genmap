"use client";

import React, { useState, useEffect } from "react";
import { SimpleMetadata } from "@/gen/schema";
import ImageGenerator from "@/components/ImageGenerator";
import ImageSearch from "@/components/ImageSearch";
import ImageGallery from "@/components/ImageGallery";
import { getAllSimpleMetadataApiImageAllSimpleMetadataGet } from "@/gen/image/image";
import SearchResults from "@/components/SearchResults";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";

export default function Home() {
  const [images, setImages] = useState<SimpleMetadata[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchResults, setSearchResults] = useState<SimpleMetadata[]>([]);

  // Fetch all images on load
  useEffect(() => {
    fetchImages();
  }, []);

  // Fetch all images
  const fetchImages = async () => {
    setIsLoading(true);
    try {
      const response = await getAllSimpleMetadataApiImageAllSimpleMetadataGet();
      setImages(response.data);
    } catch (error) {
      console.error("Error fetching images:", error);
      alert("画像の取得に失敗しました");
    } finally {
      setIsLoading(false);
    }
  };

  // Update search results
  const handleSearchResults = (results: SimpleMetadata[]) => {
    setSearchResults(results);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8 text-center">GenMap</h1>

      <Tabs defaultValue="generate" className="flex flex-col gap-3">
        <TabsList className="grid w-full grid-cols-2 h-14">
          <TabsTrigger
            value="generate"
            className="text-2xl font-semibold data-[state=active]:bg-gray-500 data-[state=active]:text-white data-[state=active]:shadow-md"
          >
            Generate
          </TabsTrigger>
          <TabsTrigger
            value="search"
            className="text-2xl font-semibold data-[state=active]:bg-gray-500 data-[state=active]:text-white data-[state=active]:shadow-md"
          >
            Search
          </TabsTrigger>
        </TabsList>
        {/* Generateページ */}
        <TabsContent value="generate" className="w-full">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Left Side */}
            <div className="flex flex-col gap-4 bg-gray-100 p-6 rounded-lg border-r">
              <h2 className="text-xl font-semibold mb-4">Input</h2>
              <ImageGenerator onImageGenerated={fetchImages} />
            </div>

            {/* Right Side */}
            <div className="flex flex-col gap-4 bg-white p-6 rounded-lg shadow-lg">
              <h2 className="text-xl font-semibold mb-4">Output</h2>
              <ImageGallery images={images} isLoading={isLoading} onRefresh={fetchImages} />
            </div>
          </div>
        </TabsContent>

        {/* Searchページ */}
        <TabsContent value="search" className="w-full">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Left Side */}
            <div className="flex flex-col gap-4 bg-gray-100 p-6 rounded-lg border-r">
              <h2 className="text-xl font-semibold mb-4">Input</h2>
              <ImageSearch onSearchResults={handleSearchResults} />
            </div>

            {/* Right Side */}
            <div className="flex flex-col gap-4 bg-white p-6 rounded-lg shadow-lg">
              <h2 className="text-xl font-semibold mb-4">Output</h2>
              <SearchResults
                searchResults={searchResults}
                setSearchResults={setSearchResults}
                onRefresh={fetchImages}
              />
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
