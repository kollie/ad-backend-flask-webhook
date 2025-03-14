import { useEffect } from 'react';

declare global {
  interface Window {
    frameworkReady?: () => void;
  }
}

export function useFrameworkReady() {
  useEffect(() => {
    try {
      window.frameworkReady?.();
    } catch (error) {
      // Safely handle any potential errors
      console.warn('Framework ready error:', error);
    }
  }, []);
}