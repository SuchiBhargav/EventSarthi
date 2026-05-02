import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { HelpCircle, Plus, Edit2, Trash2, Save, X } from 'lucide-react';
import { FAQ } from '@/types';
import api from '@/services/api';
import { toast } from 'react-hot-toast';

const FAQManagement: React.FC = () => {
  const { eventId } = useParams<{ eventId: string }>();
  const [faqs, setFaqs] = useState<FAQ[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [editingFaq, setEditingFaq] = useState<FAQ | null>(null);
  const [formData, setFormData] = useState({
    question: '',
    answer: '',
    category: 'general' as FAQ['category'],
  });

  useEffect(() => {
    if (eventId) {
      loadFAQs();
    }
  }, [eventId]);

  const loadFAQs = async () => {
    try {
      const data = await api.getFAQs(eventId!);
      setFaqs(data.faqs || data.items || []);
    } catch (error) {
      toast.error('Failed to load FAQs');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      if (editingFaq) {
        await api.updateFAQ(editingFaq.faq_id, formData);
        toast.success('FAQ updated successfully');
      } else {
        await api.addFAQ(eventId!, formData);
        toast.success('FAQ added successfully');
      }

      setFormData({ question: '', answer: '', category: 'general' });
      setShowAddModal(false);
      setEditingFaq(null);
      loadFAQs();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to save FAQ');
    }
  };

  const handleEdit = (faq: FAQ) => {
    setEditingFaq(faq);
    setFormData({
      question: faq.question,
      answer: faq.answer,
      category: faq.category,
    });
    setShowAddModal(true);
  };

  const handleDelete = async (faqId: string) => {
    if (!confirm('Are you sure you want to delete this FAQ?')) return;

    try {
      await api.deleteFAQ(faqId);
      toast.success('FAQ deleted successfully');
      loadFAQs();
    } catch (error) {
      toast.error('Failed to delete FAQ');
    }
  };

  const categories: FAQ['category'][] = [
    'venue',
    'food',
    'schedule',
    'transport',
    'accommodation',
    'general',
  ];

  const getCategoryColor = (category: FAQ['category']) => {
    const colors = {
      venue: 'bg-blue-100 text-blue-800',
      food: 'bg-green-100 text-green-800',
      schedule: 'bg-purple-100 text-purple-800',
      transport: 'bg-yellow-100 text-yellow-800',
      accommodation: 'bg-pink-100 text-pink-800',
      general: 'bg-gray-100 text-gray-800',
    };
    return colors[category];
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">FAQ Management</h1>
        <p className="text-gray-600">
          Manage frequently asked questions for your event. The AI bot will use these to answer
          guest queries.
        </p>
      </div>

      {/* Add FAQ Button */}
      <div className="mb-6">
        <button
          onClick={() => {
            setEditingFaq(null);
            setFormData({ question: '', answer: '', category: 'general' });
            setShowAddModal(true);
          }}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Add FAQ
        </button>
      </div>

      {/* FAQ List */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="card text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            <p className="mt-2 text-gray-600">Loading FAQs...</p>
          </div>
        ) : faqs.length === 0 ? (
          <div className="card text-center py-12">
            <HelpCircle className="w-16 h-16 mx-auto text-gray-300 mb-4" />
            <p className="text-gray-600 mb-4">No FAQs added yet</p>
            <button onClick={() => setShowAddModal(true)} className="btn-primary">
              Add Your First FAQ
            </button>
          </div>
        ) : (
          faqs.map((faq) => (
            <div key={faq.faq_id} className="card">
              <div className="flex justify-between items-start gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded-full capitalize ${getCategoryColor(
                        faq.category
                      )}`}
                    >
                      {faq.category}
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{faq.question}</h3>
                  <p className="text-gray-600">{faq.answer}</p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleEdit(faq)}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"
                  >
                    <Edit2 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(faq.faq_id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Add/Edit Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-semibold mb-4">
              {editingFaq ? 'Edit FAQ' : 'Add New FAQ'}
            </h3>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category
                </label>
                <select
                  value={formData.category}
                  onChange={(e) =>
                    setFormData({ ...formData, category: e.target.value as FAQ['category'] })
                  }
                  className="input-field"
                  required
                >
                  {categories.map((cat) => (
                    <option key={cat} value={cat} className="capitalize">
                      {cat}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Question
                </label>
                <input
                  type="text"
                  value={formData.question}
                  onChange={(e) => setFormData({ ...formData, question: e.target.value })}
                  placeholder="e.g., What time does the event start?"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Answer
                </label>
                <textarea
                  value={formData.answer}
                  onChange={(e) => setFormData({ ...formData, answer: e.target.value })}
                  placeholder="Provide a clear and helpful answer..."
                  rows={4}
                  className="input-field"
                  required
                />
              </div>

              <div className="flex gap-2 pt-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowAddModal(false);
                    setEditingFaq(null);
                    setFormData({ question: '', answer: '', category: 'general' });
                  }}
                  className="btn-secondary flex-1"
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary flex-1 flex items-center justify-center gap-2">
                  <Save className="w-4 h-4" />
                  {editingFaq ? 'Update' : 'Add'} FAQ
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default FAQManagement;

// Made with Bob
