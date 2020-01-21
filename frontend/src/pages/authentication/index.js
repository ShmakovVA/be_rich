import React, {useEffect, useState} from 'react'
import {Link} from 'react-router-dom'
import axios from 'axios'

const Authentication = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const getUrl = () => {
    let full_url = window.location.href
    return full_url.substring(full_url.lastIndexOf('/') + 1)
  }

  const handleSubmit = event => {
    event.preventDefault()
    let url = getUrl()
    if (url === 'login') {
      axios
        .post('../api/rest-auth/login/', {
          username: email,
          password: password
        })
        .then(response => {
          localStorage.setItem('token', response.data.key)
          alert(`You are logged in now ${email}!`)
          window.location = '/'
        })
        .catch(exception => {
          setEmail('')
          setPassword('')
          alert('Wrong credentials, try again!')
        })
    }
    if (url === 'register') {
      axios
        .post('../api/rest-auth/register/', {
          username: email,
          email: email,
          password1: password,
          password2: password
        })
        .then(response => {
          alert('You was registered, try to log in now !')
          window.location = '/login'
        })
        .catch(exception => {
          alert("You haven't been registered, try again later !")
        })
    }
  }

  useEffect(() => {
    if (getUrl() === 'logout') {
      axios
        .post('../api/rest-auth/logout/', {})
        .then(response => {
          localStorage.removeItem('token');
          alert('You was logged out')
        })
        .catch(exception => {
          alert("You haven't been logged out, try again later !")
        })
    }
  }, [])

  return (getUrl() !== 'logout') ? (
    <div className="auth-page bg-secondary">
      <div className="container page">
        <div className="row">
          <div className="col-md-6 col-xs-3">
            <h1 className="text-xs-center">{getUrl()}</h1>
            <p className="text-xs-center">
              <Link to="register">Need an account?</Link>
            </p>
            <form onSubmit={handleSubmit}>
              <fieldset>
                <fieldset className="form-group">
                  <input
                    type="email"
                    className="form-control form-control-lg"
                    placeholder="Email"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                  />
                </fieldset>
                <fieldset className="form-group">
                  <input
                    type="password"
                    className="form-control form-control-lg"
                    placeholder="Password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                  />
                </fieldset>
                <button className="btn btn-lg btn-primary pull-xs-right">
                  {getUrl()}
                </button>
              </fieldset>
            </form>
          </div>
        </div>
      </div>
    </div>
  ) : (
    <div></div>
  )
}

export default Authentication
