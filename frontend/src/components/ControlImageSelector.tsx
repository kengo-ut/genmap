import { Label } from "@/components/ui/label";
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectItem,
  SelectValue,
} from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { ControlImage1, ControlImage2 } from "@/types";
import Image from "next/image";
import React, { useEffect } from "react";
import { Card, CardContent, CardTitle, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { getAllControlImageFilenamesApiImageAllControlImageFilenamesGet } from "@/gen/image/image";
import { RotateCcw } from "lucide-react";

type ControlImageSelectorProps = {
  controlImage1: ControlImage1;
  controlImage2: ControlImage2;
  onChangeControlImage1: (data: Partial<ControlImage1>) => void;
  onChangeControlImage2: (data: Partial<ControlImage2>) => void;
};

const ControlImageSelector: React.FC<ControlImageSelectorProps> = ({
  controlImage1,
  controlImage2,
  onChangeControlImage1,
  onChangeControlImage2,
}) => {
  const [controlImageFilenames, setControlImageFilenames] = useState<string[]>([]);

  const handleReloadControlImages = async () => {
    try {
      const response = await getAllControlImageFilenamesApiImageAllControlImageFilenamesGet(); // ← APIクライアント
      setControlImageFilenames(response.data);
    } catch (error) {
      console.error("Failed to reload control images:", error);
      alert("Failed to reload control images.");
    }
  };

  // Fetch all control images on load
  useEffect(() => {
    handleReloadControlImages();
  }, []);

  return (
    <div>
      <Button
        variant="outline"
        size="lg"
        onClick={handleReloadControlImages}
        className="mb-2 flex items-center gap-2"
      >
        <RotateCcw className="w-4 h-4" /> Reload control images
      </Button>
      <div className="flex gap-4">
        {/* Control Image 1 */}
        <Card className="w-1/2">
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle>Control Image 1</CardTitle>
              <Button
                variant="destructive"
                size="sm"
                onClick={() =>
                  onChangeControlImage1({
                    controlImageFilename: null,
                    controlnetConditioningScale: null,
                    controlGuidanceEnd: null,
                  })
                }
              >
                Reset
              </Button>
            </div>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            {/* Image Selector */}
            <Select
              onValueChange={(value) => onChangeControlImage1({ controlImageFilename: value })}
              value={controlImage1.controlImageFilename ?? ""}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select image" />
              </SelectTrigger>
              <SelectContent>
                {controlImageFilenames.map((filename) => (
                  <SelectItem key={filename} value={filename}>
                    {filename}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Preview */}
            {controlImage1.controlImageFilename && (
              <div className="relative w-full aspect-square">
                <Image
                  src={`/data/control_images/${controlImage1.controlImageFilename}`}
                  alt="Selected Control 1"
                  fill
                  className="rounded border object-contain"
                />
              </div>
            )}

            {/* Sliders */}
            <div>
              <Label>
                Conditioning Scale: {controlImage1.controlnetConditioningScale ?? "N/A"}
              </Label>
              <Slider
                defaultValue={[controlImage1.controlnetConditioningScale ?? 1]}
                min={0}
                max={2}
                step={0.1}
                onValueChange={(value) =>
                  onChangeControlImage1({ controlnetConditioningScale: value[0] })
                }
              />
            </div>
            <div>
              <Label>Guidance End: {controlImage1.controlGuidanceEnd ?? "N/A"}</Label>
              <Slider
                defaultValue={[controlImage1.controlGuidanceEnd ?? 1]}
                min={0}
                max={1}
                step={0.05}
                onValueChange={(value) => onChangeControlImage1({ controlGuidanceEnd: value[0] })}
              />
            </div>
          </CardContent>
        </Card>

        {/* Control Image 2 */}
        <Card className="w-1/2">
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle>Control Image 2</CardTitle>
              <Button
                variant="destructive"
                size="sm"
                onClick={() =>
                  onChangeControlImage2({
                    controlImageFilename: null,
                    controlnetConditioningScale: null,
                    controlGuidanceEnd: null,
                  })
                }
              >
                Reset
              </Button>
            </div>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            {/* Image Selector */}
            <Select
              onValueChange={(value) => onChangeControlImage2({ controlImageFilename: value })}
              value={controlImage2.controlImageFilename ?? ""}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select image" />
              </SelectTrigger>
              <SelectContent>
                {controlImageFilenames.map((filename) => (
                  <SelectItem key={filename} value={filename}>
                    {filename}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Preview */}
            {controlImage2.controlImageFilename && (
              <div className="relative w-full aspect-square">
                <Image
                  src={`/data/control_images/${controlImage2.controlImageFilename}`}
                  alt="Selected Control 2"
                  fill
                  className="rounded border object-contain"
                />
              </div>
            )}

            {/* Sliders */}
            <div>
              <Label>
                Conditioning Scale: {controlImage2.controlnetConditioningScale ?? "N/A"}
              </Label>
              <Slider
                defaultValue={[controlImage2.controlnetConditioningScale ?? 1]}
                min={0}
                max={2}
                step={0.1}
                onValueChange={(value) =>
                  onChangeControlImage2({ controlnetConditioningScale: value[0] })
                }
              />
            </div>
            <div>
              <Label>Guidance End: {controlImage2.controlGuidanceEnd ?? "N/A"}</Label>
              <Slider
                defaultValue={[controlImage2.controlGuidanceEnd ?? 1]}
                min={0}
                max={1}
                step={0.05}
                onValueChange={(value) => onChangeControlImage2({ controlGuidanceEnd: value[0] })}
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ControlImageSelector;
