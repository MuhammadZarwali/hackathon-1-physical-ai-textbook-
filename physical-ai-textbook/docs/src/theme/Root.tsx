import React from 'react';
import ChatWidget from '../components/ChatWidget';

// Root component that wraps the entire Docusaurus app
// This allows the ChatWidget to appear on all pages
export default function Root({ children }) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
