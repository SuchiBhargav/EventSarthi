import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, File, X, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { toast } from 'react-hot-toast';
import api from '@/services/api';
import { UploadProgress } from '@/types';

interface DocumentUploadProps {
  eventId: string;
  documentType: 'guest_list' | 'menu' | 'map' | 'schedule' | 'faq' | 'other';
  onUploadComplete?: () => void;
  acceptedFileTypes?: string;
  maxFiles?: number;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({
  eventId,
  documentType,
  onUploadComplete,
  acceptedFileTypes = '.pdf,.csv,.xlsx,.xls,.jpg,.jpeg,.png',
  maxFiles = 5,
}) => {
  const [uploads, setUploads] = useState<UploadProgress[]>([]);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      // Initialize upload progress for each file
      const newUploads: UploadProgress[] = acceptedFiles.map((file) => ({
        file,
        progress: 0,
        status: 'pending',
      }));

      setUploads((prev) => [...prev, ...newUploads]);

      // Upload files one by one
      for (let i = 0; i < acceptedFiles.length; i++) {
        const file = acceptedFiles[i];
        const uploadIndex = uploads.length + i;

        try {
          setUploads((prev) =>
            prev.map((upload, idx) =>
              idx === uploadIndex ? { ...upload, status: 'uploading' } : upload
            )
          );

          await api.uploadDocument(eventId, file, documentType, (progress) => {
            setUploads((prev) =>
              prev.map((upload, idx) =>
                idx === uploadIndex ? { ...upload, progress } : upload
              )
            );
          });

          setUploads((prev) =>
            prev.map((upload, idx) =>
              idx === uploadIndex ? { ...upload, status: 'success', progress: 100 } : upload
            )
          );

          toast.success(`${file.name} uploaded successfully`);
        } catch (error: any) {
          setUploads((prev) =>
            prev.map((upload, idx) =>
              idx === uploadIndex
                ? {
                    ...upload,
                    status: 'error',
                    error: error.response?.data?.detail || 'Upload failed',
                  }
                : upload
            )
          );
          toast.error(`Failed to upload ${file.name}`);
        }
      }

      if (onUploadComplete) {
        onUploadComplete();
      }
    },
    [eventId, documentType, onUploadComplete, uploads.length]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptedFileTypes.split(',').reduce((acc, type) => {
      acc[type.trim()] = [];
      return acc;
    }, {} as Record<string, string[]>),
    maxFiles,
  });

  const removeUpload = (index: number) => {
    setUploads((prev) => prev.filter((_, idx) => idx !== index));
  };

  const getFileIcon = (fileName: string) => {
    const ext = fileName.split('.').pop()?.toLowerCase();
    return <File className="w-5 h-5 text-gray-400" />;
  };

  const getStatusIcon = (status: UploadProgress['status']) => {
    switch (status) {
      case 'uploading':
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return null;
    }
  };

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
        }`}
      >
        <input {...getInputProps()} />
        <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
        {isDragActive ? (
          <p className="text-primary-600 font-medium">Drop files here...</p>
        ) : (
          <div>
            <p className="text-gray-700 font-medium mb-1">
              Drag & drop files here, or click to select
            </p>
            <p className="text-sm text-gray-500">
              Supported: PDF, CSV, Excel, Images (Max {maxFiles} files)
            </p>
          </div>
        )}
      </div>

      {uploads.length > 0 && (
        <div className="space-y-2">
          <h4 className="font-medium text-gray-700">Uploads</h4>
          {uploads.map((upload, index) => (
            <div
              key={index}
              className="flex items-center gap-3 p-3 bg-white border border-gray-200 rounded-lg"
            >
              {getFileIcon(upload.file.name)}
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {upload.file.name}
                </p>
                <p className="text-xs text-gray-500">
                  {(upload.file.size / 1024 / 1024).toFixed(2)} MB
                </p>
                {upload.status === 'uploading' && (
                  <div className="mt-1">
                    <div className="w-full bg-gray-200 rounded-full h-1.5">
                      <div
                        className="bg-primary-600 h-1.5 rounded-full transition-all"
                        style={{ width: `${upload.progress}%` }}
                      />
                    </div>
                  </div>
                )}
                {upload.status === 'error' && upload.error && (
                  <p className="text-xs text-red-600 mt-1">{upload.error}</p>
                )}
              </div>
              <div className="flex items-center gap-2">
                {getStatusIcon(upload.status)}
                {upload.status !== 'uploading' && (
                  <button
                    onClick={() => removeUpload(index)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;

// Made with Bob
