import React from 'react';
import {createRoot} from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import App from './App';
import Radio from './radio';

// Render your React component instead
const root = createRoot(document.getElementById('root'));

root.render(
    <Router>
        <Routes>
            <Route path='/' element={ <App /> } />
            <Route path="/radio" element={ <Radio /> } />
            <Route path='*' element={ <App /> } />
        </Routes>
    </Router>
);