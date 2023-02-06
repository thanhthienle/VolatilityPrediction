import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import Header from './components/Header';
import Detail from './components/Detail';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import "./index.css"

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <BrowserRouter>
      <Header/>
      <Routes>
        <Route exact path="/" element={<App/>}></Route>
        <Route path="/:id" element={<Detail/>}></Route>
      </Routes>
    </BrowserRouter>
);
