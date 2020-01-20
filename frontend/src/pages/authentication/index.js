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
    if (getUrl() === 'login') {
      axios
        .post('../api/rest-auth/login/', {
          username: email,
          password: password
        })
        .then(response => {
          if (response.status !== 200) {
            this.setState({email: ''})
            this.setState({password: ''})
            console.log(response.errors)
          }
          localStorage.setItem('token', response.data.key)
        })
        .catch(exception => {
          console.log(exception)
        })
    } else {
      axios
        .post('../api/rest-auth/register/', {
          username: email,
          password1: password,
          password2: password
        })
        .then(response => {
          if (response.status !== 200) {
            console.log(response.errors)
          }
        })
        .catch(exception => {
          console.log(exception)
        })
    }
    //
    // const token = 'Token '.concat(localStorage.getItem('token'))
    // console.log(token)
    // axios.get('../api/wallets/', {
    //     params: {
    //         filter: ''
    //     },
    //     headers: {Authorization: token}
    // }).then(response => {
    //     if (response.status !== 200) {
    //         console.log(response)
    //     }
    //     console.log(response)
    // }).catch(exception => {
    //     console.log(exception)
    // })
    //
    // console.log('data', email, password)
  }

  useEffect(() => {}, [])

  return (
    <div className="auth-page">
      <div className="container page">
        <div className="row">
          <div className="col-md-6 offset-md-3 col-xs-3">
            <h1 className="text-xs-center">{getUrl()}</h1>
            <p className="text-xs-center">
              <Link to="register">Need an account?</Link>
            </p>
            <form onSubmit={handleSubmit}>
              <fieldset>
                <fieldset className="form-group">
                  <input
                    type="text"
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
                  Sign in
                </button>
              </fieldset>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Authentication
