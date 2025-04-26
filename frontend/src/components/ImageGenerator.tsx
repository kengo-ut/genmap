import React, { useState } from "react";
import { generateImageApiImageGeneratePost } from "@/gen/image/image";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { ImageGeneratorProps } from "@/types";

const ImageGenerator: React.FC<ImageGeneratorProps> = ({ onImageGenerated }) => {
  const [prompt, setPrompt] = useState("");
  const [width, setWidth] = useState<number>(512);
  const [height, setHeight] = useState<number>(512);
  const [numInferenceSteps, setNumInferenceSteps] = useState(30);
  const [guidanceScale, setGuidanceScale] = useState(3.5);
  const [seed, setSeed] = useState<number>(42);
  const [isGenerating, setIsGenerating] = useState(false);

  // Generate image
  const handleGenerateImage = async () => {
    setIsGenerating(true);
    try {
      await generateImageApiImageGeneratePost({
        prompt: prompt,
        width: width,
        height: height,
        num_inference_steps: numInferenceSteps,
        guidance_scale: guidanceScale,
        seed: seed,
      });

      // Notify parent to refresh the image list
      onImageGenerated();
    } catch (error) {
      console.error("Error generating image:", error);
      alert("failed to generate image");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <Card className="shadow-lg border border-gray-200 rounded-lg">
      <CardHeader className="p-4">
        <CardTitle className="text-2xl font-semibold">Generation</CardTitle>
      </CardHeader>
      <CardContent className="p-4">
        <div className="mb-4">
          <label className="block text-md font-semibold mb-1">prompt:</label>
          <Input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="text prompt (e.g., 'A cute, fluffy cat with striking green eyes.')"
            disabled={isGenerating}
          />
        </div>

        <div className="mb-4">
          <Label htmlFor="width" className="block text-md font-semibold mb-1">
            width: {width}
          </Label>
          <Slider
            defaultValue={[width]}
            min={100}
            max={1024}
            onValueChange={(value) => setWidth(value[0])}
            disabled={isGenerating}
          />
        </div>

        <div className="mb-4">
          <Label htmlFor="steps" className="block text-md font-semibold mb-1">
            height: {height}
          </Label>
          <Slider
            defaultValue={[height]}
            min={100}
            max={1024}
            onValueChange={(value) => setHeight(value[0])}
            disabled={isGenerating}
          />
        </div>

        <div className="mb-4">
          <Label htmlFor="steps" className="block text-md font-semibold mb-1">
            steps: {numInferenceSteps}
          </Label>
          <Slider
            defaultValue={[numInferenceSteps]}
            min={10}
            max={50}
            onValueChange={(value) => setNumInferenceSteps(value[0])}
            disabled={isGenerating}
          />
        </div>

        <div className="mb-4">
          <Label htmlFor="guidance-scale" className="block text-md font-semibold mb-1">
            guidance scale: {guidanceScale}
          </Label>
          <Slider
            defaultValue={[guidanceScale]}
            min={0}
            max={10}
            step={0.5}
            onValueChange={(value) => setGuidanceScale(value[0])}
            disabled={isGenerating}
            color="red"
          />
        </div>

        <div className="mb-4">
          <Label htmlFor="seed" className="block text-md font-semibold mb-1">
            seed: {seed}
          </Label>
          <Slider
            defaultValue={[seed]}
            min={0}
            max={1024}
            onValueChange={(value) => setSeed(value[0])}
            disabled={isGenerating}
            color="red"
          />
        </div>

        <Button
          onClick={handleGenerateImage}
          disabled={isGenerating || !prompt.trim()}
          className={`w-full py-2 rounded text-md font-semibold ${
            isGenerating || !prompt.trim()
              ? "bg-gray-300 text-gray-500"
              : "bg-blue-500 text-white hover:bg-blue-600"
          }`}
        >
          {isGenerating ? "Generating..." : "Generate"}
        </Button>
      </CardContent>
    </Card>
  );
};

export default ImageGenerator;
