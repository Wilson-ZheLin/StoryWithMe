import React from 'react';
import ReactDOM from 'react-dom/client';
import './input.css';
import { RouterProvider } from 'react-router-dom';
import { router } from './routing/routes';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div data-theme="cupcake">
      <RouterProvider router={router} />
    </div>
  </React.StrictMode>
);

