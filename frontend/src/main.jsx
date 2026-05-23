import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// Ensure root fills the viewport
const rootEl = document.getElementById('root')
rootEl.style.height = '100%'
document.documentElement.style.height = '100%'
document.body.style.height = '100%'

createRoot(rootEl).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
