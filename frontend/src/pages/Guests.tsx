import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import {
  Users,
  Search,
  ArrowLeft,
  Loader2,
  Calendar,
  Upload,
} from 'lucide-react';
import { Event } from '@/types';
import api from '@/services/api';
import { toast } from 'react-hot-toast';

const Guests: React.FC = () => {
  const navigate = useNavigate();
  useAuth();
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadEvents();
  }, []);

  const loadEvents = async () => {
    try {
      const response = await api.getEvents({ page: 1, page_size: 100 });
      setEvents(response.events || []);
    } catch (error) {
      toast.error('Failed to load events');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredEvents = events.filter((event) =>
    event.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
              <h1 className="text-2xl font-bold text-gray-900">Guest Management</h1>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search */}
        <div className="card mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search events..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field pl-10"
            />
          </div>
        </div>

        {/* Events List */}
        {isLoading ? (
          <div className="text-center py-12">
            <Loader2 className="w-8 h-8 animate-spin mx-auto text-primary-600" />
            <p className="mt-2 text-gray-600">Loading events...</p>
          </div>
        ) : filteredEvents.length === 0 ? (
          <div className="card text-center py-12">
            <Calendar className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <p className="text-gray-600 mb-4">
              {searchTerm ? 'No events found' : 'No events yet'}
            </p>
            <button
              onClick={() => navigate('/events/create')}
              className="btn-primary"
            >
              Create Your First Event
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredEvents.map((event) => (
              <div
                key={event.id}
                className="card hover:shadow-lg transition-shadow"
              >
                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
                    {event.name}
                  </h3>
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <Calendar className="w-4 h-4" />
                    {new Date(event.event_date).toLocaleDateString()}
                  </div>
                </div>

                <div className="flex items-center justify-between mb-4 p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2">
                    <Users className="w-5 h-5 text-primary-600" />
                    <div>
                      <p className="text-sm text-gray-600">Guests</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {event.confirmed_guests} / {event.expected_guests}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-600">Confirmed</p>
                    <p className="text-lg font-semibold text-green-600">
                      {Math.round((event.confirmed_guests / event.expected_guests) * 100)}%
                    </p>
                  </div>
                </div>

                <div className="space-y-2">
                  <button
                    onClick={() => navigate(`/events/${event.id}/guests`)}
                    className="btn-primary w-full"
                  >
                    Manage Guests
                  </button>
                  <button
                    onClick={() => {
                      // Navigate to guest upload functionality
                      navigate(`/events/${event.id}/guests`);
                    }}
                    className="btn-secondary w-full flex items-center justify-center gap-2"
                  >
                    <Upload className="w-4 h-4" />
                    Upload Guest List
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Guests;

// Made with Bob