import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Users, Upload, Download, Search } from 'lucide-react';
import { Guest } from '@/types';
import api from '@/services/api';
import { toast } from 'react-hot-toast';
import * as XLSX from 'xlsx';
import Papa from 'papaparse';

const GuestManagement: React.FC = () => {
  const { eventId } = useParams<{ eventId: string }>();
  const [guests, setGuests] = useState<Guest[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showUploadModal, setShowUploadModal] = useState(false);

  useEffect(() => {
    if (eventId) {
      loadGuests();
    }
  }, [eventId]);

  const loadGuests = async () => {
    try {
      const data = await api.getGuests(eventId!);
      setGuests(data.guests || data.items || []);
    } catch (error) {
      toast.error('Failed to load guests');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const fileExtension = file.name.split('.').pop()?.toLowerCase();

    try {
      if (fileExtension === 'csv') {
        Papa.parse(file, {
          header: true,
          complete: async (results) => {
            await processGuestData(results.data);
          },
          error: (error) => {
            toast.error(`CSV parsing error: ${error.message}`);
          },
        });
      } else if (fileExtension === 'xlsx' || fileExtension === 'xls') {
        const reader = new FileReader();
        reader.onload = async (e) => {
          const data = new Uint8Array(e.target?.result as ArrayBuffer);
          const workbook = XLSX.read(data, { type: 'array' });
          const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
          const jsonData = XLSX.utils.sheet_to_json(firstSheet);
          await processGuestData(jsonData);
        };
        reader.readAsArrayBuffer(file);
      }
    } catch (error) {
      toast.error('Failed to process file');
    }
  };

  const processGuestData = async (data: any[]) => {
    try {
      const guestData = data.map((row: any) => ({
        name: row.name || row.Name || row.NAME,
        phone: row.phone || row.Phone || row.PHONE,
        email: row.email || row.Email || row.EMAIL,
        relation_type: row.relation_type || row.relation || 'other',
        room_number: row.room_number || row.room,
        food_preference: row.food_preference || row.food,
        vip_level: row.vip_level || 0,
      }));

      await api.bulkAddGuests(eventId!, guestData);
      toast.success(`${guestData.length} guests added successfully`);
      setShowUploadModal(false);
      loadGuests();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to add guests');
    }
  };

  const downloadTemplate = () => {
    const template = [
      {
        name: 'John Doe',
        phone: '+919876543210',
        email: 'john@example.com',
        relation_type: 'friend',
        room_number: '101',
        food_preference: 'vegetarian',
        vip_level: 0,
      },
    ];

    const ws = XLSX.utils.json_to_sheet(template);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Guests');
    XLSX.writeFile(wb, 'guest_list_template.xlsx');
    toast.success('Template downloaded');
  };

  const filteredGuests = guests.filter(
    (guest) =>
      guest.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      guest.phone.includes(searchTerm)
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Guest Management</h1>
        <p className="text-gray-600">Upload and manage your event guest list</p>
      </div>

      {/* Actions Bar */}
      <div className="card mb-6">
        <div className="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search guests..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field pl-10"
            />
          </div>

          <div className="flex gap-2">
            <button onClick={downloadTemplate} className="btn-secondary flex items-center gap-2">
              <Download className="w-4 h-4" />
              Download Template
            </button>
            <button
              onClick={() => setShowUploadModal(true)}
              className="btn-primary flex items-center gap-2"
            >
              <Upload className="w-4 h-4" />
              Upload Guest List
            </button>
          </div>
        </div>
      </div>

      {/* Guest List */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">
            Guests ({filteredGuests.length})
          </h2>
        </div>

        {isLoading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            <p className="mt-2 text-gray-600">Loading guests...</p>
          </div>
        ) : filteredGuests.length === 0 ? (
          <div className="text-center py-12">
            <Users className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <p className="text-gray-600 mb-4">No guests found</p>
            <button
              onClick={() => setShowUploadModal(true)}
              className="btn-primary"
            >
              Upload Guest List
            </button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Phone
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Relation
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Room
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredGuests.map((guest) => (
                  <tr key={guest.guest_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{guest.name}</div>
                      {guest.email && (
                        <div className="text-sm text-gray-500">{guest.email}</div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {guest.phone}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800 capitalize">
                        {guest.relation_type}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {guest.room_number || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {guest.checked_in ? (
                        <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
                          Checked In
                        </span>
                      ) : (
                        <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800">
                          Pending
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Upload Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-xl font-semibold mb-4">Upload Guest List</h3>
            <p className="text-gray-600 mb-4">
              Upload a CSV or Excel file with guest information. Download the template to see
              the required format.
            </p>

            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <Upload className="w-12 h-12 mx-auto text-gray-400 mb-2" />
                <label className="cursor-pointer">
                  <span className="text-primary-600 hover:text-primary-700 font-medium">
                    Choose file
                  </span>
                  <input
                    type="file"
                    accept=".csv,.xlsx,.xls"
                    onChange={handleFileUpload}
                    className="hidden"
                  />
                </label>
                <p className="text-sm text-gray-500 mt-1">CSV or Excel files only</p>
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => setShowUploadModal(false)}
                  className="btn-secondary flex-1"
                >
                  Cancel
                </button>
                <button onClick={downloadTemplate} className="btn-primary flex-1">
                  Download Template
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GuestManagement;

// Made with Bob
