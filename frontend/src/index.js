import React from 'react'
import ReactDOM from 'react-dom'
import {BrowserRouter} from 'react-router-dom'
import Routes from './routes'
import TopBar from './components/topBar'

const App = () => {
  return (
    <div>
      <BrowserRouter>
        <TopBar />
        <Routes />
      </BrowserRouter>
    </div>
  )
}

const wrapper = document.getElementById('app')
wrapper ? ReactDOM.render(<App />, wrapper) : null
