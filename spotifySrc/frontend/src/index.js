import React from 'react';
import {createRoot} from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom'
import App from './App';

// Clear the existing HTML content
document.body.innerHTML = '<div id="app"></div>';

// Render your React component instead
const root = createRoot(document.getElementById('app'));

root.render(
    <Router>
        <React.StrictMode>
            <App />
        </React.StrictMode>
    </Router>
);