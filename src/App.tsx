import { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Toast, ToastType } from './components/Toast';
import { Home } from './pages/Home';
import { Search } from './pages/Search';
import { ThemeProvider } from './contexts/ThemeContext';
import { supabase, Photo } from './lib/supabase';

type Page = 'home' | 'search';

interface ToastState {
  message: string;
  type: ToastType;
}

function AppContent() {
  const [currentPage, setCurrentPage] = useState<Page>('home');
  const [isProcessing, setIsProcessing] = useState(false);
  const [toast, setToast] = useState<ToastState | null>(null);

  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000';

  const showToast = (message: string, type: ToastType) => {
    setToast({ message, type });
  };

  const handleProcessDrive = async (driveLink: string) => {
    setIsProcessing(true);

    try {
      const response = await fetch(`${BACKEND_URL}/api/fetch-drive`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ driveLink }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch Drive images');
      }

      const { images } = await response.json();

      if (!images || images.length === 0) {
        showToast('No images found in the Drive folder', 'info');
        setIsProcessing(false);
        return;
      }

      const captionResponse = await fetch(`${BACKEND_URL}/api/caption`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ images }),
      });

      if (!captionResponse.ok) {
        throw new Error('Failed to generate captions');
      }

      const { captions } = await captionResponse.json();

      const storeResponse = await fetch(`${BACKEND_URL}/api/store`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ photos: captions }),
      });

      if (!storeResponse.ok) {
        throw new Error('Failed to store photos');
      }

      showToast(`Successfully processed ${images.length} photos!`, 'success');
      setCurrentPage('search');
    } catch (error) {
      console.error('Processing error:', error);
      showToast(
        error instanceof Error ? error.message : 'Failed to process photos',
        'error'
      );
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSearch = async (query: string): Promise<Photo[]> => {
    try {
      const response = await fetch(
        `${BACKEND_URL}/api/search?${new URLSearchParams({ query })}`
      );

      if (!response.ok) {
        throw new Error('Search failed');
      }

      const { results } = await response.json();
      return results || [];
    } catch (error) {
      console.error('Search error:', error);
      showToast('Search failed. Please try again.', 'error');
      return [];
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 transition-colors">
      <Navbar onNavigate={setCurrentPage} currentPage={currentPage} />

      <main>
        {currentPage === 'home' && (
          <Home onProcess={handleProcessDrive} isProcessing={isProcessing} />
        )}
        {currentPage === 'search' && <Search onSearch={handleSearch} />}
      </main>

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

export default App;
