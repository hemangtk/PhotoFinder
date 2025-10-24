import { useState, useEffect } from 'react';
import { SearchBar } from '../components/SearchBar';
import { PhotoGrid } from '../components/PhotoGrid';
import { Photo } from '../lib/supabase';
import { ImageOff } from 'lucide-react';

interface SearchProps {
  onSearch: (query: string) => Promise<Photo[]>;
}

export function Search({ onSearch }: SearchProps) {
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [currentQuery, setCurrentQuery] = useState('');

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setHasSearched(true);
    setCurrentQuery(query);
    try {
      const results = await onSearch(query);
      setPhotos(results);
    } catch (error) {
      console.error('Search error:', error);
      setPhotos([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100">
            Search Your Photos
          </h1>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Describe what you're looking for in natural language
          </p>
        </div>

        <SearchBar onSearch={handleSearch} isLoading={isLoading} />

        {hasSearched && !isLoading && (
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {photos.length > 0 ? (
                <>
                  Found <span className="font-semibold text-gray-900 dark:text-gray-100">{photos.length}</span> {photos.length === 1 ? 'photo' : 'photos'} matching "{currentQuery}"
                </>
              ) : (
                <>No results for "{currentQuery}"</>
              )}
            </p>
          </div>
        )}

        {!hasSearched && !isLoading && (
          <div className="text-center py-16">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gray-100 dark:bg-gray-800 mb-4">
              <ImageOff className="w-10 h-10 text-gray-400 dark:text-gray-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Ready to search
            </h3>
            <p className="text-gray-600 dark:text-gray-400 max-w-md mx-auto">
              Try searching for things like "person in front of church", "beach sunset", or "group photo"
            </p>
          </div>
        )}

        {(hasSearched || isLoading) && (
          <PhotoGrid photos={photos} isLoading={isLoading} />
        )}
      </div>
    </div>
  );
}
