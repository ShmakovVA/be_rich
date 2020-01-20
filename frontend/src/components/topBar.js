import React from 'react'
import {Link, NavLink} from 'react-router-dom'

const TopBar = () => {
  return (
    <nav className="navbar navbar-expand-sm bg-dark navbar-dark sticky-top">
      <div className="container">
        <Link to="/" className="navbar-brand">
          BeRich
        </Link>
        <ul className="nav navbar-nav pull-right">
          <li className="nav-item">
            <NavLink to="/" className="nav-link" exact>
              Home
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/pay" className="nav-link">
              Pay
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/login" className="nav-link">
              Sign in
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/register" className="nav-link">
              Sign up
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  )
}

export default TopBar
