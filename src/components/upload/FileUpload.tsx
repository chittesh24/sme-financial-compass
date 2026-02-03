import { useCallback, useState } from "react";
import { cn } from "@/lib/utils";
import { Upload, File, X, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

interface FileUploadProps {
  onFilesSelected: (files: File[]) => void;
  acceptedTypes?: string[];
  maxFiles?: number;
  className?: string;
}

interface UploadedFile {
  file: File;
  progress: number;
  status: "uploading" | "complete" | "error";
}

export function FileUpload({
  onFilesSelected,
  acceptedTypes = [".csv", ".xlsx", ".pdf"],
  maxFiles = 5,
  className,
}: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragging(true);
    } else if (e.type === "dragleave") {
      setIsDragging(false);
    }
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);

      const files = Array.from(e.dataTransfer.files).slice(0, maxFiles);
      processFiles(files);
    },
    [maxFiles]
  );

  const handleFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files) {
        const files = Array.from(e.target.files).slice(0, maxFiles);
        processFiles(files);
      }
    },
    [maxFiles]
  );

  const processFiles = (files: File[]) => {
    const newFiles: UploadedFile[] = files.map((file) => ({
      file,
      progress: 0,
      status: "uploading" as const,
    }));

    setUploadedFiles((prev) => [...prev, ...newFiles]);

    // Simulate upload progress
    newFiles.forEach((uploadedFile, index) => {
      const interval = setInterval(() => {
        setUploadedFiles((prev) =>
          prev.map((f) => {
            if (f.file === uploadedFile.file) {
              const newProgress = Math.min(f.progress + 20, 100);
              return {
                ...f,
                progress: newProgress,
                status: newProgress === 100 ? "complete" : "uploading",
              };
            }
            return f;
          })
        );
      }, 200 * (index + 1));

      setTimeout(() => clearInterval(interval), 1200);
    });

    onFilesSelected(files);
  };

  const removeFile = (file: File) => {
    setUploadedFiles((prev) => prev.filter((f) => f.file !== file));
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <div className={cn("space-y-4", className)}>
      {/* Drop Zone */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={cn(
          "relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed p-8 transition-all duration-200",
          isDragging
            ? "border-accent bg-accent/5"
            : "border-border bg-muted/30 hover:border-accent/50 hover:bg-muted/50"
        )}
      >
        <input
          type="file"
          multiple
          accept={acceptedTypes.join(",")}
          onChange={handleFileSelect}
          className="absolute inset-0 cursor-pointer opacity-0"
        />
        <div
          className={cn(
            "flex h-16 w-16 items-center justify-center rounded-full transition-all duration-200",
            isDragging ? "bg-accent text-accent-foreground" : "bg-muted"
          )}
        >
          <Upload className="h-8 w-8" />
        </div>
        <p className="mt-4 text-center font-medium">
          Drag & drop your financial files here
        </p>
        <p className="mt-1 text-center text-sm text-muted-foreground">
          or click to browse
        </p>
        <p className="mt-2 text-xs text-muted-foreground">
          Supported formats: CSV, XLSX, PDF (Max {maxFiles} files)
        </p>
      </div>

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <div className="space-y-2">
          {uploadedFiles.map((uploadedFile, index) => (
            <div
              key={index}
              className="flex items-center gap-3 rounded-lg border bg-card p-3"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-muted">
                <File className="h-5 w-5 text-muted-foreground" />
              </div>
              <div className="flex-1 space-y-1">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium">{uploadedFile.file.name}</p>
                  {uploadedFile.status === "complete" ? (
                    <CheckCircle2 className="h-4 w-4 text-success" />
                  ) : (
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-6 w-6"
                      onClick={() => removeFile(uploadedFile.file)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <Progress value={uploadedFile.progress} className="h-1 flex-1" />
                  <span className="text-xs text-muted-foreground">
                    {formatFileSize(uploadedFile.file.size)}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
