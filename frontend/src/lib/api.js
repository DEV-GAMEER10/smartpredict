/**
 * SmartPredict AI — API Client
 * Handles all communication with the FastAPI backend.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...(options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
          ...options.headers,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || `HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error.message === 'Failed to fetch') {
        throw new Error('Cannot connect to server. Please make sure the backend is running on port 8000.');
      }
      throw error;
    }
  }

  // ── Upload ──────────────────────────────────────────
  async uploadFile(file, onProgress) {
    const formData = new FormData();
    formData.append('file', file);

    // Use XMLHttpRequest for progress tracking
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open('POST', `${API_BASE}/api/upload`);

      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable && onProgress) {
          onProgress(Math.round((e.loaded / e.total) * 100));
        }
      };

      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(JSON.parse(xhr.responseText));
        } else {
          try {
            const error = JSON.parse(xhr.responseText);
            reject(new Error(error.detail || 'Upload failed'));
          } catch {
            reject(new Error('Upload failed'));
          }
        }
      };

      xhr.onerror = () => reject(new Error('Cannot connect to server'));
      xhr.send(formData);
    });
  }

  // ── Datasets ────────────────────────────────────────
  async getDatasets() {
    return this.request('/api/datasets');
  }

  async getDataset(id) {
    return this.request(`/api/datasets/${id}`);
  }

  // ── Insights ────────────────────────────────────────
  async getInsights(datasetId) {
    return this.request(`/api/insights/${datasetId}`);
  }

  async refreshInsights(datasetId) {
    return this.request(`/api/insights/${datasetId}/refresh`);
  }

  // ── Chat ────────────────────────────────────────────
  async sendChat(datasetId, message) {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ dataset_id: datasetId, message }),
    });
  }

  // ── Health ──────────────────────────────────────────
  async healthCheck() {
    return this.request('/api/health');
  }
}

const api = new ApiClient();
export default api;
