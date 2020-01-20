import React, {useEffect, useState} from 'react'
import {Link} from 'react-router-dom'
import axios from 'axios'

const Transaction = () => {
  const [amount, setamount] = useState('')
  const [message, setMessage] = useState('')
  const [from_wallet, setWalletFrom] = useState('')
  const [to_wallet, setWalletTo] = useState('')

  const handleSubmit = event => {
    event.preventDefault()
    const token = 'Token '.concat(localStorage.getItem('token'))
    axios
      .post(
        '../api/accounts/do_transaction/',
        {
          wallet_from: from_wallet,
          wallet_to: to_wallet,
          amount: amount,
          message: message
        },
        {headers: {Authorization: token}}
      )
      .then(response => {
        if (response.data.error) {
          alert(`Error : ${response.data.error}`)
        } else {
          alert(`We sent your money to ${to_wallet} !`)
        }
      })
      .catch(exception => {
        alert(`Sorry, but something went wrong... Try again later`)
      })
  }

  useEffect(() => {}, [])

  return (
    <div className="bg-secondary">
      <div className="container page">
        <div className="row">
          <div className="col-md-6 col-xs-3">
            <h1 className="text-xs-center">
              Fill the form for apply transaction
            </h1>
            <form onSubmit={handleSubmit}>
              <fieldset>
                <fieldset className="form-group">
                  <input
                    type="text"
                    className="form-control form-control-lg"
                    placeholder="Your wallet"
                    value={from_wallet}
                    onChange={e => setWalletFrom(e.target.value)}
                  />
                </fieldset>
                <fieldset className="form-group">
                  <input
                    type="text"
                    className="form-control form-control-lg"
                    placeholder="His/her wallet"
                    value={to_wallet}
                    onChange={e => setWalletTo(e.target.value)}
                  />
                </fieldset>
                <fieldset className="form-group">
                  <input
                    type="float"
                    className="form-control form-control-lg"
                    placeholder="Amount"
                    value={amount}
                    onChange={e => setamount(e.target.value)}
                  />
                </fieldset>
                <fieldset className="form-group">
                  <input
                    type="text"
                    className="form-control form-control-lg"
                    placeholder="Message"
                    value={message}
                    onChange={e => setMessage(e.target.value)}
                  />
                </fieldset>
                <button className="btn btn-lg btn-primary pull-xs-right">
                  Pay
                </button>
              </fieldset>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Transaction
