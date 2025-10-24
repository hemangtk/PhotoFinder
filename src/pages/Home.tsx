import { useState, FormEvent } from 'react';
import { FolderOpen, Sparkles, ArrowRight } from 'lucide-react';

interface HomeProps {
  onProcess: (driveLink: string) => void;
  isProcessing: boolean;
}

export function Home({ onProcess, isProcessing }: HomeProps) {
  const [driveLink, setDriveLink] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (driveLink.trim()) {
      onProcess(driveLink.trim());
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4">
      <div className="w-full max-w-2xl mx-auto text-center space-y-8">
        <div className="space-y-4">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 shadow-lg shadow-blue-500/30">
            <Sparkles className="w-10 h-10 text-white" />
          </div>

          <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 dark:from-gray-100 dark:to-gray-300 bg-clip-text text-transparent">
            Find Your Photos
            <br />
            with Natural Language
          </h1>

          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-xl mx-auto leading-relaxed">
            Connect your Google Drive folder and search through your photos using everyday descriptions.
            Powered by AI image captioning and semantic search.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
              <FolderOpen className="w-5 h-5" />
            </div>
            <input
              type="url"
              value={driveLink}
              onChange={(e) => setDriveLink(e.target.value)}
              placeholder="Paste your public Google Drive folder link..."
              disabled={isProcessing}
              required
              className="w-full px-12 py-4 text-base rounded-xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:border-blue-500 dark:focus:border-blue-400 focus:ring-4 focus:ring-blue-500/10 dark:focus:ring-blue-400/10 outline-none transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>

          <button
            type="submit"
            disabled={isProcessing || !driveLink.trim()}
            className="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold rounded-xl shadow-lg shadow-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center space-x-2 mx-auto group"
          >
            {isProcessing ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Processing Photos...</span>
              </>
            ) : (
              <>
                <span>Process Photos</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </form>

        <div className="pt-8 grid grid-cols-1 sm:grid-cols-3 gap-6 text-left">
          <div className="p-6 rounded-xl bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/10 dark:to-cyan-900/10 border border-blue-100 dark:border-blue-900/30">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-3">
              <span className="text-xl">🔗</span>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">Connect Drive</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Paste your public Google Drive folder link
            </p>
          </div>

          <div className="p-6 rounded-xl bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/10 dark:to-pink-900/10 border border-purple-100 dark:border-purple-900/30">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-3">
              <span className="text-xl">✨</span>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">AI Captions</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              BLIP model generates natural descriptions
            </p>
          </div>

          <div className="p-6 rounded-xl bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/10 dark:to-emerald-900/10 border border-green-100 dark:border-green-900/30">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center mb-3">
              <span className="text-xl">🔍</span>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">Smart Search</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Find photos using everyday language
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
