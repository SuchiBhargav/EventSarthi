import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import {
  LayoutDashboard,
  Users,
  Calendar,
  LogOut,
  Plus,
  ShieldCheck,
  Building2,
  Upload,
  MessageSquare,
  HelpCircle,
  BarChart3,
  Activity,
} from 'lucide-react';
import { Event } from '@/types';
import api from '@/services/api';
import { toast } from 'react-hot-toast';

type EventAnalytics = {
  event_status?: string;
  guest_analytics?: {
    total_guests?: number;
    confirmed_guests?: number;
    checked_in_guests?: number;
    attendance_rate?: number;
  };
  engagement_analytics?: {
    total_conversations?: number;
    total_broadcasts?: number;
  };
};

type EventConversation = {
  conversation_id: string;
  guest_id: string;
  event_id: string;
  last_message?: string;
  last_message_at?: string;
  created_at?: string;
};

const Dashboard: React.FC = () => {
  const { planner, logout } = useAuth();
  const navigate = useNavigate();
  const [events, setEvents] = useState<Event[]>([]);
  const [stats, setStats] = useState({
    total_events: 0,
    upcoming_events: 0,
    completed_events: 0,
    total_guests: 0,
  });
  const [featuredAnalytics, setFeaturedAnalytics] = useState<EventAnalytics | null>(null);
  const [recentConversations, setRecentConversations] = useState<EventConversation[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const plannerUploadCount = useMemo(
    () =>
      events.filter(
        (event) =>
          event.guest_data_file_name ||
          event.food_menu_file_name ||
          event.faq_file_name ||
          event.venue_details_file_name
      ).length,
    [events]
  );

  const faqCoverageCount = useMemo(
    () => events.filter((event) => event.faq_file_name || event.faq_notes).length,
    [events]
  );

  const askedQuestionsPreview = useMemo(
    () =>
      recentConversations
        .map((conversation) => conversation.last_message?.trim())
        .filter((message): message is string => Boolean(message))
        .slice(0, 3),
    [recentConversations]
  );

  const loadDashboardData = async () => {
    try {
      const [eventsData, statsData] = await Promise.all([
        api.getEvents({ page: 1, page_size: 10 }),
        api.getEventStats(),
      ]);

      const loadedEvents = eventsData.events || [];
      setEvents(loadedEvents);
      setStats(statsData);

      if (loadedEvents.length > 0) {
        const featuredEvent = loadedEvents[0];
        const [analyticsData, conversationsData] = await Promise.all([
          api.getEventAnalytics(featuredEvent.id),
          api.getEventConversations(featuredEvent.id),
        ]);

        setFeaturedAnalytics(analyticsData);
        setRecentConversations(conversationsData.conversations || []);
      } else {
        setFeaturedAnalytics(null);
        setRecentConversations([]);
      }
    } catch (error) {
      toast.error('Failed to load dashboard data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <LayoutDashboard className="w-8 h-8 text-primary-600" />
              <h1 className="text-2xl font-bold text-gray-900">EventSarthi</h1>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{planner?.full_name}</p>
                <p className="text-xs text-gray-500">{planner?.email}</p>
              </div>
              <button
                onClick={handleLogout}
                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8 rounded-2xl border border-gray-200 bg-white p-6">
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div>
              <div className="flex items-center gap-2 mb-2">
                {planner?.role === 'admin' ? (
                  <ShieldCheck className="w-5 h-5 text-purple-600" />
                ) : (
                  <Building2 className="w-5 h-5 text-primary-600" />
                )}
                <span className="text-sm font-medium uppercase tracking-wide text-gray-500">
                  {planner?.role === 'admin' ? 'Internal Admin Dashboard' : 'Planner Dashboard'}
                </span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900">
                {planner?.role === 'admin'
                  ? 'Monitor all planner events and uploaded source data'
                  : 'One place to create, upload, and track every event'}
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                {planner?.role === 'admin'
                  ? 'Review cross-planner activity, uploaded guest/menu/FAQ/venue details, and event readiness.'
                  : 'Use a single event workflow to create the event and attach guest list, food menu, FAQ, and venue files.'}
              </p>
            </div>

            <button
              onClick={() => navigate('/events/create')}
              className="btn-primary flex items-center gap-2"
            >
              <Plus className="w-5 h-5" />
              {planner?.role === 'admin' ? 'Create Managed Event' : 'Create Event'}
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Events</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total_events}</p>
              </div>
              <Calendar className="w-10 h-10 text-primary-500" />
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Upcoming</p>
                <p className="text-3xl font-bold text-gray-900">{stats.upcoming_events}</p>
              </div>
              <Calendar className="w-10 h-10 text-blue-500" />
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Completed</p>
                <p className="text-3xl font-bold text-gray-900">{stats.completed_events}</p>
              </div>
              <Calendar className="w-10 h-10 text-green-500" />
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Guests</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total_guests}</p>
              </div>
              <Users className="w-10 h-10 text-purple-500" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="text-sm text-gray-600">Event Status</p>
                <p className="text-2xl font-bold text-gray-900 capitalize">
                  {featuredAnalytics?.event_status || 'No data'}
                </p>
              </div>
              <Activity className="w-8 h-8 text-emerald-500" />
            </div>
            <p className="text-sm text-gray-600">
              Track the current state of your latest event and readiness level.
            </p>
          </div>

          <div className="card">
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="text-sm text-gray-600">Conversation History</p>
                <p className="text-2xl font-bold text-gray-900">
                  {featuredAnalytics?.engagement_analytics?.total_conversations ?? 0}
                </p>
              </div>
              <MessageSquare className="w-8 h-8 text-blue-500" />
            </div>
            <p className="text-sm text-gray-600">
              Recent guest interactions and WhatsApp conversation sessions.
            </p>
          </div>

          <div className="card">
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="text-sm text-gray-600">Questions Asked</p>
                <p className="text-2xl font-bold text-gray-900">{askedQuestionsPreview.length}</p>
              </div>
              <HelpCircle className="w-8 h-8 text-amber-500" />
            </div>
            <p className="text-sm text-gray-600">
              Latest questions are captured from guest conversations for planner review.
            </p>
          </div>

          <div className="card">
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="text-sm text-gray-600">Planner Uploads</p>
                <p className="text-2xl font-bold text-gray-900">{plannerUploadCount}</p>
              </div>
              <BarChart3 className="w-8 h-8 text-primary-500" />
            </div>
            <p className="text-sm text-gray-600">
              Events with guest, menu, FAQ, or venue source files already attached.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mb-8">
          <div className="card xl:col-span-2">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">
                  {planner?.role === 'admin' ? 'All Planner Events' : 'Your Events'}
                </h2>
                <p className="text-sm text-gray-600 mt-1">
                  Open an event to manage uploads, guests, and event operations from one place.
                </p>
              </div>
            </div>

            {isLoading ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                <p className="mt-2 text-gray-600">Loading events...</p>
              </div>
            ) : events.length === 0 ? (
              <div className="text-center py-12">
                <Calendar className="w-16 h-16 mx-auto text-gray-300 mb-4" />
                <p className="text-gray-600 mb-4">
                  {planner?.role === 'admin' ? 'No planner events yet' : 'No events yet'}
                </p>
                <button
                  onClick={() => navigate('/events/create')}
                  className="btn-primary"
                >
                  {planner?.role === 'admin' ? 'Create First Managed Event' : 'Create Your First Event'}
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                {events.map((event) => (
                  <div
                    key={event.id}
                    className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 hover:shadow-sm transition-all cursor-pointer"
                    onClick={() => navigate(`/events/${event.id}`)}
                  >
                    <div className="flex justify-between items-start gap-4">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 mb-1">{event.name}</h3>
                        <p className="text-sm text-gray-600 mb-2">{event.description}</p>
                        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
                          <span className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            {new Date(event.event_date).toLocaleDateString()}
                          </span>
                          <span className="flex items-center gap-1">
                            <Users className="w-4 h-4" />
                            {event.confirmed_guests} / {event.expected_guests} guests
                          </span>
                          <span className="capitalize px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs font-medium">
                            {event.status}
                          </span>
                          {(event.guest_data_file_name ||
                            event.food_menu_file_name ||
                            event.faq_file_name ||
                            event.venue_details_file_name) && (
                            <span className="flex items-center gap-1 text-emerald-700">
                              <Upload className="w-4 h-4" />
                              Planner data attached
                            </span>
                          )}
                        </div>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/events/${event.id}/manage`);
                        }}
                        className="btn-secondary text-sm"
                      >
                        Open Workspace
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="space-y-6">
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Latest Questions</h3>
                <HelpCircle className="w-5 h-5 text-amber-500" />
              </div>
              {askedQuestionsPreview.length === 0 ? (
                <p className="text-sm text-gray-600">
                  No guest questions captured yet for the latest event.
                </p>
              ) : (
                <div className="space-y-3">
                  {askedQuestionsPreview.map((question, index) => (
                    <div key={`${question}-${index}`} className="rounded-lg bg-amber-50 p-3">
                      <p className="text-sm text-gray-800">{question}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Operational Snapshot</h3>
                <BarChart3 className="w-5 h-5 text-primary-500" />
              </div>
              <div className="space-y-3 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">FAQ coverage</span>
                  <span className="font-semibold text-gray-900">{faqCoverageCount} events</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Confirmed guests</span>
                  <span className="font-semibold text-gray-900">
                    {featuredAnalytics?.guest_analytics?.confirmed_guests ?? 0}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Checked in</span>
                  <span className="font-semibold text-gray-900">
                    {featuredAnalytics?.guest_analytics?.checked_in_guests ?? 0}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Attendance rate</span>
                  <span className="font-semibold text-gray-900">
                    {featuredAnalytics?.guest_analytics?.attendance_rate ?? 0}%
                  </span>
                </div>
              </div>
            </div>

            <button
              onClick={() => navigate('/events')}
              className="card hover:shadow-md transition-shadow text-left w-full"
            >
              <Calendar className="w-8 h-8 text-primary-600 mb-3" />
              <h3 className="font-semibold text-gray-900 mb-1">Event Workspace</h3>
              <p className="text-sm text-gray-600">
                {planner?.role === 'admin'
                  ? 'Open events to review planner uploads, conversations, and readiness.'
                  : 'Use events as the single place to create, upload, and manage everything.'}
              </p>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

// Made with Bob
