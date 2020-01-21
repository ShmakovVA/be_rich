import React, {useState} from 'react'
import DataProvider from '../../components/dataProvider'
import Table from '../../components/table'
import axios from 'axios'

const TransactionList = () => {
  const [account_sort_by, setASortBy] = useState('id')
  const [wallet_sort_by, setWSortBy] = useState('id')
  const [transaction_sort_by, setTSortBy] = useState('id')
  const [account_filters, setAFilters] = useState({})
  const [wallet_filters, setWFilters] = useState({})
  const [transaction_filters, setTFilters] = useState({})

  const getInputValueById = id => {
    return document.getElementById(id).value
  }

  const buildFilters = id => {
    let filters = {}
    filters = Object.assign(
      {message: getInputValueById('message_input')},
      filters
    )
    filters = Object.assign(
      {status: getInputValueById('status_input')},
      filters
    )
    filters = Object.assign(
      {from_wallet: getInputValueById('from_w_input')},
      filters
    )
    filters = Object.assign(
      {to_wallet: getInputValueById('to_w_input')},
      filters
    )
    filters = Object.assign(
      {amount: getInputValueById('amount_input')},
      filters
    )
    for (let [key, value] of Object.entries(filters)) {
      if (!value) {
        delete filters[key]
      }
    }
    return filters
  }

  const handleSortFilter = event => {
    event.preventDefault()
    setTSortBy(getInputValueById('sort_input'))
    setTFilters(buildFilters())
  }

  const filterForm = () => {
    return (
      <div className="container">
        <form onSubmit={handleSortFilter}>
          <h2 className="badge badge-info">Filters and sorting</h2>
          <div className="row">
            <div className="col-md-6">
              <p>Status</p>
              <input
                id="status_input"
                type="text"
                className="form-control form-control-lg"
                placeholder="status"
              />
              <p>From</p>
              <input
                id="from_w_input"
                type="text"
                className="form-control form-control-lg"
                placeholder="from wallet"
              />
              <p>To</p>
              <input
                id="to_w_input"
                type="text"
                className="form-control form-control-lg"
                placeholder="to wallet"
              />
            </div>
            <div className="col-md-6">
              <p>amount</p>
              <input
                id="amount_input"
                type="text"
                className="form-control form-control-lg"
                placeholder="amount"
              />
              <p>message</p>
              <input
                id="message_input"
                type="text"
                className="form-control form-control-lg"
                placeholder="message"
              />
              <p>Sort by</p>
              <input
                id="sort_input"
                type="text"
                className="form-control form-control-lg"
                placeholder="sort field"
              />
            </div>
          </div>
          <button
            className="btn btn-lg btn-primary pull-right"
            style={{width: '100%'}}
          >
            Apply
          </button>
        </form>
      </div>
    )
  }

  return (
    <div className="bg-secondary">
      <h1>Account(s)</h1>
      <DataProvider
        endpoint="../api/accounts/"
        render={data => <Table data={data} />}
        sort_by={account_sort_by}
        filters={account_filters}
      />
      <h1>Wallets</h1>
      <DataProvider
        endpoint="../api/wallets/"
        render={data => <Table data={data} />}
        sort_by={wallet_sort_by}
        filters={wallet_filters}
      />
      <h1>Transactions</h1>
      {filterForm()}
      <DataProvider
        endpoint="../api/transactions/"
        render={data => <Table data={data} />}
        sort_by={transaction_sort_by}
        filters={transaction_filters}
      />
    </div>
  )
}

export default TransactionList
