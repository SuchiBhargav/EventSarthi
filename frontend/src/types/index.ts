// Type definitions for EventSarthi Frontend

export interface Planner {
  planner_id: string;
  email: string;
  phone: string;
  full_name: string;
  company_name?: string;
  profile_image_url?: string;
  whatsapp_number?: string;
  is_active: boolean;
  is_verified: boolean;
  role: 'admin' | 'planner';
  subscription_tier: 'free' | 'pro' | 'enterprise';
  language_preference: string;
  timezone: string;
  created_at: string;
  last_login_at?: string;
}

export interface Event {
  id: string;
  planner_id: string;
  name: string;
  event_type: 'wedding' | 'birthday' | 'corporate' | 'conference' | 'other';
  description?: string;
  event_date: string;
  venue: string;
  expected_guests: number;
  confirmed_guests: number;
  budget?: number;
  status: 'draft' | 'planning' | 'confirmed' | 'ongoing' | 'completed' | 'cancelled';
  guest_data_file_name?: string;
  guest_data_file_url?: string;
  food_menu_file_name?: string;
  food_menu_file_url?: string;
  faq_file_name?: string;
  faq_file_url?: string;
  venue_details_file_name?: string;
  venue_details_file_url?: string;
  guest_data_notes?: string;
  food_menu_notes?: string;
  faq_notes?: string;
  venue_details_notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Guest {
  guest_id: string;
  event_id: string;
  name: string;
  phone: string;
  email?: string;
  relation_type: 'uncle' | 'aunt' | 'friend' | 'colleague' | 'vip' | 'other';
  tone_preference: 'formal' | 'casual' | 'respectful';
  language: 'en' | 'hi' | 'kn';
  vip_level?: number;
  health_notes?: Record<string, any>;
  food_preference?: string;
  hotel_name?: string;
  room_number?: string;
  is_attending: boolean;
  checked_in: boolean;
  created_at: string;
}

export interface FAQ {
  faq_id: string;
  event_id: string;
  question: string;
  answer: string;
  category: 'venue' | 'food' | 'schedule' | 'transport' | 'accommodation' | 'general';
  created_at: string;
}

export interface Document {
  id: string;
  event_id: string;
  name: string;
  type: 'guest_list' | 'menu' | 'map' | 'schedule' | 'faq' | 'other';
  file_url: string;
  file_size: number;
  mime_type: string;
  uploaded_at: string;
}

export interface UploadProgress {
  file: File;
  progress: number;
  status: 'pending' | 'uploading' | 'success' | 'error';
  error?: string;
}

export interface AuthState {
  isAuthenticated: boolean;
  planner: Planner | null;
  token: string | null;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

// Made with Bob
