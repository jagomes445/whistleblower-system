import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import Loading from '../components/Loading';
import { magicLinksAPI } from '../api/magicLinks';
import { MagicLink, CreateMagicLinkData } from '../types';

const MagicLinks: React.FC = () => {
  const [magicLinks, setMagicLinks] = useState<MagicLink[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState<CreateMagicLinkData>({
    name: '',
    is_active: true,
    expires_at: null,
  });

  useEffect(() => {
    loadMagicLinks();
  }, []);

  const loadMagicLinks = async () => {
    setLoading(true);
    try {
      const data = await magicLinksAPI.list();
      setMagicLinks(data);
    } catch (err: any) {
      setError('Failed to load magic links');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await magicLinksAPI.create(formData);
      setFormData({ name: '', is_active: true, expires_at: null });
      setShowForm(false);
      loadMagicLinks();
    } catch (err: any) {
      setError('Failed to create magic link');
    }
  };

  const handleToggleStatus = async (id: string, currentStatus: boolean) => {
    try {
      await magicLinksAPI.update(id, { is_active: !currentStatus });
      loadMagicLinks();
    } catch (err: any) {
      setError('Failed to update magic link');
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this magic link?')) {
      return;
    }

    try {
      await magicLinksAPI.delete(id);
      loadMagicLinks();
    } catch (err: any) {
      setError('Failed to delete magic link');
    }
  };

  const copyToClipboard = (url: string) => {
    navigator.clipboard.writeText(url);
    alert('Link copied to clipboard!');
  };

  return (
    <Layout>
      <div className="px-4 sm:px-6 lg:px-8">
        <div className="sm:flex sm:items-center">
          <div className="sm:flex-auto">
            <h1 className="text-2xl font-semibold text-gray-900">Magic Links</h1>
            <p className="mt-2 text-sm text-gray-700">
              Create and manage report submission links for your company.
            </p>
          </div>
          <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
            <button
              type="button"
              onClick={() => setShowForm(!showForm)}
              className="inline-flex items-center justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 sm:w-auto"
            >
              {showForm ? 'Cancel' : 'Create Magic Link'}
            </button>
          </div>
        </div>

        {error && (
          <div className="mt-4 bg-red-50 p-4 rounded-md">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        {/* Create Form */}
        {showForm && (
          <form onSubmit={handleSubmit} className="mt-6 bg-white shadow sm:rounded-lg p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Create New Magic Link
            </h3>
            <div className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                  Name (Optional)
                </label>
                <input
                  type="text"
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="e.g., Employee Portal Link"
                />
              </div>
              <div>
                <label htmlFor="expires_at" className="block text-sm font-medium text-gray-700">
                  Expiration Date (Optional)
                </label>
                <input
                  type="datetime-local"
                  id="expires_at"
                  value={formData.expires_at || ''}
                  onChange={(e) => setFormData({ ...formData, expires_at: e.target.value || null })}
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                />
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="is_active"
                  checked={formData.is_active}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="is_active" className="ml-2 block text-sm text-gray-900">
                  Active
                </label>
              </div>
            </div>
            <div className="mt-5">
              <button
                type="submit"
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Create Link
              </button>
            </div>
          </form>
        )}

        {/* Magic Links List */}
        <div className="mt-8 flex flex-col">
          {loading ? (
            <Loading />
          ) : magicLinks.length === 0 ? (
            <div className="bg-white p-12 text-center rounded-lg shadow">
              <p className="text-gray-500">No magic links created yet</p>
            </div>
          ) : (
            <div className="space-y-4">
              {magicLinks.map((link) => (
                <div key={link.id} className="bg-white shadow rounded-lg p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <h3 className="text-lg font-medium text-gray-900">
                          {link.name || 'Unnamed Link'}
                        </h3>
                        <span
                          className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                            link.is_valid
                              ? 'bg-green-100 text-green-800'
                              : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {link.is_valid ? 'Active' : 'Inactive'}
                        </span>
                      </div>
                      <p className="mt-1 text-sm text-gray-500">
                        Created on {new Date(link.created_at).toLocaleDateString()}
                        {link.expires_at && (
                          <> • Expires: {new Date(link.expires_at).toLocaleString()}</>
                        )}
                      </p>
                      <div className="mt-4">
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Submission URL:
                        </label>
                        <div className="flex items-center space-x-2">
                          <input
                            type="text"
                            value={link.url}
                            readOnly
                            className="flex-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 bg-gray-50 sm:text-sm"
                          />
                          <button
                            onClick={() => copyToClipboard(link.url)}
                            className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                          >
                            Copy
                          </button>
                        </div>
                      </div>
                    </div>
                    <div className="ml-4 flex flex-col space-y-2">
                      <button
                        onClick={() => handleToggleStatus(link.id, link.is_active)}
                        className="text-sm text-blue-600 hover:text-blue-800"
                      >
                        {link.is_active ? 'Deactivate' : 'Activate'}
                      </button>
                      <button
                        onClick={() => handleDelete(link.id)}
                        className="text-sm text-red-600 hover:text-red-800"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default MagicLinks;
