import { Copy, ExternalLink, Check } from 'lucide-react';
import { useState } from 'react';
import { Photo } from '../lib/supabase';

interface PhotoCardProps {
  photo: Photo;
}

export function PhotoCard({ photo }: PhotoCardProps) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopyLink = async () => {
    await navigator.clipboard.writeText(photo.drive_link);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getImageUrl = (driveLink: string) => {
    const fileIdMatch = driveLink.match(/[-\w]{25,}/);
    if (fileIdMatch) {
      return `https://drive.google.com/uc?export=view&id=${fileIdMatch[0]}`;
    }
    return driveLink;
  };

  return (
    <div className="group relative bg-white dark:bg-gray-800 rounded-xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 border border-gray-200 dark:border-gray-700">
      <div className="aspect-square relative bg-gray-100 dark:bg-gray-900">
        {!imageLoaded && !imageError && (
          <div className="absolute inset-0 animate-pulse bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-800" />
        )}

        {!imageError ? (
          <img
            src={getImageUrl(photo.drive_link)}
            alt={photo.caption}
            loading="lazy"
            onLoad={() => setImageLoaded(true)}
            onError={() => setImageError(true)}
            className={`w-full h-full object-cover transition-opacity duration-300 ${
              imageLoaded ? 'opacity-100' : 'opacity-0'
            }`}
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center text-gray-400 dark:text-gray-600">
            <span className="text-sm">Failed to load</span>
          </div>
        )}

        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      </div>

      <div className="p-4 space-y-3">
        <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2 leading-relaxed">
          {photo.caption}
        </p>

        {photo.similarity !== undefined && (
          <div className="flex items-center space-x-2">
            <div className="flex-1 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full transition-all duration-500"
                style={{ width: `${photo.similarity * 100}%` }}
              />
            </div>
            <span className="text-xs font-medium text-gray-500 dark:text-gray-400">
              {(photo.similarity * 100).toFixed(0)}%
            </span>
          </div>
        )}

        <div className="flex items-center space-x-2 pt-2">
          <button
            onClick={handleCopyLink}
            className="flex-1 flex items-center justify-center space-x-2 px-3 py-2 text-sm font-medium bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg transition-colors"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                <span>Copy Link</span>
              </>
            )}
          </button>

          <a
            href={photo.drive_link}
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors"
            aria-label="Open in Drive"
          >
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>
    </div>
  );
}
