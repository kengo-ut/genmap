import React, { useState } from "react";
import { generateImageApiImageGeneratePost } from "@/gen/image/image";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { ControlImage1, ControlImage2, ImageGeneratorProps } from "@/types";
import { Switch } from "@/components/ui/switch";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { HelpCircle } from "lucide-react";
import ControlImageSelector from "@/components/ControlImageSelector";

const ImageGenerator: React.FC<ImageGeneratorProps> = ({ onImageGenerated }) => {
  const [prompt, setPrompt] = useState("");
  const [width, setWidth] = useState<number>(512);
  const [height, setHeight] = useState<number>(512);
  const [numInferenceSteps, setNumInferenceSteps] = useState(30);
  const [guidanceScale, setGuidanceScale] = useState(3.5);
  const [seed, setSeed] = useState<number>(42);
  const [isGenerating, setIsGenerating] = useState(false);
  const [useControlImage, setUseControlImage] = useState(false);
  const [controlImage1, setControlImage1] = useState<ControlImage1>({
    controlImageFilename: null,
    controlnetConditioningScale: null,
    controlGuidanceEnd: null,
  });
  const [controlImage2, setControlImage2] = useState<ControlImage2>({
    controlImageFilename: null,
    controlnetConditioningScale: null,
    controlGuidanceEnd: null,
  });

  const handleChangeControlImage1 = (update: Partial<ControlImage1>) => {
    setControlImage1((prev) => ({
      ...prev,
      ...update,
    }));
  };

  const handleChangeControlImage2 = (update: Partial<ControlImage2>) => {
    setControlImage2((prev) => ({
      ...prev,
      ...update,
    }));
  };

  // Generate image
  const handleGenerateImage = async () => {
    setIsGenerating(true);
    try {
      await generateImageApiImageGeneratePost({
        prompt: prompt,
        width: width,
        height: height,
        control_image_filename_1: controlImage1.controlImageFilename,
        control_image_filename_2: controlImage2.controlImageFilename,
        controlnet_conditioning_scale_1: controlImage1.controlnetConditioningScale,
        controlnet_conditioning_scale_2: controlImage2.controlnetConditioningScale,
        control_guidance_end_1: controlImage1.controlGuidanceEnd,
        control_guidance_end_2: controlImage2.controlGuidanceEnd,
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

  console.log(useControlImage);

  return (
    <Card className="shadow-lg border border-gray-200 rounded-lg">
      <CardHeader className="p-4">
        <CardTitle className="text-2xl font-semibold">Generation</CardTitle>
      </CardHeader>
      <CardContent className="p-4">
        <div className="mb-4">
          {/* Control Image Toggle */}
          <div className="flex items-center space-x-2">
            <Switch
              id="control-image"
              checked={useControlImage}
              onCheckedChange={() => setUseControlImage(!useControlImage)}
            />
            <Label htmlFor="cross-modal" className="text-md font-semibold">
              use control images
            </Label>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger>
                  <HelpCircle className="w-4 h-4 text-gray-400 cursor-pointer" />
                </TooltipTrigger>
                <TooltipContent>
                  <p>Use control images to guide generation</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </div>
        {useControlImage && (
          <div className="mb-4">
            <ControlImageSelector
              controlImage1={controlImage1}
              controlImage2={controlImage2}
              onChangeControlImage1={handleChangeControlImage1}
              onChangeControlImage2={handleChangeControlImage2}
            />
          </div>
        )}
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
            min={64}
            max={1024}
            step={16}
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
            min={64}
            max={1024}
            step={16}
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
