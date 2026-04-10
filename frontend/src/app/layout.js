import './globals.css';

export const metadata = {
  title: 'SmartPredict AI — Turn Data Into Decisions',
  description: 'AI-powered platform that transforms raw data into actionable business insights. Upload your data, get predictions, and make smarter decisions.',
  keywords: 'AI, data analytics, business intelligence, predictions, machine learning',
  openGraph: {
    title: 'SmartPredict AI',
    description: 'Transform raw data into actionable business insights',
    type: 'website',
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
