import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaglineSection from './TaglineSection';

test('renders tagline header and text', () => {
  render(<TaglineSection />);
  
  // Check that the header is rendered
  const headerElement = screen.getByText(/Track. Manage. Grow./i);
  expect(headerElement).toBeInTheDocument();

  // Check that the tagline description is rendered
  const descriptionElement = screen.getByText(/Streamline your inventory with smart product management/i);
  expect(descriptionElement).toBeInTheDocument();

  // Check that the company name is rendered
  const companyElement = screen.getByText(/Gen/i);
  expect(companyElement).toBeInTheDocument();
});
