import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import {
  FileText,
  Upload,
  Download,
  Trash2,
  ArrowLeft,
  Loader2,
  Calendar,
} from 'lucide-react';
import { Event, Document } from '@/types';
import api from '@/services/api';
import { toast } from 'react-hot-toast';

const Documents: React.FC = () => {
  const navigate = useNavigate();
  const { planner } = useAuth();
  const [events, setEvents] = useState<Event[]>([]);
  const [selectedEventId, setSelectedEventId] = useState<string>('');
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  useEffect(() => {
    loadEvents();
  }, []);

  useEffect(() => {
    if (selectedEventId) {
      loadDocuments();
    }
  }, [selectedEventId]);

  const loadEvents = async () => {
    try {
      const response = await api.getEvents({ page: 1, page_size: 100 });
      const eventsList = response.events || [];
      setEvents(eventsList);
      if (eventsList.length > 0) {
        setSelectedEventId(eventsList[0].id);
      }
    } catch (error) {
      toast.error('Failed to load events');
    } finally {
      setIsLoading(false);
    }
  };

  const loadDocuments = async () => {
    if (!selectedEventId) return;
    
    try {
      const docs = await api.getDocuments(selectedEventId);
      setDocuments(docs);
    } catch (error) {
      toast.error('Failed to load documents');
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !selectedEventId) return;

    setIsUploading(true);
    setUploadProgress(0);

    try {
      await api.uploadDocument(
        selectedEventId,
        file,
        'other',
        (progress) => setUploadProgress(progress)
      );
      toast.success('Document uploaded successfully');
      loadDocuments();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to upload document');
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
      e.target.value = '';
    }
  };

  const handleDeleteDocument = async (documentId: string) => {
    if (!confirm('Are you sure you want to delete this document?')) return;

    try {
      await api.deleteDocument(documentId);
      toast.success('Document deleted successfully');
      loadDocuments();
    } catch (error) {
      toast.error('Failed to delete document');
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <h1 className="text-2xl font-bold text-gray-900">Documents</h1>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {isLoading ? (
          <div className="text-center py-12">
            <Loader2 className="w-8 h-8 animate-spin mx-auto text-primary-600" />
            <p className="mt-2 text-gray-600">Loading...</p>
          </div>
        ) : events.length === 0 ? (
          <div className="card text-center py-12">
            <Calendar className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <p className="text-gray-600 mb-4">No events found</p>
            <button
              onClick={() => navigate('/events/create')}
              className="btn-primary"
            >
              Create Your First Event
            </button>
          </div>
        ) : (
          <>
            {/* Event Selector */}
            <div className="card mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Event
              </label>
              <select
                value={selectedEventId}
                onChange={(e) => setSelectedEventId(e.target.value)}
                className="input-field"
              >
                {events.map((event) => (
                  <option key={event.id} value={event.id}>
                    {event.name} - {new Date(event.event_date).toLocaleDateString()}
                  </option>
                ))}
              </select>
            </div>

            {/* Upload Section */}
            <div className="card mb-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Upload Document
              </h2>
              <div className="flex items-center gap-4">
                <label className="btn-primary cursor-pointer flex items-center gap-2">
                  <Upload className="w-5 h-5" />
                  Choose File
                  <input
                    type="file"
                    onChange={handleFileUpload}
                    disabled={isUploading || !selectedEventId}
                    className="hidden"
                    accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png"
                  />
                </label>
                {isUploading && (
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full transition-all"
                          style={{ width: `${uploadProgress}%` }}
                        />
                      </div>
                      <span className="text-sm text-gray-600">{uploadProgress}%</span>
                    </div>
                  </div>
                )}
              </div>
              <p className="text-sm text-gray-500 mt-2">
                Supported formats: PDF, DOC, DOCX, XLS, XLSX, JPG, PNG (Max 10MB)
              </p>
            </div>

            {/* Documents List */}
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Uploaded Documents
              </h2>
              {documents.length === 0 ? (
                <div className="text-center py-8">
                  <FileText className="w-12 h-12 mx-auto text-gray-300 mb-2" />
                  <p className="text-gray-600">No documents uploaded yet</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {documents.map((doc) => (
                    <div
                      key={doc.id}
                      className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-primary-300 transition-colors"
                    >
                      <div className="flex items-center gap-3 flex-1">
                        <FileText className="w-8 h-8 text-primary-600" />
                        <div className="flex-1 min-w-0">
                          <h3 className="font-medium text-gray-900 truncate">
                            {doc.name}
                          </h3>
                          <div className="flex items-center gap-3 text-sm text-gray-500">
                            <span>{formatFileSize(doc.file_size)}</span>
                            <span>•</span>
                            <span>
                              {new Date(doc.uploaded_at).toLocaleDateString()}
                            </span>
                            <span>•</span>
                            <span className="capitalize">{doc.type}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <a
                          href={doc.file_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                          title="Download"
                        >
                          <Download className="w-5 h-5" />
                        </a>
                        <button
                          onClick={() => handleDeleteDocument(doc.id)}
                          className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Documents;

// Made with Bob