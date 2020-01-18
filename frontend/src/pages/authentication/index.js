import React, {useEffect, useState} from 'react'
import {Link} from 'react-router-dom'
import axios from 'axios'

const Authentication = () => {
    // const [token_, setToken] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const handleSubmit = event => {
        event.preventDefault()
        var to = ''
        axios.post('../api/login', {
            "username": email,
            "password": password
        }).then(response => {
            if (response.status !== 200) {
                this.setState({email: ''})
                console.log(response.errors)
            }
            to = response.data.token
            // setToken(response.data.token)
            console.log(to)
            // console.log(token_)
        }).catch(exception => {
            console.log(exception)
        })

        axios.get('../api/test', {
            params: {
                token: 'e6ea0c8cdbbcf7e8ab31e0818095e406d8a30c54',
                filter: ''
            }
        }).then(response => {
            if (response.status !== 200) {
                console.log(response)
            }
            console.log(response)
        }).catch(exception => {
            console.log(exception)
        })

        console.log('data', email, password)
    }

    useEffect(() => {

    }, [])

    return (
        <div className="auth-page">
            <div className="container page">
                <div className="row">
                    <div className="col-md-6 offset-md-3 col-xs-3">
                        <h1 className="text-xs-center">Login</h1>
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
                                <button
                                    className="btn btn-lg btn-primary pull-xs-right">
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
